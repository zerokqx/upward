import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { mergeOpenApiSpecs, type OpenApiDoc } from './merger.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SPECS_DIR = path.resolve(__dirname, '../specs');

export interface ServiceSpecConfig {
  id: string;
  name: string;
  prefix: string;
  liveUrl: string;
  fallbackFile: string;
}

export const SERVICES: ServiceSpecConfig[] = [
  {
    id: 'bff',
    name: 'BFF Service (Client Gateway)',
    prefix: 'BFF',
    liveUrl: process.env.BFF_DOCS_URL || 'http://127.0.0.1:4000/docs-json',
    fallbackFile: path.join(SPECS_DIR, 'bff.json'),
  },
  {
    id: 'uptime',
    name: 'Uptime Service (Core Monitoring)',
    prefix: 'Uptime',
    liveUrl: process.env.UPTIME_DOCS_URL || 'http://127.0.0.1:3000/docs/docs.json',
    fallbackFile: path.join(SPECS_DIR, 'uptime.json'),
  },
  {
    id: 'identify',
    name: 'Identify Service (Auth & Tokens)',
    prefix: 'Identify',
    liveUrl: process.env.IDENTIFY_DOCS_URL || 'http://127.0.0.1:3001/openapi.json',
    fallbackFile: path.join(SPECS_DIR, 'identify.json'),
  },
];

const cache: Map<string, { doc: OpenApiDoc; timestamp: number }> = new Map();
const CACHE_TTL_MS = 5000; // 5 seconds cache

export async function fetchOrFallbackSpec(
  service: ServiceSpecConfig,
): Promise<OpenApiDoc> {
  const cached = cache.get(service.id);
  const now = Date.now();
  if (cached && now - cached.timestamp < CACHE_TTL_MS) {
    return cached.doc;
  }

  // Try live fetch with 1.5s timeout
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 1500);
    const res = await fetch(service.liveUrl, {
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    if (res.ok) {
      const doc = (await res.json()) as OpenApiDoc;
      cache.set(service.id, { doc, timestamp: now });
      return doc;
    }
  } catch {
    // If live fetch fails, fall back to offline JSON
  }

  // Read fallback file
  if (fs.existsSync(service.fallbackFile)) {
    const content = fs.readFileSync(service.fallbackFile, 'utf8');
    const doc = JSON.parse(content) as OpenApiDoc;
    cache.set(service.id, { doc, timestamp: now });
    return doc;
  }

  // Minimal stub if file missing
  return {
    openapi: '3.0.0',
    info: { title: service.name, version: '0.1.0' },
    paths: {},
  };
}

export async function getAllSpecs(): Promise<{
  bff: OpenApiDoc;
  uptime: OpenApiDoc;
  identify: OpenApiDoc;
  combined: OpenApiDoc;
}> {
  const [bff, uptime, identify] = await Promise.all([
    fetchOrFallbackSpec(SERVICES[0]),
    fetchOrFallbackSpec(SERVICES[1]),
    fetchOrFallbackSpec(SERVICES[2]),
  ]);

  const combined = mergeOpenApiSpecs([
    { prefix: SERVICES[0].prefix, name: SERVICES[0].name, doc: bff },
    { prefix: SERVICES[1].prefix, name: SERVICES[1].name, doc: uptime },
    { prefix: SERVICES[2].prefix, name: SERVICES[2].name, doc: identify },
  ]);

  return { bff, uptime, identify, combined };
}

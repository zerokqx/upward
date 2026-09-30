import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SPECS_DIR = path.resolve(__dirname, '../specs');

export interface ServiceSpecConfig {
  id: string;
  name: string;
  liveUrl: string;
  fallbackFile: string;
}

export const SERVICES: ServiceSpecConfig[] = [
  {
    id: 'bff',
    name: 'BFF (Client Gateway)',
    liveUrl: process.env.BFF_DOCS_URL || 'http://127.0.0.1:4000/docs-json',
    fallbackFile: path.join(SPECS_DIR, 'bff.json'),
  },
  {
    id: 'uptime',
    name: 'Uptime (Monitoring Core)',
    liveUrl: process.env.UPTIME_DOCS_URL || 'http://127.0.0.1:3000/docs/docs.json',
    fallbackFile: path.join(SPECS_DIR, 'uptime.json'),
  },
  {
    id: 'identify',
    name: 'Identify (Auth Service)',
    liveUrl: process.env.IDENTIFY_DOCS_URL || 'http://127.0.0.1:3001/openapi.json',
    fallbackFile: path.join(SPECS_DIR, 'identify.json'),
  },
];

const cache: Map<string, { doc: Record<string, unknown>; timestamp: number }> = new Map();
const CACHE_TTL_MS = 5000;

export async function fetchOrFallbackSpec(
  service: ServiceSpecConfig,
): Promise<Record<string, unknown>> {
  const cached = cache.get(service.id);
  const now = Date.now();
  if (cached && now - cached.timestamp < CACHE_TTL_MS) {
    return cached.doc;
  }

  // Live fetch with 1.5s timeout
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 1500);
    const res = await fetch(service.liveUrl, { signal: controller.signal });
    clearTimeout(timeoutId);
    if (res.ok) {
      const doc = (await res.json()) as Record<string, unknown>;
      cache.set(service.id, { doc, timestamp: now });
      return doc;
    }
  } catch {
    // Live service is offline, fallback to bundled static spec
  }

  // Fallback to static JSON spec
  if (fs.existsSync(service.fallbackFile)) {
    const content = fs.readFileSync(service.fallbackFile, 'utf8');
    const doc = JSON.parse(content) as Record<string, unknown>;
    cache.set(service.id, { doc, timestamp: now });
    return doc;
  }

  return {
    openapi: '3.0.0',
    info: { title: service.name, version: '0.1.0' },
    paths: {},
  };
}

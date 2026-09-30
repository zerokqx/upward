import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SPECS_DIR = path.resolve(__dirname, '../specs');

export interface ServiceSpecConfig {
  id: string;
  name: string;
  serverUrl: string;
  liveUrl: string;
  fallbackFile: string;
}

export const SERVICES: ServiceSpecConfig[] = [
  {
    id: 'bff',
    name: 'BFF (Client Gateway)',
    serverUrl: process.env.BFF_SERVER_URL || 'http://localhost:4000',
    liveUrl: process.env.BFF_DOCS_URL || 'http://127.0.0.1:4000/docs-json',
    fallbackFile: path.join(SPECS_DIR, 'bff.json'),
  },
  {
    id: 'uptime',
    name: 'Uptime (Monitoring Core)',
    serverUrl: process.env.UPTIME_SERVER_URL || 'http://localhost:3000',
    liveUrl: process.env.UPTIME_DOCS_URL || 'http://127.0.0.1:3000/docs/docs.json',
    fallbackFile: path.join(SPECS_DIR, 'uptime.json'),
  },
  {
    id: 'identify',
    name: 'Identify (Auth Service)',
    serverUrl: process.env.IDENTIFY_SERVER_URL || 'http://localhost:3001',
    liveUrl: process.env.IDENTIFY_DOCS_URL || 'http://127.0.0.1:3001/openapi.json',
    fallbackFile: path.join(SPECS_DIR, 'identify.json'),
  },
];

const cache: Map<string, { doc: Record<string, unknown>; timestamp: number }> = new Map();
const CACHE_TTL_MS = 5000;

function normalizeSpec(
  rawDoc: Record<string, unknown>,
  service: ServiceSpecConfig,
): Record<string, unknown> {
  const doc = { ...rawDoc };
  const servers = (doc.servers as Array<{ url: string; description?: string }>) || [];
  const hasAbsoluteServer = servers.some(
    (s) => s.url.startsWith('http://') || s.url.startsWith('https://'),
  );

  if (!hasAbsoluteServer) {
    doc.servers = [
      { url: service.serverUrl, description: `${service.name} (Direct)` },
      ...servers.filter((s) => s.url !== '/'),
    ];
  }

  return doc;
}

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
      const doc = normalizeSpec((await res.json()) as Record<string, unknown>, service);
      cache.set(service.id, { doc, timestamp: now });
      return doc;
    }
  } catch {
    // Live service is offline, fallback to bundled static spec
  }

  // Fallback to static JSON spec
  if (fs.existsSync(service.fallbackFile)) {
    const content = fs.readFileSync(service.fallbackFile, 'utf8');
    const doc = normalizeSpec(JSON.parse(content) as Record<string, unknown>, service);
    cache.set(service.id, { doc, timestamp: now });
    return doc;
  }

  return {
    openapi: '3.0.0',
    info: { title: service.name, version: '0.1.0' },
    servers: [{ url: service.serverUrl, description: service.name }],
    paths: {},
  };
}

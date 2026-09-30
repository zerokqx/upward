import Fastify, { type FastifyInstance } from 'fastify';
import cors from '@fastify/cors';
import scalarTheme from '@scalar/fastify-api-reference';
import { getAllSpecs, fetchOrFallbackSpec, SERVICES } from './specs.js';

export async function buildServer(): Promise<FastifyInstance> {
  const fastify = Fastify({
    logger: process.env.NODE_ENV !== 'test',
  });

  await fastify.register(cors, {
    origin: true,
  });

  // Health check
  fastify.get('/health', async () => {
    return { status: 'ok', service: 'docs', timestamp: new Date().toISOString() };
  });

  // Raw JSON specification endpoints
  fastify.get('/specs/bff.json', async (_req, reply) => {
    const spec = await fetchOrFallbackSpec(SERVICES[0]);
    return reply.type('application/json').send(spec);
  });

  fastify.get('/specs/uptime.json', async (_req, reply) => {
    const spec = await fetchOrFallbackSpec(SERVICES[1]);
    return reply.type('application/json').send(spec);
  });

  fastify.get('/specs/identify.json', async (_req, reply) => {
    const spec = await fetchOrFallbackSpec(SERVICES[2]);
    return reply.type('application/json').send(spec);
  });

  fastify.get('/specs/combined.json', async (_req, reply) => {
    const { combined } = await getAllSpecs();
    return reply.type('application/json').send(combined);
  });

  // Dedicated Scalar documentation for each service
  await fastify.register(scalarTheme, {
    routePrefix: '/bff',
    configuration: {
      url: '/specs/bff.json',
      pageTitle: 'BFF Service API Reference',
      theme: 'purple',
    },
  });

  await fastify.register(scalarTheme, {
    routePrefix: '/uptime',
    configuration: {
      url: '/specs/uptime.json',
      pageTitle: 'Uptime Service API Reference',
      theme: 'deepSpace',
    },
  });

  await fastify.register(scalarTheme, {
    routePrefix: '/identify',
    configuration: {
      url: '/specs/identify.json',
      pageTitle: 'Identify Service API Reference',
      theme: 'saturn',
    },
  });

  // Main Unified Portal at root `/`
  await fastify.register(scalarTheme, {
    routePrefix: '/',
    configuration: {
      sources: [
        { title: '1. Combined Platform API (All Services)', url: '/specs/combined.json' },
        { title: '2. BFF (Client Gateway)', url: '/specs/bff.json' },
        { title: '3. Uptime Service (Core)', url: '/specs/uptime.json' },
        { title: '4. Identify Service (Auth)', url: '/specs/identify.json' },
      ],
      pageTitle: 'Upward Developer Documentation Portal',
      theme: 'purple',
    },
  });

  return fastify;
}

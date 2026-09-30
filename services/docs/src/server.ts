import Fastify, { type FastifyInstance } from 'fastify';
import cors from '@fastify/cors';
import fastifySwagger from '@fastify/swagger';
import fastifySwaggerUi from '@fastify/swagger-ui';
import { getAllSpecs, fetchOrFallbackSpec, SERVICES } from './specs.js';

export async function buildServer(): Promise<FastifyInstance> {
  const fastify = Fastify({
    logger: process.env.NODE_ENV !== 'test',
  });

  await fastify.register(cors, {
    origin: true,
  });

  // Base swagger plugin registration required by @fastify/swagger-ui
  await fastify.register(fastifySwagger, {
    openapi: {
      info: {
        title: 'Upward Platform Documentation',
        version: '0.1.0',
      },
    },
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

  // Dedicated Swagger UI documentation for BFF
  await fastify.register(async (scope) => {
    await scope.register(fastifySwaggerUi, {
      routePrefix: '/bff',
      theme: {
        title: 'BFF Service API Documentation',
      },
      uiConfig: {
        url: '/specs/bff.json',
        docExpansion: 'list',
        deepLinking: true,
      },
    });
  });

  // Dedicated Swagger UI documentation for Uptime
  await fastify.register(async (scope) => {
    await scope.register(fastifySwaggerUi, {
      routePrefix: '/uptime',
      theme: {
        title: 'Uptime Service API Documentation',
      },
      uiConfig: {
        url: '/specs/uptime.json',
        docExpansion: 'list',
        deepLinking: true,
      },
    });
  });

  // Dedicated Swagger UI documentation for Identify
  await fastify.register(async (scope) => {
    await scope.register(fastifySwaggerUi, {
      routePrefix: '/identify',
      theme: {
        title: 'Identify Service API Documentation',
      },
      uiConfig: {
        url: '/specs/identify.json',
        docExpansion: 'list',
        deepLinking: true,
      },
    });
  });

  // Main Unified Portal at root `/` with multi-spec dropdown
  await fastify.register(async (scope) => {
    await scope.register(fastifySwaggerUi, {
      routePrefix: '/',
      theme: {
        title: 'Upward Developer Documentation Portal',
      },
      uiConfig: {
        urls: [
          { name: '1. Combined Platform API (All Services)', url: '/specs/combined.json' },
          { name: '2. BFF (Client Gateway)', url: '/specs/bff.json' },
          { name: '3. Uptime Service (Core)', url: '/specs/uptime.json' },
          { name: '4. Identify Service (Auth)', url: '/specs/identify.json' },
        ],
        docExpansion: 'list',
        deepLinking: true,
      },
    });
  });

  return fastify;
}

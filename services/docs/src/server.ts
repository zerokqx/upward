import Fastify, { type FastifyInstance } from 'fastify';
import cors from '@fastify/cors';
import fastifySwagger from '@fastify/swagger';
import fastifySwaggerUi from '@fastify/swagger-ui';
import { fetchOrFallbackSpec, SERVICES } from './specs.js';

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

  // Raw JSON specification endpoints for each service
  for (const service of SERVICES) {
    fastify.get(`/specs/${service.id}.json`, async (_req, reply) => {
      const spec = await fetchOrFallbackSpec(service);
      return reply.type('application/json').send(spec);
    });
  }

  // Quick redirects to service in Swagger UI
  for (const service of SERVICES) {
    fastify.get(`/${service.id}`, async (_req, reply) => {
      return reply.redirect(`/?url=/specs/${service.id}.json`);
    });
  }

  // Swagger UI Portal at root `/` with native multi-service dropdown selector
  await fastify.register(fastifySwaggerUi, {
    routePrefix: '/',
    theme: {
      title: 'Upward Platform Documentation',
    },
    uiConfig: {
      urls: SERVICES.map((service) => ({
        name: service.name,
        url: `/specs/${service.id}.json`,
      })),
      docExpansion: 'list',
      deepLinking: true,
    },
  });

  return fastify;
}

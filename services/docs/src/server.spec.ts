import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import type { FastifyInstance } from 'fastify';
import { buildServer } from './server.js';

describe('Docs Server API', () => {
  let app: FastifyInstance;

  beforeAll(async () => {
    process.env.NODE_ENV = 'test';
    app = await buildServer();
    await app.ready();
  });

  afterAll(async () => {
    await app.close();
  });

  describe('GET /health', () => {
    it('should return health status 200', async () => {
      const res = await app.inject({
        method: 'GET',
        url: '/health',
      });
      expect(res.statusCode).toBe(200);
      const json = res.json();
      expect(json.status).toBe('ok');
      expect(json.service).toBe('docs');
    });
  });

  describe('GET /specs/*.json', () => {
    it('should return bff.json spec with paths', async () => {
      const res = await app.inject({
        method: 'GET',
        url: '/specs/bff.json',
      });
      expect(res.statusCode).toBe(200);
      const json = res.json();
      expect(json.info.title).toContain('BFF');
      expect(Object.keys(json.paths).length).toBeGreaterThan(0);
    });

    it('should return uptime.json spec with paths', async () => {
      const res = await app.inject({
        method: 'GET',
        url: '/specs/uptime.json',
      });
      expect(res.statusCode).toBe(200);
      const json = res.json();
      expect(json.info.title).toContain('Uptime');
      expect(Object.keys(json.paths).length).toBeGreaterThan(0);
    });

    it('should return identify.json spec with paths', async () => {
      const res = await app.inject({
        method: 'GET',
        url: '/specs/identify.json',
      });
      expect(res.statusCode).toBe(200);
      const json = res.json();
      expect(json.info.title).toContain('Identify');
      expect(Object.keys(json.paths).length).toBeGreaterThan(0);
    });
  });

  describe('Swagger UI Portal and Navigation', () => {
    it('should return 200 and Swagger UI HTML on root /', async () => {
      const res = await app.inject({
        method: 'GET',
        url: '/',
      });
      expect(res.statusCode).toBe(200);
      expect(res.headers['content-type']).toContain('text/html');
      expect(res.body).toContain('swagger-ui');
    });

    it('should redirect /bff to Swagger UI with BFF spec url', async () => {
      const res = await app.inject({
        method: 'GET',
        url: '/bff',
      });
      expect(res.statusCode).toBe(302);
      expect(res.headers.location).toBe('/?url=/specs/bff.json');
    });

    it('should redirect /uptime to Swagger UI with Uptime spec url', async () => {
      const res = await app.inject({
        method: 'GET',
        url: '/uptime',
      });
      expect(res.statusCode).toBe(302);
      expect(res.headers.location).toBe('/?url=/specs/uptime.json');
    });

    it('should redirect /identify to Swagger UI with Identify spec url', async () => {
      const res = await app.inject({
        method: 'GET',
        url: '/identify',
      });
      expect(res.statusCode).toBe(302);
      expect(res.headers.location).toBe('/?url=/specs/identify.json');
    });
  });
});

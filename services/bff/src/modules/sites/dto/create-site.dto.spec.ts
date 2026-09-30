import { describe, it, expect } from 'vitest';
import { CreateSiteSchema } from './create-site.dto.js';

describe('CreateSite Zod Schema', () => {
  it('should validate valid https URL', () => {
    const payload = { site: 'https://example.com' };
    const result = CreateSiteSchema.parse(payload);
    expect(result).toEqual({ site: 'https://example.com' });
  });

  it('should validate valid http URL', () => {
    const payload = { site: 'http://my-service.internal:8080' };
    const result = CreateSiteSchema.parse(payload);
    expect(result).toEqual({ site: 'http://my-service.internal:8080' });
  });

  it('should preprocess and accept "url" parameter as fallback', () => {
    const payload = { url: 'https://example.org' };
    const result = CreateSiteSchema.parse(payload);
    expect(result).toEqual({ site: 'https://example.org' });
  });

  it('should reject unsupported schemes (ftp, ws, javascript, etc.)', () => {
    expect(() =>
      CreateSiteSchema.parse({ site: 'ftp://files.example.com' }),
    ).toThrow();
  });

  it('should reject non-URL strings', () => {
    expect(() => CreateSiteSchema.parse({ site: 'not-a-valid-url' })).toThrow();
  });

  it('should reject empty or missing site field', () => {
    expect(() => CreateSiteSchema.parse({})).toThrow();
    expect(() => CreateSiteSchema.parse({ site: '' })).toThrow();
  });
});

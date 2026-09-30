import { describe, it, expect } from 'vitest';
import { RegisterSchema } from './register.dto.js';
import { LoginSchema } from './login.dto.js';
import { RefreshSchema } from './refresh.dto.js';

describe('Auth Zod DTO Schemas', () => {
  describe('RegisterSchema', () => {
    it('should validate valid registration payload', () => {
      const payload = {
        email: 'user@example.com',
        password: 'Password123!',
      };
      const result = RegisterSchema.parse(payload);
      expect(result).toEqual(payload);
    });

    it('should reject invalid email', () => {
      expect(() =>
        RegisterSchema.parse({
          email: 'not-an-email',
          password: 'Password123!',
        }),
      ).toThrow();
    });

    it('should reject password shorter than 8 characters', () => {
      expect(() =>
        RegisterSchema.parse({
          email: 'user@example.com',
          password: '123',
        }),
      ).toThrow();
    });

    it('should reject password longer than 128 characters', () => {
      expect(() =>
        RegisterSchema.parse({
          email: 'user@example.com',
          password: 'a'.repeat(129),
        }),
      ).toThrow();
    });
  });

  describe('LoginSchema', () => {
    it('should validate valid login payload', () => {
      const payload = {
        email: 'user@example.com',
        password: 'Password123!',
      };
      const result = LoginSchema.parse(payload);
      expect(result).toEqual(payload);
    });

    it('should reject empty email or password', () => {
      expect(() => LoginSchema.parse({})).toThrow();
    });
  });

  describe('RefreshSchema', () => {
    it('should validate valid UUID v4 refresh token', () => {
      const payload = {
        refresh: 'b428d082-356a-4b92-808c-901a1e582845',
      };
      const result = RefreshSchema.parse(payload);
      expect(result).toEqual(payload);
    });

    it('should reject non-UUID refresh token', () => {
      expect(() =>
        RefreshSchema.parse({
          refresh: 'invalid-non-uuid-token',
        }),
      ).toThrow();
    });
  });
});

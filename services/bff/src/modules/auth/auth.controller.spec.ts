import { Test, TestingModule } from '@nestjs/testing';
import { PassportModule } from '@nestjs/passport';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import type { Request, Response } from 'express';
import { AuthController } from './auth.controller.js';
import { AuthService } from './services/auth.service.js';
import { JwtAuthGuard } from './guards/jwt-auth.guard.js';
import { GoogleAuthGuard } from './guards/google-auth.guard.js';

describe('AuthController', () => {
  let controller: AuthController;
  let authService: {
    register: ReturnType<typeof vi.fn>;
    login: ReturnType<typeof vi.fn>;
    refresh: ReturnType<typeof vi.fn>;
  };

  const createMockResponse = () => {
    return {
      cookie: vi.fn(),
      clearCookie: vi.fn(),
      status: vi.fn().mockReturnThis(),
      json: vi.fn().mockReturnThis(),
    } as unknown as Response;
  };

  beforeEach(async () => {
    authService = {
      register: vi.fn(),
      login: vi.fn(),
      refresh: vi.fn(),
    };

    const module: TestingModule = await Test.createTestingModule({
      imports: [PassportModule.register({ defaultStrategy: 'jwt' })],
      controllers: [AuthController],
      providers: [
        {
          provide: AuthService,
          useValue: authService,
        },
      ],
    })
      .overrideGuard(JwtAuthGuard)
      .useValue({ canActivate: () => true })
      .overrideGuard(GoogleAuthGuard)
      .useValue({ canActivate: () => true })
      .compile();

    controller = module.get<AuthController>(AuthController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  describe('register', () => {
    it('should call authService.register with dto', async () => {
      const dto = { email: 'test@example.com', password: 'Password123!' };
      authService.register.mockResolvedValue({
        message: 'Пользователь успешно зарегистрирован',
      });

      const result = await controller.register(dto);
      expect(authService.register).toHaveBeenCalledWith(dto);
      expect(result).toEqual({
        message: 'Пользователь успешно зарегистрирован',
      });
    });
  });

  describe('login', () => {
    it('should call authService.login, set refresh cookie and return only access token', async () => {
      const dto = { email: 'test@example.com', password: 'Password123!' };
      const tokens = { access: 'jwt-access-token', refresh: 'refresh-uuid' };
      authService.login.mockResolvedValue(tokens);
      const mockRes = createMockResponse();

      const result = await controller.login(dto, mockRes);
      expect(authService.login).toHaveBeenCalledWith(dto);
      expect(mockRes.cookie).toHaveBeenCalledWith(
        'refresh_token',
        'refresh-uuid',
        expect.objectContaining({ httpOnly: true, sameSite: 'lax' }),
      );
      expect(result).toEqual({ access: 'jwt-access-token' });
    });
  });

  describe('refresh', () => {
    it('should extract refresh token from cookie, call authService.refresh, rotate cookie and return access', async () => {
      const tokens = {
        access: 'new-jwt-access-token',
        refresh: 'new-refresh-uuid',
      };
      authService.refresh.mockResolvedValue(tokens);
      const mockReq = {
        cookies: { refresh_token: 'b428d082-356a-4b92-808c-901a1e582845' },
      } as unknown as Request;
      const mockRes = createMockResponse();

      const result = await controller.refresh(mockReq, mockRes);
      expect(authService.refresh).toHaveBeenCalledWith({
        refresh: 'b428d082-356a-4b92-808c-901a1e582845',
      });
      expect(mockRes.cookie).toHaveBeenCalledWith(
        'refresh_token',
        'new-refresh-uuid',
        expect.objectContaining({ httpOnly: true }),
      );
      expect(result).toEqual({ access: 'new-jwt-access-token' });
    });

    it('should accept refresh token from body if cookie is missing', async () => {
      const tokens = {
        access: 'new-jwt-access-token',
        refresh: 'new-refresh-uuid',
      };
      authService.refresh.mockResolvedValue(tokens);
      const mockReq = { cookies: {} } as unknown as Request;
      const mockRes = createMockResponse();
      const dto = { refresh: 'b428d082-356a-4b92-808c-901a1e582845' };

      const result = await controller.refresh(mockReq, mockRes, dto);
      expect(authService.refresh).toHaveBeenCalledWith(dto);
      expect(result).toEqual({ access: 'new-jwt-access-token' });
    });

    it('should throw UnauthorizedException if refresh token is missing in both cookie and body', async () => {
      const mockReq = { cookies: {} } as unknown as Request;
      const mockRes = createMockResponse();

      await expect(controller.refresh(mockReq, mockRes)).rejects.toThrow();
    });
  });

  describe('logout', () => {
    it('should clear refresh cookie', () => {
      const mockRes = createMockResponse();
      const result = controller.logout(mockRes);
      expect(mockRes.clearCookie).toHaveBeenCalledWith(
        'refresh_token',
        expect.objectContaining({ httpOnly: true }),
      );
      expect(result).toEqual({ message: 'Успешный выход' });
    });
  });

  describe('me', () => {
    it('should return current user', () => {
      const user = { id: 'usr-123', email: 'test@example.com' };
      const result = controller.getProfile(user);
      expect(result).toEqual(user);
    });
  });
});

import { Test, TestingModule } from '@nestjs/testing';
import { PassportModule } from '@nestjs/passport';
import { describe, it, expect, beforeEach, vi } from 'vitest';
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
    it('should call authService.login with credentials', async () => {
      const dto = { email: 'test@example.com', password: 'Password123!' };
      const tokens = { access: 'jwt-access-token', refresh: 'refresh-uuid' };
      authService.login.mockResolvedValue(tokens);

      const result = await controller.login(dto);
      expect(authService.login).toHaveBeenCalledWith(dto);
      expect(result).toEqual(tokens);
    });
  });

  describe('refresh', () => {
    it('should call authService.refresh with refresh token', async () => {
      const dto = { refresh: 'b428d082-356a-4b92-808c-901a1e582845' };
      const tokens = {
        access: 'new-jwt-access-token',
        refresh: 'new-refresh-uuid',
      };
      authService.refresh.mockResolvedValue(tokens);

      const result = await controller.refresh(dto);
      expect(authService.refresh).toHaveBeenCalledWith(dto);
      expect(result).toEqual(tokens);
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

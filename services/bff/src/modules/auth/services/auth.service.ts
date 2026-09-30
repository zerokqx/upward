import { Injectable } from '@nestjs/common';
import { getAuth } from '../../../shared/api/orval/identify-service/auth/auth.js';
import { handleUpstreamError } from '../../../shared/utils/axios-error.js';
import type { RegisterDto } from '../dto/register.dto.js';
import type { LoginDto } from '../dto/login.dto.js';
import type { RefreshDto } from '../dto/refresh.dto.js';
import type { LoginByPasswordResponseDto } from '../../../shared/api/orval/identify-service/identify-service.schemas.js';

@Injectable()
export class AuthService {
  private readonly identifyAuth = getAuth();

  async register(dto: RegisterDto): Promise<{ message: string }> {
    try {
      await this.identifyAuth.registerByPassword({
        email: dto.email,
        password: dto.password,
      });
      return { message: 'Пользователь успешно зарегистрирован' };
    } catch (error) {
      handleUpstreamError(error, 'identify-service');
    }
  }

  async login(dto: LoginDto): Promise<LoginByPasswordResponseDto> {
    try {
      return await this.identifyAuth.loginByPassword({
        email: dto.email,
        password: dto.password,
      });
    } catch (error) {
      handleUpstreamError(error, 'identify-service');
    }
  }

  async refresh(dto: RefreshDto): Promise<LoginByPasswordResponseDto> {
    try {
      return await this.identifyAuth.refresh({
        refresh: dto.refresh,
      });
    } catch (error) {
      handleUpstreamError(error, 'identify-service');
    }
  }
}

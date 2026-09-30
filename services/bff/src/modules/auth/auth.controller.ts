import {
  Body,
  Controller,
  Get,
  HttpCode,
  HttpStatus,
  Post,
  Req,
  Res,
  UseGuards,
} from '@nestjs/common';
import {
  ApiBearerAuth,
  ApiOperation,
  ApiResponse,
  ApiTags,
} from '@nestjs/swagger';
import type { Request, Response } from 'express';
import { AuthService } from './services/auth.service.js';
import { RegisterDto } from './dto/register.dto.js';
import { LoginDto } from './dto/login.dto.js';
import { RefreshDto } from './dto/refresh.dto.js';
import { JwtAuthGuard } from './guards/jwt-auth.guard.js';
import { GoogleAuthGuard } from './guards/google-auth.guard.js';
import { CurrentUser } from './decorators/current-user.decorator.js';
import type { AuthenticatedUser } from './strategies/jwt.strategy.js';
import type { GoogleUser } from './strategies/google.strategy.js';

@ApiTags('Auth')
@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('register')
  @HttpCode(HttpStatus.CREATED)
  @ApiOperation({ summary: 'Регистрация нового пользователя по email и паролю' })
  @ApiResponse({ status: 201, description: 'Пользователь успешно зарегистрирован' })
  @ApiResponse({ status: 400, description: 'Невалидные входные данные' })
  @ApiResponse({ status: 409, description: 'Пользователь с таким email уже существует' })
  async register(@Body() dto: RegisterDto) {
    return await this.authService.register(dto);
  }

  @Post('login')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Аутентификация по email и паролю' })
  @ApiResponse({ status: 200, description: 'Успешная аутентификация, возвращены Access и Refresh токены' })
  @ApiResponse({ status: 400, description: 'Невалидные учетные данные' })
  @ApiResponse({ status: 401, description: 'Неверный пароль' })
  @ApiResponse({ status: 404, description: 'Пользователь не найден' })
  async login(@Body() dto: LoginDto) {
    return await this.authService.login(dto);
  }

  @Post('refresh')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Обновление пары токенов по Refresh токену (Token Rotation)' })
  @ApiResponse({ status: 200, description: 'Токены успешно обновлены' })
  @ApiResponse({ status: 401, description: 'Невалидный или протухший Refresh токен' })
  async refresh(@Body() dto: RefreshDto) {
    return await this.authService.refresh(dto);
  }

  @Get('google')
  @UseGuards(GoogleAuthGuard)
  @ApiOperation({ summary: 'Инициация входа через Google OAuth' })
  @ApiResponse({ status: 302, description: 'Редирект на страницу согласия Google' })
  googleLogin() {
    // Guard автоматически осуществляет редирект на форму входа Google
  }

  @Get('google/callback')
  @UseGuards(GoogleAuthGuard)
  @ApiOperation({ summary: 'OAuth Callback для завершения входа через Google' })
  @ApiResponse({ status: 200, description: 'Успешная аутентификация через Google' })
  googleCallback(@Req() req: Request, @Res() res: Response) {
    const user = req.user as GoogleUser;
    // Возвращаем профиль полученного через Google пользователя
    return res.status(HttpStatus.OK).json({
      message: 'Успешная авторизация через Google OAuth',
      user,
    });
  }

  @Get('me')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Получение профиля текущего авторизованного пользователя' })
  @ApiResponse({ status: 200, description: 'Данные текущего пользователя' })
  @ApiResponse({ status: 401, description: 'Пользователь не авторизован' })
  getProfile(@CurrentUser() user: AuthenticatedUser) {
    return user;
  }
}

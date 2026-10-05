import {
  Body,
  Controller,
  Get,
  HttpCode,
  HttpStatus,
  Post,
  Req,
  Res,
  UnauthorizedException,
  UseGuards,
} from '@nestjs/common';
import {
  ApiBearerAuth,
  ApiOperation,
  ApiResponse,
  ApiTags,
} from '@nestjs/swagger';
import type { Request, Response, CookieOptions } from 'express';
import { AuthService } from './services/auth.service.js';
import { RegisterDto } from './dto/register.dto.js';
import { LoginDto } from './dto/login.dto.js';
import { RefreshDto } from './dto/refresh.dto.js';
import { AuthResponseDto } from './dto/auth-response.dto.js';
import { JwtAuthGuard } from './guards/jwt-auth.guard.js';
import { GoogleAuthGuard } from './guards/google-auth.guard.js';
import { CurrentUser } from './decorators/current-user.decorator.js';
import type { AuthenticatedUser } from './strategies/jwt.strategy.js';
import type { GoogleUser } from './strategies/google.strategy.js';

const REFRESH_COOKIE_NAME = 'refresh_token';

const COOKIE_OPTIONS: CookieOptions = {
  httpOnly: true,
  secure: process.env.NODE_ENV === 'production',
  sameSite: 'lax',
  path: '/',
  maxAge: 30 * 24 * 60 * 60 * 1000, // 30 дней (соответствует TTL сессии в identify)
};

@ApiTags('Auth')
@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('register')
  @HttpCode(HttpStatus.CREATED)
  @ApiOperation({
    summary: 'Регистрация нового пользователя по email и паролю',
  })
  @ApiResponse({
    status: 201,
    description: 'Пользователь успешно зарегистрирован',
  })
  @ApiResponse({ status: 400, description: 'Невалидные входные данные' })
  @ApiResponse({
    status: 409,
    description: 'Пользователь с таким email уже существует',
  })
  async register(@Body() dto: RegisterDto) {
    return await this.authService.register(dto);
  }

  @Post('login')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Аутентификация по email и паролю' })
  @ApiResponse({
    status: 200,
    type: AuthResponseDto,
    description:
      'Успешная аутентификация, возвращен Access токен в теле и Refresh токен в HttpOnly cookie',
  })
  @ApiResponse({ status: 400, description: 'Невалидные учетные данные' })
  @ApiResponse({ status: 401, description: 'Неверный пароль' })
  @ApiResponse({ status: 404, description: 'Пользователь не найден' })
  async login(
    @Body() dto: LoginDto,
    @Res({ passthrough: true }) res: Response,
  ): Promise<AuthResponseDto> {
    const tokens = await this.authService.login(dto);
    res.cookie(REFRESH_COOKIE_NAME, tokens.refresh, COOKIE_OPTIONS);
    return { access: tokens.access };
  }

  @Post('refresh')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({
    summary: 'Обновление пары токенов (Token Rotation)',
  })
  @ApiResponse({
    status: 200,
    type: AuthResponseDto,
    description:
      'Access токен успешно обновлен, новый Refresh токен сохранен в HttpOnly cookie',
  })
  @ApiResponse({
    status: 401,
    description: 'Невалидный или протухший Refresh токен',
  })
  async refresh(
    @Req() req: Request,
    @Res({ passthrough: true }) res: Response,
    @Body() dto?: RefreshDto,
  ): Promise<AuthResponseDto> {
    const refreshToken = req.cookies?.[REFRESH_COOKIE_NAME] ?? dto?.refresh;
    if (!refreshToken) {
      throw new UnauthorizedException(
        'Refresh токен отсутствует в cookies или теле запроса',
      );
    }

    const tokens = await this.authService.refresh({ refresh: refreshToken });
    res.cookie(REFRESH_COOKIE_NAME, tokens.refresh, COOKIE_OPTIONS);
    return { access: tokens.access };
  }

  @Post('logout')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Выход из системы (очистка HttpOnly cookie)' })
  @ApiResponse({ status: 200, description: 'Успешный выход' })
  logout(@Res({ passthrough: true }) res: Response) {
    res.clearCookie(REFRESH_COOKIE_NAME, COOKIE_OPTIONS);
    return { message: 'Успешный выход' };
  }

  @Get('google')
  @UseGuards(GoogleAuthGuard)
  @ApiOperation({ summary: 'Инициация входа через Google OAuth' })
  @ApiResponse({
    status: 302,
    description: 'Редирект на страницу согласия Google',
  })
  googleLogin() {
    // Guard автоматически осуществляет редирект на форму входа Google
  }

  @Get('google/callback')
  @UseGuards(GoogleAuthGuard)
  @ApiOperation({ summary: 'OAuth Callback для завершения входа через Google' })
  @ApiResponse({
    status: 200,
    description: 'Успешная аутентификация через Google',
  })
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
  @ApiOperation({
    summary: 'Получение профиля текущего авторизованного пользователя',
  })
  @ApiResponse({ status: 200, description: 'Данные текущего пользователя' })
  @ApiResponse({ status: 401, description: 'Пользователь не авторизован' })
  getProfile(@CurrentUser() user: AuthenticatedUser) {
    return user;
  }
}

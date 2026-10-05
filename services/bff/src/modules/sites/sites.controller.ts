import {
  Body,
  Controller,
  Get,
  HttpCode,
  HttpStatus,
  Param,
  Post,
  UseGuards,
} from '@nestjs/common';
import {
  ApiBearerAuth,
  ApiOperation,
  ApiResponse,
  ApiTags,
} from '@nestjs/swagger';
import { SitesService } from './services/sites.service.js';
import {
  CreateSiteDto,
  CreateSiteResponseDto,
  SiteResponseDto,
  VerifySiteResponseDto,
  PingRecordDto,
} from './dto/index.js';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard.js';
import { CurrentUser } from '../auth/decorators/current-user.decorator.js';
import { RawToken } from '../auth/decorators/raw-token.decorator.js';
import type { AuthenticatedUser } from '../auth/strategies/jwt.strategy.js';

@ApiTags('Sites')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('sites')
export class SitesController {
  constructor(private readonly sitesService: SitesService) {}

  @Post()
  @HttpCode(HttpStatus.CREATED)
  @ApiOperation({ summary: 'Регистрация нового сайта для мониторинга' })
  @ApiResponse({
    status: 201,
    type: CreateSiteResponseDto,
    description: 'Сайт успешно зарегистрирован',
  })
  @ApiResponse({
    status: 400,
    description: 'Невалидный URL или ошибка DNS-резолвинга',
  })
  @ApiResponse({ status: 401, description: 'Пользователь не авторизован' })
  @ApiResponse({
    status: 403,
    description: 'Запрещено: IP является приватным или заблокирован',
  })
  async createSite(
    @CurrentUser() user: AuthenticatedUser,
    @RawToken() rawToken: string,
    @Body() dto: CreateSiteDto,
  ) {
    return await this.sitesService.createSite(user.id, dto.site, rawToken);
  }

  @Get()
  @HttpCode(HttpStatus.OK)
  @ApiOperation({
    summary: 'Получить список отслеживаемых сайтов текущего пользователя',
  })
  @ApiResponse({
    status: 200,
    type: [SiteResponseDto],
    description: 'Список сайтов пользователя',
  })
  @ApiResponse({ status: 401, description: 'Пользователь не авторизован' })
  async getAllSites(
    @CurrentUser() user: AuthenticatedUser,
    @RawToken() rawToken: string,
  ) {
    return await this.sitesService.getAllSites(user.id, rawToken);
  }

  @Post(':id/verify')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({
    summary: 'Подтвердить владение сайтом через HTTP-01 Challenge',
  })
  @ApiResponse({
    status: 200,
    type: VerifySiteResponseDto,
    description: 'Владение сайтом успешно подтверждено',
  })
  @ApiResponse({
    status: 400,
    description: 'Токен не совпадает или некорректный ответ сайта',
  })
  @ApiResponse({ status: 401, description: 'Пользователь не авторизован' })
  @ApiResponse({ status: 404, description: 'Сайт не найден' })
  @ApiResponse({ status: 502, description: 'Ошибка связи с целевым сайтом' })
  async verifySite(@Param('id') id: string, @RawToken() rawToken: string) {
    return await this.sitesService.verifySite(id, rawToken);
  }

  @Get(':id/pings')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'История замеров доступности сайта' })
  @ApiResponse({
    status: 200,
    type: [PingRecordDto],
    description: 'История замеров доступности за последние 30 дней',
  })
  @ApiResponse({ status: 401, description: 'Пользователь не авторизован' })
  @ApiResponse({ status: 404, description: 'Сайт не найден' })
  async getPings(
    @Param('id') id: string,
    @CurrentUser() user: AuthenticatedUser,
    @RawToken() rawToken: string,
  ) {
    return await this.sitesService.getPings(id, user.id, rawToken);
  }
}

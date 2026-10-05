import { z } from 'zod';
import { createZodDto } from 'nestjs-zod';

export const SiteResponseSchema = z.object({
  id: z.string().describe('Идентификатор сайта'),
  user_id: z.string().describe('Идентификатор пользователя-владельца'),
  url: z.string().describe('Отслеживаемый URL'),
  active: z.boolean().describe('Признак подтверждения и активности сайта'),
  status: z.string().describe('Текущий статус сайта в очереди'),
  created_at: z.string().describe('Время добавления сайта (UTC)'),
  status_updated_at: z.string().describe('Время обновления статуса (UTC)'),
  last_check: z.string().nullable().optional().describe('Время последней проверки (UTC)'),
  extra: z.record(z.string(), z.any()).optional().describe('Дополнительные данные последней проверки'),
});

export class SiteResponseDto extends createZodDto(SiteResponseSchema) {}

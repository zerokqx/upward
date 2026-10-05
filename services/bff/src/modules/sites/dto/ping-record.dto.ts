import { z } from 'zod';
import { createZodDto } from 'nestjs-zod';

export const PingRecordSchema = z.object({
  site_id: z.string().describe('Идентификатор сайта'),
  duration_ms: z.number().describe('Длительность ответа в миллисекундах'),
  extra: z.record(z.string(), z.any()).optional().describe('Дополнительные метаданные замера'),
});

export class PingRecordDto extends createZodDto(PingRecordSchema) {}

import { z } from 'zod';
import { createZodDto } from 'nestjs-zod';

export const VerifySiteResponseSchema = z.object({
  id: z.string().describe('Идентификатор подтвержденного сайта'),
  status: z.string().describe('Статус операции'),
});

export class VerifySiteResponseDto extends createZodDto(VerifySiteResponseSchema) {}

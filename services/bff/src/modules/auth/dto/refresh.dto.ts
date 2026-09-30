import { z } from 'zod';
import { createZodDto } from 'nestjs-zod';

export const RefreshSchema = z.object({
  refresh: z
    .uuid({ message: 'Refresh токен должен быть валидным UUID v4' })
    .describe('Refresh токен сессии (UUID v4)'),
});

export class RefreshDto extends createZodDto(RefreshSchema) {}

import { z } from 'zod';
import { createZodDto } from 'nestjs-zod';

export const RefreshSchema = z.object({
  refresh: z
    .string({ message: 'Поле refresh обязательно для заполнения' })
    .uuid('Refresh токен должен быть валидным UUID v4')
    .describe('Refresh токен сессии (UUID v4)'),
});

export class RefreshDto extends createZodDto(RefreshSchema) {}

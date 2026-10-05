import { z } from 'zod';
import { createZodDto } from 'nestjs-zod';

export const AuthResponseSchema = z.object({
  access: z.string().describe('JWT токен доступа (Bearer)'),
});

export class AuthResponseDto extends createZodDto(AuthResponseSchema) {}

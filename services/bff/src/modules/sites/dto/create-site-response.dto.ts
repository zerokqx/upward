import { z } from 'zod';
import { createZodDto } from 'nestjs-zod';

export const CreateSiteResponseSchema = z.object({
  id: z.string().describe('Идентификатор созданного сайта'),
  status: z.string().describe('Статус операции'),
  challenge_path: z.string().describe('Путь, по которому должен быть доступен токен'),
  challenge_token: z.string().describe('Секретный токен для подтверждения владения сайтом'),
});

export class CreateSiteResponseDto extends createZodDto(CreateSiteResponseSchema) {}

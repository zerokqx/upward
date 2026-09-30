import { z } from 'zod';
import { createZodDto } from 'nestjs-zod';

export const RegisterSchema = z.object({
  email: z.preprocess(
    (v) => (typeof v === 'string' ? v.trim() : v),
    z
      .email({ message: 'Некорректный формат email адреса' })
      .max(320, 'Email не должен превышать 320 символов')
      .describe('Email пользователя'),
  ),
  password: z
    .string({ message: 'Поле password обязательно для заполнения' })
    .min(8, 'Пароль должен содержать как минимум 8 символов')
    .max(128, 'Пароль не должен превышать 128 символов')
    .describe('Пароль учетной записи (от 8 до 128 символов)'),
});

export class RegisterDto extends createZodDto(RegisterSchema) {}

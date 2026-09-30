import { z } from 'zod';
import { createZodDto } from 'nestjs-zod';

export const LoginSchema = z.object({
  email: z
    .string({ message: 'Поле email обязательно для заполнения' })
    .trim()
    .email('Некорректный формат email адреса')
    .max(320, 'Email не должен превышать 320 символов')
    .describe('Email пользователя'),
  password: z
    .string({ message: 'Поле password обязательно для заполнения' })
    .min(8, 'Пароль должен содержать как минимум 8 символов')
    .max(128, 'Пароль не должен превышать 128 символов')
    .describe('Пароль пользователя'),
});

export class LoginDto extends createZodDto(LoginSchema) {}

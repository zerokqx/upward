import { ApiProperty } from '@nestjs/swagger';
import { IsEmail, IsString, MaxLength, MinLength } from 'class-validator';

export class RegisterDto {
  @ApiProperty({
    example: 'user@example.com',
    description: 'Адрес электронной почты пользователя',
    maxLength: 320,
  })
  @IsEmail({}, { message: 'Некорректный формат адреса электронной почты' })
  @MaxLength(320, { message: 'Длина email не должна превышать 320 символов' })
  email!: string;

  @ApiProperty({
    example: 'strongpassword123',
    description: 'Пароль учетной записи',
    minLength: 8,
    maxLength: 128,
  })
  @IsString({ message: 'Пароль должен быть строкой' })
  @MinLength(8, { message: 'Пароль должен содержать не менее 8 символов' })
  @MaxLength(128, { message: 'Пароль не должен превышать 128 символов' })
  password!: string;
}

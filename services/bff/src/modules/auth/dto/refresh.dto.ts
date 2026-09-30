import { ApiProperty } from '@nestjs/swagger';
import { IsNotEmpty, IsString, IsUUID } from 'class-validator';

export class RefreshDto {
  @ApiProperty({
    example: '1024ad10-4b6d-490c-a55d-ed70dcbe4f84',
    description: 'Одноразовый Refresh токен для ротации',
  })
  @IsString({ message: 'Refresh токен должен быть строкой' })
  @IsNotEmpty({ message: 'Refresh токен не может быть пустым' })
  @IsUUID('4', { message: 'Refresh токен должен быть корректным UUIDv4' })
  refresh!: string;
}

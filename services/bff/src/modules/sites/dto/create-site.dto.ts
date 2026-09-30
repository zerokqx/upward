import { ApiProperty } from '@nestjs/swagger';
import { IsNotEmpty, IsString, IsUrl, MaxLength } from 'class-validator';
import { Transform } from 'class-transformer';

export class CreateSiteDto {
  @ApiProperty({
    description: 'URL сайта для проверки (поддерживаются протоколы http:// и https://)',
    example: 'https://example.com',
    minLength: 1,
    maxLength: 2048,
  })
  @Transform(({ value, obj }) => (typeof value === 'string' ? value : typeof obj?.url === 'string' ? obj.url : value)?.trim())
  @IsNotEmpty({ message: 'Поле site (URL сайта) обязательно для заполнения' })
  @IsString({ message: 'URL сайта должен быть строкой' })
  @IsUrl(
    { require_tld: false, protocols: ['http', 'https'], require_protocol: true },
    { message: 'Некорректный формат URL. Поддерживаются только протоколы http:// и https://' },
  )
  @MaxLength(2048, { message: 'Длина URL сайта не должна превышать 2048 символов' })
  site!: string;
}

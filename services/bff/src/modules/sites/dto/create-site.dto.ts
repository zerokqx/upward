import { z } from 'zod';
import { createZodDto } from 'nestjs-zod';

export const CreateSiteSchema = z.preprocess(
  (val) => {
    if (val && typeof val === 'object' && !('site' in val) && 'url' in val) {
      return { ...val, site: (val as { url: unknown }).url };
    }
    return val;
  },
  z.object({
    site: z
      .url({
        message:
          'Некорректный формат URL. Поддерживаются только протоколы http:// и https://',
      })
      .max(2048, 'Длина URL сайта не должна превышать 2048 символов')
      .refine(
        (val) => val.startsWith('http://') || val.startsWith('https://'),
        {
          message:
            'Некорректный протокол URL. Поддерживаются только http:// и https://',
        },
      )
      .describe(
        'URL сайта для проверки (поддерживаются протоколы http:// и https://)',
      ),
  }),
);

export class CreateSiteDto extends createZodDto(CreateSiteSchema) {}

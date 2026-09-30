import { Logger } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import cookieParser from 'cookie-parser';
import { ZodValidationPipe, cleanupOpenApiDoc } from 'nestjs-zod';
import { apiReference } from '@scalar/nestjs-api-reference';
import { AppModule } from './app.module.js';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.enableCors({
    origin: true,
    credentials: true,
  });

  app.use(cookieParser());

  app.useGlobalPipes(new ZodValidationPipe());

  const swaggerConfig = new DocumentBuilder()
    .setTitle('Upward BFF API')
    .setDescription(
      'Backend-For-Frontend API для веб- и мобильных клиентов Upward: единая точка входа для авторизации и мониторинга сайтов',
    )
    .setVersion('0.1.0')
    .addBearerAuth()
    .build();

  const document = SwaggerModule.createDocument(app, swaggerConfig);
  cleanupOpenApiDoc(document);
  SwaggerModule.setup('docs', app, document);

  app.use(
    '/reference',
    apiReference({
      spec: {
        content: document,
      },
      pageTitle: 'Upward BFF API Reference',
      theme: 'purple',
    }),
  );

  const port = process.env.PORT ?? 4000;
  await app.listen(port);
  Logger.log(
    `Upward BFF service is running on http://127.0.0.1:${port}`,
    'Bootstrap',
  );
  Logger.log(
    `Swagger documentation available at http://127.0.0.1:${port}/docs`,
    'Bootstrap',
  );
  Logger.log(
    `Scalar API Reference available at http://127.0.0.1:${port}/reference`,
    'Bootstrap',
  );
}

await bootstrap();

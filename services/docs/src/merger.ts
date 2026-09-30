export interface OpenApiDoc {
  openapi: string;
  info: {
    title: string;
    version: string;
    description?: string;
  };
  servers?: Array<{ url: string; description?: string }>;
  tags?: Array<{ name: string; description?: string }>;
  paths: Record<string, any>;
  components?: {
    schemas?: Record<string, any>;
    securitySchemes?: Record<string, any>;
  };
}

export function mergeOpenApiSpecs(
  specs: Array<{ prefix: string; name: string; doc: OpenApiDoc }>,
): OpenApiDoc {
  const combined: OpenApiDoc = {
    openapi: '3.0.3',
    info: {
      title: 'Upward Platform API (All Services)',
      version: '0.1.0',
      description:
        '# Единая документация Upward\n\nОбъединенный API-справочник всех сервисов монорепозитория Upward:\n- **BFF (Backend-For-Frontend)**: клиентский API-шлюз\n- **Uptime Service**: ядро системы мониторинга и сбор метрик\n- **Identify Service**: аутентификация и выпуск токенов',
    },
    servers: [
      { url: 'http://localhost:4000', description: 'BFF Gateway' },
      { url: 'http://localhost:3000', description: 'Uptime Core Service' },
      { url: 'http://localhost:3001', description: 'Identify Auth Service' },
    ],
    tags: [],
    paths: {},
    components: {
      schemas: {},
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT',
          description: 'Access token (RS256 JWT)',
        },
      },
    },
  };

  for (const { prefix, name, doc } of specs) {
    const prefixTag = `[${prefix}]`;

    if (doc.tags) {
      for (const tag of doc.tags) {
        combined.tags!.push({
          name: `${prefixTag} ${tag.name}`,
          description: tag.description ? `(${name}) ${tag.description}` : name,
        });
      }
    }

    if (doc.components?.schemas) {
      for (const [key, schema] of Object.entries(doc.components.schemas)) {
        const schemaKey = combined.components!.schemas![key]
          ? `${prefix}_${key}`
          : key;
        combined.components!.schemas![schemaKey] = schema;
      }
    }

    if (doc.paths) {
      for (const [pathKey, pathItem] of Object.entries(doc.paths)) {
        const newPathItem: Record<string, any> = { ...pathItem };
        for (const method of ['get', 'post', 'put', 'delete', 'patch']) {
          if (newPathItem[method]) {
            const op = { ...newPathItem[method] };
            op.tags =
              op.tags && op.tags.length > 0
                ? op.tags.map((t: string) => `${prefixTag} ${t}`)
                : [`${prefixTag} General`];
            newPathItem[method] = op;
          }
        }

        const combinedPathKey = combined.paths[pathKey]
          ? `/${prefix.toLowerCase()}${pathKey}`
          : pathKey;
        combined.paths[combinedPathKey] = newPathItem;
      }
    }
  }

  return combined;
}

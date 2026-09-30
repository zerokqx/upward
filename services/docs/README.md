# Upward Developer Documentation Portal (`services/docs`)

Легковесный микросервис портала разработчика на **Fastify** и **Swagger UI**.
Предоставляет доступ ко всем спецификациям микросервисов монорепозитория Upward через единый веб-интерфейс с интерактивным тестированием API.

## Возможности

- **Экстремальная легковесность**: Fastify стартует за 20 мс, потребляет менее 30 МБ памяти, без тяжеловесного NestJS.
- **Нативный селектор сервисов**: выпадающий список (dropdown) Swagger UI для моментального переключения между микросервисами без перезагрузки страницы.
- **Отказоустойчивость**: пытается загружать актуальные спецификации с живых микросервисов, а при их недоступности мгновенно переключается на встроенные оффлайн-схемы.
- **Без лишней сложности**: схемы не мутируются и не склеиваются костылями — каждый сервис сохраняет свои оригинальные пути, серверы и модели.

## Эндпоинты

- **`http://localhost:5000/`** — Главный портал Swagger UI с переключателем сервисов:
  - `BFF (Client Gateway)`
  - `Uptime (Monitoring Core)`
  - `Identify (Auth Service)`
- **`http://localhost:5000/bff`** — Быстрый переход к документации BFF
- **`http://localhost:5000/uptime`** — Быстрый переход к документации Uptime
- **`http://localhost:5000/identify`** — Быстрый переход к документации Identify
- **`http://localhost:5000/specs/bff.json`** — OpenAPI 3.0 спецификация BFF
- **`http://localhost:5000/specs/uptime.json`** — OpenAPI 3.0 спецификация Uptime
- **`http://localhost:5000/specs/identify.json`** — OpenAPI 3.0 спецификация Identify
- **`http://localhost:5000/health`** — Проверка работоспособности

## Запуск через Moonrepo

```bash
moon run docs:dev    # Режим разработки
moon run docs:build  # Сборка TypeScript
moon run docs:test   # Запуск тестов
moon run docs:lint   # Линтер oxlint
moon run docs:start  # Запуск собранного сервиса
```

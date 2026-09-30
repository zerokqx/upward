# Upward Developer Documentation Portal (`services/docs`)

Легковесный микросервис портала разработчика на **Fastify** и **Swagger UI**.
Объединяет спецификации всех сервисов монорепозитория Upward в единый удобный интерфейс с интерактивным тестированием API.

## Возможности

- **Экстремальная легковесность**: Fastify стартует за 20 мс, потребляет менее 30 МБ памяти, без тяжеловесного NestJS.
- **Единый портал (Multi-Spec)**: удобный селектор сервисов прямо в интерфейсе Swagger UI (dropdown выбора спецификации).
- **Отказоустойчивость**: пытается загружать актуальные спецификации с живых микросервисов, а при их недоступности мгновенно переключается на встроенные оффлайн-схемы.
- **Объединенный API**: генерирует объединенную спецификацию `combined.json` со всеми эндпоинтами монорепозитория.

## Эндпоинты

- **`http://localhost:5000/`** — Главный портал со списком всех сервисов:
  - `1. Combined Platform API (All Services)`
  - `2. BFF (Client Gateway)`
  - `3. Uptime Service (Core)`
  - `4. Identify Service (Auth)`
- **`http://localhost:5000/bff/`** — Документация BFF
- **`http://localhost:5000/uptime/`** — Документация Uptime
- **`http://localhost:5000/identify/`** — Документация Identify
- **`http://localhost:5000/specs/combined.json`** — Объединенная OpenAPI 3.0 спецификация
- **`http://localhost:5000/specs/bff.json`** — Спецификация BFF
- **`http://localhost:5000/specs/uptime.json`** — Спецификация Uptime
- **`http://localhost:5000/specs/identify.json`** — Спецификация Identify
- **`http://localhost:5000/health`** — Проверка работоспособности

## Запуск через Moonrepo

```bash
moon run docs:dev    # Режим разработки
moon run docs:build  # Сборка TypeScript
moon run docs:test   # Запуск тестов
moon run docs:lint   # Линтер oxlint
moon run docs:start  # Запуск собранного сервиса
```

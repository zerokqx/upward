# Руководство для AI-агентов и разработчиков (AGENTS.md)

В этом документе описаны правила работы с монорепозиторием **Upward**, принципы управления задачами через **Moonrepo**, а также пошаговое руководство по созданию и применению миграций базы данных.

---

## 1. Обзор проекта и окружения

**Upward** — это полиглот-монорепозиторий распределённой системы мониторинга доступности сервисов:
- **`services/uptime`** (Rust / Axum / Tokio / SQLx / TimescaleDB) — сервис мониторинга доступности сайтов и сохранения метрик.
- **`services/bff`** (NestJS / TypeScript / pnpm) — Backend-for-Frontend для клиентов.
- **`services/identify`** (OCaml / Dune / RabbitMQ) — сервис идентификации и аутентификации.

### Окружение (Nix / Devenv / Direnv)
Все зависимости (Rust toolchain, Node.js, pnpm, OCaml/Dune, Moonrepo, SQLx CLI) изолированы и управляются декларативно через `devenv.nix`.
- При включенном `direnv` переменные и пути к утилитам подгружаются автоматически при входе в терминал.
- При явном вызове утилит без direnv бинарники доступны через профиль:
  - `moon`: доступен глобально либо в `.devenv/profile/bin/moon`
  - `sqlx`: `.devenv/profile/bin/sqlx`
  - `cargo`, `pnpm`, `node`: также в профиле devenv.

> [!WARNING]
> Интерактивный вызов `devenv shell` ожидает ввода в stdin. В скриптах и агентных сценариях используйте прямые команды (когда активен direnv) либо `devenv shell <command>` без зависания в subshell.

---

## 2. Использование Moonrepo (`moon`)

**Moonrepo (`moon`)** — оркестратор задач и сборщик воркспейса. Он берет на себя запуск линтеров, сборки, тестов, миграций и поднятие инфраструктуры с кэшированием результатов.

### 2.1. Основные команды

| Команда | Описание |
| :--- | :--- |
| `moon query projects` | Вывести список всех зарегистрированных проектов воркспейса. |
| `moon project <project>` | Показать детальную информацию о проекте: файловые группы, задачи, зависимости (например: `moon project uptime`). |
| `moon run <project>:<task>` | Запустить конкретную задачу проекта (например: `moon run uptime:check`). |
| `moon check --all` | Запустить проверку всех сервисов в монорепозитории. |
| `moon run <task> -- --clean` | Запустить задачу с принудительным игнорированием кэша moon. |

---

### 2.2. Задачи сервиса `uptime`

Конфигурация задач сервиса описана в [services/uptime/moon.yml](file:///home/zerok/projects/upward/services/uptime/moon.yml):

```bash
# 1. Поднять локальную инфраструктуру (TimescaleDB / Postgres в Docker)
moon run uptime:compose-infra-up

# 2. Применить миграции базы данных
moon run uptime:migrate

# 3. Быстрая проверка компиляции (cargo check)
moon run uptime:check

# 4. Проверка линтером clippy
moon run uptime:lint

# 5. Проверка форматирования кода (rustfmt)
moon run uptime:format

# 6. Запуск тестов
moon run uptime:test

# 7. Полная сборка бинарника
moon run uptime:build

# 8. Запуск сервиса
moon run uptime:run
```

---

## 3. Работа с базой данных и миграциями (SQLx)

Сервис `uptime` использует **PostgreSQL** с расширением **TimescaleDB** и асинхронный драйвер **SQLx**.
Все миграции хранятся в директории:
📁 [services/uptime/migrations/](file:///home/zerok/projects/upward/services/uptime/migrations/)

Параметры подключения задаются в [services/uptime/.env](file:///home/zerok/projects/upward/services/uptime/.env):
```env
DATABASE_URL=postgres://myuser:mypassword@127.0.0.1:5432/uptimedb
```

---

### 3.1. Как создать новую миграцию

Проект использует **простые (simple/up-only)** миграции с временной меткой в формате `YYYYMMDDHHMMSS_<name>.sql`.

#### Вариант А: Через `sqlx-cli` из корня репозитория (Рекомендуется)
```bash
.devenv/profile/bin/sqlx migrate add --simple <migration_name> --source services/uptime/migrations
```

#### Вариант Б: Через `sqlx-cli` из директории сервиса
```bash
cd services/uptime
sqlx migrate add --simple <migration_name>
```

**Пример:**
```bash
.devenv/profile/bin/sqlx migrate add --simple create_forbidden_ip_table --source services/uptime/migrations
```
Команда создаст файл вида:
`services/uptime/migrations/20260914100658_create_forbidden_ip_table.sql`.

---

### 3.2. Правила оформления SQL-миграций

1. **Идемпотентность:** всегда используйте `IF NOT EXISTS` и `IF EXISTS`:
   ```sql
   CREATE TABLE IF NOT EXISTS my_table ( ... );
   CREATE INDEX IF NOT EXISTS idx_my_table_field ON my_table (field);
   ALTER TABLE my_table ADD COLUMN IF NOT EXISTS field TEXT;
   ```

2. **Первичные ключи и таймштампы:**
   - Первичный ключ: `id BIGSERIAL PRIMARY KEY`.
   - Время создания: `created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`.

3. **Индексация:**
   - Добавляйте индексы на поля, по которым выполняется частый поиск, фильтрация или джойны.
   - Для уникальных сущностей используйте `CREATE UNIQUE INDEX IF NOT EXISTS`.

4. **Типы данных:**
   - Для гибких строк (URL, хосты, IP-адреса, домены) используйте `TEXT` — это исключает падения при вставке невалидных строковых форматов, в отличие от строгого `INET`.
   - Для перечислений и коротких статусов используйте `VARCHAR(20)`.

---

### 3.3. Как применить миграции

После добавления или изменения SQL-файла примените миграции через moon:
```bash
moon run uptime:migrate
```

Moon выполнит команду `sqlx migrate run` с учётом переменных из `.env` сервиса.

---

### 3.4. Как проверить статус миграций

1. **Через SQLx:**
   ```bash
   .devenv/profile/bin/sqlx migrate info --source services/uptime/migrations
   ```

2. **Напрямую в контейнере TimescaleDB:**
   ```bash
   docker exec -i uptime-timescale psql -U myuser -d uptimedb -c "SELECT version, description, installed_on, success FROM _sqlx_migrations ORDER BY version DESC;"
   ```

---

## 4. Памятка для агентов при выполнении задач

1. **Соблюдайте архитектуру слоёв:**
   В `services/uptime` принята модульная структура по аналогии с NestJS:
   - `domain.rs` — чистые структуры данных и типы ошибок (`thiserror`).
   - `infrastructure.rs` — сетевые клиенты, работа с внешними протоколами.
   - `repository.rs` — взаимодействие с базой через SQLx.
   - `controller.rs` — HTTP-хэндлеры и валидация DTO.
   - `mod.rs` — экспорт и маршрутизация модуля.

2. **Всегда проверяйте компиляцию и миграции перед завершением:**
   ```bash
   moon run uptime:migrate
   moon run uptime:check
   ```

3. **Сохраняйте документацию и комментарии:**
   Не удаляйте существующие комментарии и контекстные заметки (например, [ARCHITECTURE_NOTES.md](file:///home/zerok/projects/upward/services/uptime/ARCHITECTURE_NOTES.md)).

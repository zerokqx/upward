# Архитектурный конспект и статус проекта (Uptime & Identify)
*Дата сохранения: 11 сентября 2026 г.*

---

## 1. Текущий статус сервиса Uptime (Rust)

### Что уже сделано:
1. **Слой Domain (`src/site/domain.rs`):**
   - Модель `Site` очищена от сетевой логики и стала чистой структурой данных:
     - `pub id: Option<i64>`
     - `pub user_id: UserId` (Newtype паттерн для типобезопасности)
     - `pub url: String`
   - Добавлены конструкторы `Site::new(url, user_id)` и `Site::with_id(id, url, user_id)`.
   - Исправлена опечатка `ping_duratation` -> `ping_duration`.
   - Ошибки типизированы через `thiserror` (`SiteError`).

2. **Слой Infrastructure (`src/site/infrastructure.rs`):**
   - Сетевой I/O вынесен в структуру `SitePinger`.
   - Конструктор `SitePinger::new(client: &reqwest::Client)` принимает ссылку на клиента и клонирует его дескриптор (`Arc`). Это не дублирует сетевые ресурсы/пул сокетов и позволяет безопасно передавать структуру в async-задачи без привязки к временам жизни (`'static`).
   - Метод `ping(&self, site: &Site)` выполняет замер времени и запрос к целевому сайту.

3. **База данных и миграции (`migrations/`):**
   - Создана и успешно применена миграция `20260911171211_add_last_check_to_sites.sql`:
     ```sql
     ALTER TABLE sites
     ADD COLUMN IF NOT EXISTS last_check TIMESTAMPTZ;

     CREATE INDEX IF NOT EXISTS idx_sites_last_check ON sites (last_check ASC NULLS FIRST);
     ```
   - Индекс `ASC NULLS FIRST` гарантирует быстрый поиск сайтов, которые пора проверить.

---

## 2. Ключевые архитектурные инсайты: Конкурентность и БД

### А. Семафор (Ограничение параллельности запросов)
- **Проблема:** Если запустить 1000 HTTP-запросов одновременно, ОС исчерпает лимиты сокетов/дескрипторов (ulimit), а DNS-сервер начнет дропать пакеты.
- **Решение:** `tokio::sync::Semaphore` (например, на 50 разрешений). Он пропускает в сеть не более 50 одновременных запросов, передавая освободившийся "пропуск" следующему сайту.

### Б. Пакетная вставка (Batch Insert)
- **Проблема:** 1000 одиночных `INSERT INTO site_pings ...` — это 1000 сетевых round-trips к Postgres, которые забьют пул соединений (`max_connections = 5`).
- **Решение:** Формирование одного SQL-запроса через запятую (Batch INSERT) на весь батч:
  ```sql
  INSERT INTO site_pings (time, site_id, duration_ms, extra)
  VALUES (NOW(), 1, 120, '...'), (NOW(), 2, 45, '...'), ...;
  ```

### В. Мультиинстансы и состояние гонки (Race Conditions)
- **Проблема:** Если запущено 2+ реплики сервиса, обычный `SELECT ... LIMIT 500` вернет **одни и те же сайты** обоим инстансам.
- **Решение:** `FOR UPDATE SKIP LOCKED`. Второй инстанс автоматически пропускает строки, занятые первым инстансом.
- **Нюанс зазора по времени:** Если сначала сделать `SELECT ... FOR UPDATE`, а потом отдельный `UPDATE`, между ними возникает временной зазор, в который может вклиниться другой инстанс.
- **Атомарный захват батча (Решение в 1 запрос):**
  ```sql
  WITH target_sites AS (
      SELECT id
      FROM sites
      WHERE last_check IS NULL OR last_check < NOW() - INTERVAL '60 seconds'
      ORDER BY last_check ASC NULLS FIRST
      LIMIT $1
      FOR UPDATE SKIP LOCKED
  )
  UPDATE sites s
  SET last_check = NOW()
  FROM target_sites ts
  WHERE s.id = ts.id
  RETURNING s.id, s.url;
  ```
  Транзакция длится **1–2 миллисекунды**, после чего соединение возвращается в пул базы данных, а воркер спокойно пингует сайты.

### Г. Защита от зависаний (Что если пинг длится долго?)
1. **Обязательный таймаут HTTP:** В `reqwest::Client` жестко задается `.timeout(Duration::from_secs(10))`. Ни один сайт не может отвечать дольше 10 секунд.
2. **Статусная модель (State Machine):**
   - Колонка `status` (`'idle'` | `'processing'`).
   - При захвате: `status = 'processing'`.
   - После пинга: `status = 'idle', last_check = NOW()`.
   - Защита от падения воркера: `WHERE status = 'idle' OR (status = 'processing' AND last_check < NOW() - INTERVAL '5 minutes')`.

---

## 3. Архитектура Axum по стандарту NestJS

Чтобы избавиться от хаоса и получить строгую структуру (как в NestJS):

```text
services/uptime/src/site/
├── mod.rs          <-- Аналог site.module.ts (собирает Router<AppState>)
├── controller.rs   <-- Аналог site.controller.ts (HTTP-хэндлеры, валидация DTO)
├── service.rs      <-- Аналог site.service.ts (бизнес-логика, координация)
├── repository.rs   <-- Аналог site.repository.ts (SQLx запросы в Postgres)
├── domain.rs       <-- Аналог entities/ (Site, PingResponse, UserId)
└── dto.rs          <-- Аналог dto/ (CreateSiteDto, UpdateSiteDto)
```

В `main.rs` модули подключаются как в `app.module.ts`:
```rust
let app = Router::new()
    .nest("/api/sites", site::routes())
    .with_state(app_state);
```

---

## 4. Статус сервиса Identify (Haskell & Neovim LSP)

### Что было исправлено:
1. В `services/identify/app/Main.hs` удалено забытое ключевое слово `data` на 4-й строке, из-за которого компилятор падал с синтаксической ошибкой.
2. В корне проекта `upward/` создан файл `cabal.project`:
   ```cabal
   packages:
     services/identify
   ```
   Благодаря этому HLS распознает монорепозиторий и переключается с аварийного `Default` на `Cabal` cradle.
3. Проверено: `cabal build` и запуск `haskell-language-server-wrapper` в консоли завершаются с **кодом 0**.

### Причина ошибки в Neovim (`haskell-tools.nvim quit with code 1`):
В конфиге Nixvim (`/home/zerok/projects/ZNix/home/zerokqx/nixvim/languages.nix`):
- В `extraPackages` прописан `haskell-language-server`, но нет `ghc`.
- Nixvim принудительно ставит свой системный HLS в начало `$PATH` Neovim.
- При открытии проекта HLS видит GHC из `devenv`, их ABI-хеши расходятся:
  `GHC ABIs don't match! Expected: ... Got: ...`
- **Решение:** Убрать `haskell-language-server` из `extraPackages` в `languages.nix` Nixvim, чтобы Neovim подхватывал согласованную пару `ghc` + `hls` из `devenv.nix`.

---

## 5. План работы на завтра

- [ ] **Шаг 1 (Uptime - Repository):** Добавить в `SiteRepository` метод `fetch_sites_to_check(limit)` (через атомарный CTE запрос) и `save_pings_batch(results)`.
- [ ] **Шаг 2 (Uptime - Cron Worker):** Написать фоновую задачу в `main.rs` (или отдельном воркере): цикл по таймеру -> выборка батча -> параллельный пинг через `Semaphore(50)` -> сохранение батча в базу.
- [ ] **Шаг 3 (Uptime - Рефакторинг слоёв):** Разложить `src/site` по схеме NestJS (`controller.rs`, `service.rs`, `dto.rs`).
- [ ] **Шаг 4 (Identify - Haskell):** Закомментировать `haskell-language-server` в Nixvim `languages.nix` и вернуть в `upward/devenv.nix`, чтобы LSP в Neovim заработал стабильно.

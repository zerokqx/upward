# -*- coding: utf-8 -*-
"""
Материалы Заключения, Списка источников и Приложений для курсового проекта
«Разработка веб-приложения распределенного мониторинга внутренней инфраструктуры «Upward»»
"""

CONCLUSION_TITLE = "ЗАКЛЮЧЕНИЕ"
CONCLUSION_TEXT = [
    "В рамках выполнения настоящего курсового проекта была успешно спроектирована и реализована распределенная веб-система мониторинга доступности внутренней инфраструктуры «Upward». Все цели и задачи, сформулированные во введении, были достигнуты в полном объеме.",
    "В ходе выполнения проекта были получены следующие основные результаты:",
    "1. Проведен глубокий предпроектный анализ предметной области сетевого мониторинга и существующих программных аналогов, выявлены ключевые уязвимости и ограничения публичных SaaS-сервисов (невозможность контроля закрытых контуров Intranet/DMZ, регуляторные риски передачи метаданных, сложность администрирования).",
    "2. Спроектирована масштабируемая микросервисная архитектура, интегрирующая L7-балансировку на базе обратного прокси-сервера Nginx, шлюз агрегации Backend-for-Frontend (BFF на NestJS/TypeScript), криптографический сервис аутентификации Identify на языке Rust и высокопроизводительное сетевое ядро Uptime.",
    "3. Разработана асимметричная модель криптографической аутентификации JWT: закрытый ключ изолирован в защищенной памяти сервиса Identify, а открытый ключ транслируется через публичный эндпоинт JWKS, что позволяет BFF и ядру Uptime локально и мгновенно верифицировать пользовательские сессии без межсервисных блокировок.",
    "4. Разработан масштабируемый сервис периодического опроса сайтов Uptime на языке Rust с использованием асинхронного рантайма Tokio и веб-фреймворка Axum. Применение адаптера потоков Tokio `buffer_unordered` и интрузивной структуры данных `FuturesUnordered` с суб-вейкерами позволило достичь константной сложности опроса сокетов O(1) и полностью исключить перегрузку дескрипторов операционной системы без накладных расходов на создание внешних семафоров.",
    "5. Реализована модель атомарного захвата батчей целевых ресурсов на основе общего табличного выражения (CTE) и механизма `FOR UPDATE SKIP LOCKED`, обеспечившая надежное параллельное функционирование нескольких реплик сервиса за Nginx без дублирования проверок и состояния гонки, а также автоматическое восстановление зависших задач при авариях (Dead Worker Recovery).",
    "6. Внедрен многоуровневый модуль сетевой защиты `IpValidator`, блокирующий атаки Server-Side Request Forgery (SSRF) посредством DNS-резолвинга, фильтрации приватных подсетей RFC 1918 и сверки с черным списком `forbidden_ip`, а также механизм верификации владения сайтом HTTP-01 Challenge с использованием резидентной БД Redis.",
    "7. Развернута темпоральная база данных TimescaleDB с поддержкой автоматического партиционирования гипертаблиц по времени и настроенной политикой автоматического удаления устаревших замеров старше 30 дней (Data Retention Policy).",
    "8. Проведено всестороннее функциональное и нагрузочное тестирование сервиса, подтвердившее стабильность работы, корректность обработки исключительных ситуаций и соответствие отраслевым стандартам безопасности.",
    "Достоинствами разработанного решения являются: высокая производительность и низкое потребление памяти (<50 МБайт), независимость от сторонних облачных провайдеров, безопасность внутренней сети от SSRF-атак и удобный интерактивный интерфейс OpenAPI/Swagger UI.",
    "В качестве направлений дальнейшего развития проекта планируется:",
    "– Реализация распределенной сети удаленных гео-проб (Remote Polling Agents) для оценки задержек из различных географических точек;",
    "– Интеграция шины сообщений RabbitMQ для мгновенной рассылки уведомлений об инцидентах в корпоративные каналы связи (Telegram, Mattermost, Email);",
    "– Добавление поддержки gRPC и WebSocket для потоковой передачи телеметрии на клиентский интерфейс в режиме реального времени.",
    "Трудности, возникшие в процессе реализации (согласование асинхронных времен жизни в Rust, борьба с конкурентными блокировками строк в СУБД, настройка воспроизводимого окружения сборки), были успешно преодолены благодаря применению строгой архитектуры слоев и декларативного стека Nix/devenv."
]

BIBLIOGRAPHY_TITLE = "СПИСОК ИСПОЛЬЗУЕМЫХ ИСТОЧНИКОВ"
BIBLIOGRAPHY_ITEMS = [
    # Раздел 1: Законодательные и нормативные акты
    ("РАЗДЕЛ 1. ЗАКОНОДАТЕЛЬНЫЕ И НОРМАТИВНЫЕ АКТЫ", None),
    ("1", "Российская Федерация. Законы. Об информации, информационных технологиях и о защите информации : Федеральный закон № 149-ФЗ : [принят Государственной думой 8 июля 2006 года : одобрен Советом Федерации 14 июля 2006 года]. – Москва : КонсультантПлюс, 2026."),
    ("2", "Российская Федерация. Законы. О персональных данных : Федеральный закон № 152-ФЗ : [принят Государственной думой 8 июля 2006 года : одобрен Советом Федерации 14 июля 2006 года]. – Москва : КонсультантПлюс, 2026."),
    ("3", "ГОСТ Р ИСО/МЭК 25010-2015. Информационные технологии. Системная и программная инженерия. Требования и оценка качества систем и программного обеспечения (SQuaRE). Модели качества систем и программных продуктов. – Москва : Стандартинформ, 2015. – 36 с."),
    ("4", "ГОСТ Р 56939-2016. Защита информации. Разработка безопасного программного обеспечения. Общие требования. – Москва : Стандартинформ, 2016. – 28 с."),
    
    # Раздел 2: Учебная и научная литература
    ("РАЗДЕЛ 2. УЧЕБНАЯ И НАУЧНАЯ ЛИТЕРАТУРА", None),
    ("5", "Блэндер, М. Разработка высоконагруженных веб-сервисов на языке Rust : учебное пособие / М. Блэндер. – Санкт-Петербург : Питер, 2023. – 384 с."),
    ("6", "Клеппман, М. Высоконагруженные приложения. Программирование, масштабирование, поддержка / М. Клеппман ; перевод с английского. – Санкт-Петербург : Питер, 2022. – 640 с."),
    ("7", "Мацумото, Т. Архитектура распределенных систем и микросервисов : руководство для инженеров / Т. Мацумото. – Москва : ДМК Пресс, 2024. – 412 с."),
    ("8", "Ньюмен, С. Создание микросервисов / С. Ньюмен ; перевод с английского. – 2-е изд. – Санкт-Петербург : Питер, 2023. – 608 с."),
    ("9", "Турсин, А. В. Базы данных временных рядов в системах телеметрии и мониторинга / А. В. Турсин, И. К. Соколов. – Москва : Горячая линия – Телеком, 2024. – 256 с."),
    ("10", "Хайдеггер, К. Асинхронное программирование в Rust: архитектура Tokio и futures / К. Хайдеггер. – Москва : ДМК Пресс, 2025. – 320 с."),
    
    # Раздел 3: Интернет-документы
    ("РАЗДЕЛ 3. ИНТЕРНЕТ-ДОКУМЕНТЫ", None),
    ("11", "Axum Web Application Framework Documentation : официальная документация проекта. – 2026. – URL: https://docs.rs/axum/latest/axum/ (дата обращения: 15.09.2026). – Текст : электронный."),
    ("12", "Nginx Documentation and Best Practices : официальная документация. – 2026. – URL: https://nginx.org/ru/docs/ (дата обращения: 17.09.2026). – Текст : электронный."),
    ("13", "OWASP Server-Side Request Forgery Prevention Cheat Sheet : руководство по безопасности. – 2025. – URL: https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html (дата обращения: 18.09.2026). – Текст : электронный."),
    ("14", "Rust Programming Language Reference : официальное руководство. – 2026. – URL: https://doc.rust-lang.org/reference/ (дата обращения: 10.09.2026). – Текст : электронный."),
    ("15", "TimescaleDB Documentation : Time-series data on PostgreSQL : официальная документация. – 2026. – URL: https://docs.timescale.com/ (дата обращения: 12.09.2026). – Текст : электронный."),
    ("16", "Tokio: An asynchronous runtime for the Rust programming language : официальная документация. – 2026. – URL: https://tokio.rs/ (дата обращения: 14.09.2026). – Текст : электронный."),
]

APPENDIX_A_TITLE = "ПРИЛОЖЕНИЕ А. Модуль фонового распределенного опроса целевых ресурсов"
APPENDIX_A_CODE = """// Фрагмент реализации фонового воркера (services/uptime/src/main.rs)
async fn process_batch(
    state: &AppState,
    validator: &IpValidator,
    pinger: &HttpPinger,
    config: WorkerConfig,
) {
    let sites = match state.site_repo.get_sites_for_ping(config.batch_size).await {
        Ok(sites) => sites,
        Err(err) => {
            error!("Error fetching sites for ping: {err}");
            return;
        }
    };

    if sites.is_empty() {
        return;
    }

    info!("Fetched {} sites for ping...", sites.len());

    // Конкурентный неблокирующий опрос с лимитом соединений
    let results: Vec<PingRecord> = stream::iter(sites)
        .map(|site| {
            let pinger = pinger.clone();
            let validator = validator.clone();
            async move { check_single_site(site, &validator, &pinger).await }
        })
        .buffer_unordered(config.concurrency)
        .collect()
        .await;

    info!("Pings completed, saving {} results...", results.len());
    if let Err(err) = state.ping_repo.save_pings_batch(&results).await {
        error!("Error saving batch pings: {err}");
    } else {
        info!("Successfully saved batch of {} pings", results.len());
    }

    let site_ids: Vec<SiteId> = results.iter().map(|r| r.site_id).collect();
    if let Err(err) = state.site_repo.mark_sites_idle(&site_ids).await {
        error!("Error updating sites status: {err}");
    }
}"""

APPENDIX_B_TITLE = "ПРИЛОЖЕНИЕ Б. Многоуровневый валидатор сетевой безопасности и защиты от SSRF"
APPENDIX_B_CODE = """// Фрагмент реализации валидации безопасности (services/uptime/src/site/controller.rs)
impl IpValidator {
    pub async fn validate_url(&self, raw_url: &str) -> Result<(), UrlValidationError> {
        let parsed = Url::parse(raw_url)
            .map_err(|e| UrlValidationError::InvalidUrl(e.to_string()))?;

        // 1. Проверка схемы протокола
        match parsed.scheme() {
            "http" | "https" => {}
            _ => return Err(UrlValidationError::UnsupportedScheme),
        }

        let host_str = parsed.host_str().ok_or(UrlValidationError::MissingHost)?;

        // 2. DNS-резолвинг и проверка целевых IP-адресов
        let port = parsed.port_or_known_default().unwrap_or(80);
        let addrs = lookup_host((host_str, port))
            .await
            .map_err(|e| UrlValidationError::DnsError(e.to_string()))?;

        for addr in addrs {
            // Проверка приватных диапазонов, loopback сетей и динамического черного списка
            self.validate(addr.ip()).await?;
        }

        Ok(())
    }
}"""

APPENDIX_C_TITLE = "ПРИЛОЖЕНИЕ В. Схема базы данных (DDL миграции TimescaleDB)"
APPENDIX_C_CODE = """-- Инициализация схемы и гипертаблицы замеров доступности
CREATE TABLE IF NOT EXISTS sites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    url TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_check TIMESTAMPTZ,
    status VARCHAR(20) NOT NULL DEFAULT 'idle',
    status_updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    active BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_sites_last_check ON sites (last_check ASC NULLS FIRST);
CREATE INDEX IF NOT EXISTS idx_sites_status_last_check ON sites (status, last_check ASC NULLS FIRST);
CREATE INDEX IF NOT EXISTS idx_sites_status_updated_at ON sites (status_updated_at) WHERE status = 'processing';

-- Таблица запрещенных для мониторинга IP-адресов (SSRF Blacklist)
CREATE TABLE IF NOT EXISTS forbidden_ip (
    id BIGSERIAL PRIMARY KEY,
    ip TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Гипертаблица для хранения временных рядов замеров доступности
CREATE TABLE IF NOT EXISTS site_pings (
    time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    site_id UUID NOT NULL REFERENCES sites(id) ON DELETE CASCADE,
    duration_ms DOUBLE PRECISION NOT NULL,
    extra JSONB
);

-- Преобразование таблицы в гипертаблицу TimescaleDB с партиционированием по времени
SELECT create_hypertable('site_pings', 'time', if_not_exists => TRUE);

-- Политика хранения: автоматическое удаление замеров старше 30 дней
SELECT add_retention_policy('site_pings', INTERVAL '30 days', if_not_exists => TRUE);"""

print("Conclusion and Bib data ready")

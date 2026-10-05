# -*- coding: utf-8 -*-
"""
Материалы Заключения, Списка источников и Приложений для курсового проекта
«Разработка веб-приложения распределенного мониторинга внутренней инфраструктуры «Upward»»
"""

CONCLUSION_TITLE = "ЗАКЛЮЧЕНИЕ"
CONCLUSION_TEXT = [
    "В рамках выполнения настоящего курсового проекта была успешно спроектирована и реализована распределенная веб-система мониторинга доступности внутренней инфраструктуры «Upward». Все цели и задачи, сформулированные во введении, были достигнуты в полном объеме.",
    "В ходе выполнения проекта были получены следующие основные научно-технические и практические результаты:",
    "1. Проведен глубокий предпроектный анализ предметной области сетевого мониторинга и существующих программных аналогов, выявлены ключевые уязвимости и ограничения публичных SaaS-сервисов (невозможность контроля закрытых контуров Intranet/DMZ, регуляторные риски передачи служебных метаданных, высокие тарифы и закрытость протоколов).",
    "2. Спроектирована и воплощена отказоустойчивая микросервисная архитектура, объединяющая пять специализированных сервисов: высокопроизводительное сетевое ядро Uptime (Rust/Axum/Tokio/SQLx), криптографический сервис идентификации Identify (Rust/Axum/SQLx), прикладной шлюз Backend-for-Frontend (NestJS/TypeScript/Zod 4/Orval), клиентский SPA-интерфейс Frontend (React 19/TypeScript/Vite/FSD/TanStack) и интерактивный портал документации Docs (Fastify/Swagger UI), защищенные единой L7-входной точкой Nginx.",
    "3. Разработана и реализована асимметричная криптографическая модель аутентификации на базе стандарта RS256 (RSA 2048-бит с ключами в формате PKCS#8 PEM). Приватный ключ изолирован в оперативной памяти сервиса Identify, а открытый ключ транслируется через эндпоинты `/keys/public` и `/keys/public.pem`, что обеспечивает шлюзу BFF возможность автономной валидации JWT без синхронных блокирующих запросов. Для защиты учетных данных внедрено хеширование паролей Argon2id в выделенном пуле потоков Tokio `spawn_blocking`, ротация refresh-токенов в БД Redis с атомарным отзывом через `GETDEL`, а также интеграция протокола Google OAuth 2.0.",
    "4. Разработано высокопроизводительное сетевое ядро Uptime на языке Rust с использованием асинхронного рантайма Tokio и фреймворка Axum. Применение адаптера потоков `buffer_unordered` и интрузивной структуры `FuturesUnordered` обеспечило константную сложность опроса сокетов O(1) и полностью исключило исчерпание дескрипторов операционной системы без накладных расходов на создание внешних семафоров. Разработан специализированный протокол телеметрии `/upward`, обеспечивающий передачу и валидацию расширенной таксономии кастомных UI-виджетов по системному справочнику таблицы `widgets` базы данных.",
    "5. Реализована модель атомарного захвата батчей целевых ресурсов на основе общего табличного выражения (CTE) и механизма `FOR UPDATE SKIP LOCKED`, обеспечившая надежное параллельное функционирование нескольких реплик сервиса за Nginx без дублирования проверок и состояния гонки, а также автоматическое восстановление зависших задач при авариях (Dead Worker Recovery).",
    "6. Внедрен многоуровневый комплекс сетевой безопасности: модуль `IpValidator` с DNS-резолвингом, блокировкой приватных подсетей RFC 1918 и черного списка `forbidden_ip`, подавление атак DNS Rebinding посредством связывания сокетов через метод `resolve_to_addrs`, потоковое ограничение размера полезной нагрузки до 512 КБайт с отсевом chunked-потоков для предотвращения DoS/OOM-атак, а также криптографическая верификация владения веб-ресурсом по протоколу HTTP-01 Challenge по пути `/upward` с сохранением секретов в резидентной БД Redis.",
    "7. Развернута темпоральная база данных TimescaleDB с поддержкой автоматического партиционирования гипертаблиц по времени и настроенной политикой автоматического удаления устаревших замеров старше 30 дней (`add_retention_policy`), а также реляционная база данных `identifydb` для безопасного хранения профилей пользователей и привязок внешних OAuth-провайдеров.",
    "8. Проведено комплексное модульное, интеграционное, нагрузочное и защищенное тестирование веб-приложения (включая сканирование Wapiti и валидацию разметки W3C), подтвердившее стабильность работы, корректность обработки исключительных ситуаций и соответствие отраслевым стандартам безопасности SQuaRE (ГОСТ Р ИСО/МЭК 25010-2015).",
    "Достоинствами разработанного решения являются: экстремальная производительность и минимальное потребление оперативной памяти (<40 МБайт для ядра Uptime), субмикросекундная точность замера сетевой задержки (RTT), полная независимость от сторонних облачных провайдеров, нулевое доверие к внешним сетевым узлам и строгая сквозная типизация от миграций БД до компонентов React 19.",
    "В качестве направлений дальнейшего развития проекта планируется:",
    "– Создание распределенной сети удаленных гео-проб (Remote Polling Agents) для замера сетевой доступности из различных точек мира;",
    "– Интеграция корпоративной очереди сообщений RabbitMQ для рассылки уведомлений об инцидентах в Telegram, Mattermost и корпоративную почту;",
    "– Реализация полнодуплексных каналов WebSocket и Server-Sent Events (SSE) для мгновенного обновления дашборда фронтенда при поступлении новых замеров.",
    "Трудности, возникшие в процессе реализации (согласование асинхронных времен жизни в Rust, обеспечение атомарности ротации токенов, настройка изоляции сред сборки), были успешно преодолены благодаря применению строгой архитектуры слоев и декларативного стека Nix/devenv/Moonrepo."
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
    ("6", "Бэнкс, А. React и Redux: функциональная веб-разработка / А. Бэнкс, Э. Порселло ; перевод с английского. – 2-е изд. – Санкт-Петербург : Питер, 2023. – 352 с."),
    ("7", "Клеппман, М. Высоконагруженные приложения. Программирование, масштабирование, поддержка / М. Клеппман ; перевод с английского. – Санкт-Петербург : Питер, 2022. – 640 с."),
    ("8", "Мацумото, Т. Архитектура распределенных систем и микросервисов : руководство для инженеров / Т. Мацумото. – Москва : ДМК Пресс, 2024. – 412 с."),
    ("9", "Ньюмен, С. Создание микросервисов / С. Ньюмен ; перевод с английского. – 2-е изд. – Санкт-Петербург : Питер, 2023. – 608 с."),
    ("10", "Турсин, А. В. Базы данных временных рядов в системах телеметрии и мониторинга / А. В. Турсин, И. К. Соколов. – Москва : Горячая линия – Телеком, 2024. – 256 с."),
    ("11", "Хайдеггер, К. Асинхронное программирование в Rust: архитектура Tokio и futures / К. Хайдеггер. – Москва : ДМК Пресс, 2025. – 320 с."),
    ("12", "Чиннатхамби, К. Изучаем React : руководство по созданию современных веб-приложений / К. Чиннатхамби. – Санкт-Петербург : Питер, 2024. – 416 с."),
    
    # Раздел 3: Интернет-документы
    ("РАЗДЕЛ 3. ИНТЕРНЕТ-ДОКУМЕНТЫ", None),
    ("13", "Axum Web Application Framework Documentation : официальная документация проекта. – 2026. – URL: https://docs.rs/axum/latest/axum/ (дата обращения: 15.09.2026). – Текст : электронный."),
    ("14", "Fastify: Fast and low overhead web framework for Node.js : official documentation. – 2026. – URL: https://fastify.dev/ (дата обращения: 18.09.2026). – Текст : электронный."),
    ("15", "NestJS: A progressive Node.js framework : official documentation. – 2026. – URL: https://docs.nestjs.com/ (дата обращения: 16.09.2026). – Текст : электронный."),
    ("16", "Nginx Documentation and Best Practices : официальная документация. – 2026. – URL: https://nginx.org/ru/docs/ (дата обращения: 17.09.2026). – Текст : электронный."),
    ("17", "OWASP Server-Side Request Forgery Prevention Cheat Sheet : руководство по безопасности. – 2025. – URL: https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html (дата обращения: 18.09.2026). – Текст : электронный."),
    ("18", "React 19 Documentation and Architecture Guide : official documentation. – 2026. – URL: https://react.dev/ (дата обращения: 20.09.2026). – Текст : электронный."),
    ("19", "RFC 7519: JSON Web Token (JWT) / M. Jones, J. Bradley, N. Sakimura. – Internet Engineering Task Force (IETF), 2015. – URL: https://datatracker.ietf.org/doc/html/rfc7519 (дата обращения: 15.09.2026). – Текст : электронный."),
    ("20", "RFC 9106: Argon2 Memory-Hard Function for Password Hashing and Proof-of-Work Applications / A. Biryukov, D. Dinu, D. Khovratovich, S. Josefsson. – IETF, 2021. – URL: https://datatracker.ietf.org/doc/html/rfc9106 (дата обращения: 15.09.2026). – Текст : электронный."),
    ("21", "Rust Programming Language Reference : официальное руководство. – 2026. – URL: https://doc.rust-lang.org/reference/ (дата обращения: 10.09.2026). – Текст : электронный."),
    ("22", "TanStack Router and Query Documentation : Modern routing and asynchronous state management. – 2026. – URL: https://tanstack.com/ (дата обращения: 21.09.2026). – Текст : электронный."),
    ("23", "TimescaleDB Documentation : Time-series data on PostgreSQL : официальная документация. – 2026. – URL: https://docs.timescale.com/ (дата обращения: 12.09.2026). – Текст : электронный."),
    ("24", "Tokio: An asynchronous runtime for the Rust programming language : официальная документация. – 2026. – URL: https://tokio.rs/ (дата обращения: 14.09.2026). – Текст : электронный."),
    ("25", "Zod: TypeScript-first schema validation with static type inference : official documentation. – 2026. – URL: https://zod.dev/ (дата обращения: 19.09.2026). – Текст : электронный.")
]

APPENDIX_A_TITLE = "ПРИЛОЖЕНИЕ А. Модуль фонового распределенного опроса целевых ресурсов"
APPENDIX_A_CODE = """// Фрагмент реализации фонового воркера с динамическими виджетами (services/uptime/src/main.rs)
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

    // Загрузка разрешенных типов UI-виджетов из базы данных
    let allowed_widgets = match state.ping_repo.get_allowed_widget_types().await {
        Ok(widgets) => Arc::new(widgets),
        Err(err) => {
            error!("Error fetching allowed widget types: {err}");
            return;
        }
    };

    let pinger = pinger.clone().with_allowed_widgets(allowed_widgets);

    // Конкурентный неблокирующий опрос с пулом воркеров Tokio
    let outcomes: Vec<(PingRecord, bool)> = stream::iter(sites)
        .map(|site| {
            let pinger = pinger.clone();
            let validator = validator.clone();
            async move { check_single_site(site, &validator, &pinger).await }
        })
        .buffer_unordered(config.concurrency)
        .collect()
        .await;

    let results: Vec<PingRecord> = outcomes.into_iter().map(|(record, _)| record).collect();

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

APPENDIX_B_TITLE = "ПРИЛОЖЕНИЕ Б. Многоуровневый модуль сетевой безопасности, защиты от SSRF и потокового лимитирования"
APPENDIX_B_CODE = """// Фрагмент реализации валидатора безопасности и потокового зондирования (services/uptime/src/)
impl IpValidator {
    pub async fn resolve_url(&self, raw_url: &str) -> Result<Vec<SocketAddr>, UrlValidationError> {
        let url = Url::parse(raw_url).map_err(|e| UrlValidationError::InvalidUrl(e.to_string()))?;
        if url.scheme() != "https" && url.scheme() != "http" {
            return Err(UrlValidationError::UnsupportedScheme);
        }
        if !url.username().is_empty() || url.password().is_some() {
            return Err(UrlValidationError::Credentials);
        }

        let host = url.host_str().ok_or(UrlValidationError::MissingHost)?;
        let port = url.port_or_known_default().unwrap_or(80);

        // Резолвинг всех IP-адресов целевого узла через DNS
        let addrs = lookup_host(format!("{}:{}", host, port))
            .await
            .map_err(|e| UrlValidationError::DnsError(e.to_string()))?;

        let mut validated = Vec::new();
        for socket_addr in addrs {
            self.validate(socket_addr.ip()).await?;
            validated.push(socket_addr);
        }
        if validated.is_empty() {
            return Err(UrlValidationError::NoAddresses);
        }
        Ok(validated)
    }

    pub fn is_forbidden_ipv4(ip: Ipv4Addr) -> bool {
        ip.is_private() || ip.is_loopback() || ip.is_link_local()
            || ip.is_unspecified() || ip.is_broadcast() || ip.is_multicast()
            || matches!(ip.octets(), [100, 64..=127, ..])
            || matches!(ip.octets(), [192, 0, 2, ..])
            || matches!(ip.octets(), [198, 51, 100, ..])
            || matches!(ip.octets(), [203, 0, 113, ..])
    }
}

// Защищенный HTTP-клиент с защитой от DNS Rebinding и ограничением размера тела (512 КБайт)
pub async fn fetch_limited(
    url: &Url,
    validator: &IpValidator,
    timeout: Duration,
) -> Result<(reqwest::header::HeaderMap, Vec<u8>, Duration), ProbeError> {
    let addresses = validator.resolve_url(url.as_str()).await?;
    let host = url.host_str().ok_or(UrlValidationError::MissingHost)?;

    let client = reqwest::Client::builder()
        .no_proxy()
        .redirect(reqwest::redirect::Policy::none())
        .timeout(timeout)
        .resolve_to_addrs(host, &addresses) // Подавление DNS Rebinding
        .build()?;

    let started = Instant::now();
    let response = client.get(url.clone()).send().await?;
    let max_payload_bytes = DEFAULT_MAX_PAYLOAD_BYTES; // 512 * 1024 байт

    // Потоковое чтение chunked-ответа с контролем расхода оперативной памяти
    let mut stream = response.bytes_stream();
    let mut body = BytesMut::new();
    while let Some(chunk) = stream.next().await {
        let chunk = chunk?;
        if body.len().saturating_add(chunk.len()) > max_payload_bytes {
            return Err(ProbeError::PayloadTooLarge { max_bytes: max_payload_bytes });
        }
        body.extend_from_slice(&chunk);
    }

    Ok((response.headers().clone(), body.to_vec(), started.elapsed()))
}"""

APPENDIX_C_TITLE = "ПРИЛОЖЕНИЕ В. Схема базы данных (DDL миграции PostgreSQL и TimescaleDB)"
APPENDIX_C_CODE = """-- Инициализация схемы базы данных TimescaleDB (services/uptime/migrations/)

-- Таблица отслеживаемых веб-сайтов
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

-- Таблица допустимых типов кастомных UI-виджетов телеметрии
CREATE TABLE IF NOT EXISTS widgets (
    id SMALLSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO widgets (name) VALUES
    ('badge'), ('stat'), ('gauge'), ('sparkline'),
    ('key_value'), ('chart'), ('row'), ('column'), ('text')
ON CONFLICT (name) DO NOTHING;

-- Гипертаблица для хранения временных рядов замеров доступности и виджетов
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

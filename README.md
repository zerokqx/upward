# Upward 🚀

> **Upward** — распределённая система мониторинга доступности сервисов (Uptime Monitoring) с микросервисной полиглот-архитектурой.

---

## 📐 Архитектура

Система построена на принципах разделения синхронных RPC-вызовов и асинхронной доставки событий:

```mermaid
flowchart TD
    Client[Client / Web UI] --> BFF[BFF\nNestJS / Node.js]
    
    subgraph Synchronous RPC
        BFF -- gRPC --> Nginx[Load Balancer\nNginx grpc_pass]
        BFF -- gRPC --> Identity[Identity Service\nOCaml]
        Nginx -- gRPC --> Uptime1[Uptime Worker 1\nRust / Axum]
        Nginx -- gRPC --> Uptime2[Uptime Worker 2\nRust / Axum]
        Nginx -- gRPC --> Uptime3[Uptime Worker 3\nRust / Axum]
    end

    subgraph Asynchronous Events
        Identity -- Events --> RMQ((RabbitMQ))
        RMQ -- Events --> Uptime1
        RMQ -- Events --> Uptime2
        RMQ -- Events --> Uptime3
    end

    subgraph Storage
        Uptime1 --> DB[(PostgreSQL / TimescaleDB)]
        Uptime2 --> DB
        Uptime3 --> DB
    end
```

### Компоненты системы

| Сервис | Стек | Роль и назначение |
| :--- | :--- | :--- |
| **`services/bff`** | **NestJS** (TypeScript / pnpm) | Backend-for-Frontend: точка входа для клиентов, агрегация данных, сессии/авторизация, проксирование в gRPC. |
| **`services/identity`** | **OCaml** (Dune) | Сервис идентификации, аутентификации и управления профилями пользователей. Эмитит доменные события в RabbitMQ. |
| **`services/uptime`** | **Rust** (Axum / Tokio) | Высокопроизводительный сервис чеков, пингов и сбора метрик доступности. Масштабируется горизонтально. |
| **Nginx** | **Reverse Proxy / LB** | L7 балансировка входящего gRPC-трафика (`grpc_pass`) между репликами Uptime сервиса. |
| **RabbitMQ** | **Message Broker** | Асинхронный обмен событиями (создание пользователя, изменение квот, алерты). |
| **PostgreSQL / TimescaleDB**| **Storage** | Хранение метаданных и таймсерий (истории пингов, метрик задержки и кодов ответа). |

---

## 🛠️ Стек окружения и монорепозиторий

Проект использует современные инструменты управления зависимостями и окружением:
- **[devenv.sh](https://devenv.sh)** / **Nix** — декларативное и изолированное окружение разработки (Rust, OCaml, Node.js, Moonrepo).
- **[direnv](https://direnv.net/)** — автоматическая активация переменных и путей при переходе в директорию проекта.
- **[Moonrepo (moon)](https://moonrepo.dev/)** — умный оркестратор задач и сборки монорепозитория.
- **pnpm** — управление пакетами JS/TS в воркспейсе.

---

## 🚀 Быстрый старт

### Требования
- Установленный [Nix](https://nixos.org/download.html)
- [direnv](https://direnv.net/) и [devenv](https://devenv.sh/)

### 1. Активация окружения

Склонируйте репозиторий и разрешите `direnv`:

```bash
git clone <repo-url> upward
cd upward
direnv allow
```

Либо войдите в шелл вручную:
```bash
devenv shell
```

При входе в шелл активируются все компиляторы и утилиты: `node`, `pnpm`, `cargo`, `ocaml`, `dune`, `moon`.

### 2. Установка зависимостей

```bash
pnpm install
```

---

## 📁 Структура проекта

```text
upward/
├── .moon/               # Конфигурация монорепозитория Moonrepo
├── services/
│   ├── bff/             # NestJS BFF приложение
│   ├── identity/        # OCaml сервис идентификации
│   └── uptime/          # Rust/Axum сервис мониторинга
├── devenv.nix           # Конфигурация окружения разработки (Nix/devenv)
├── pnpm-workspace.yaml  # Конфигурация JS воркспейсов
└── package.json
```

---

## 📜 Лицензия

Private / Proprietary

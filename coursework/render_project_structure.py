#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор архитектурно-структурной схемы монорепозитория «Upward» (Рисунок 11)
в форматах SVG и PNG (через headless Chromium).
Отражает актуальную микросервисную архитектуру:
- Client SPA: React 19 / FSD / TanStack Router & Query / Vite
- BFF Gateway: NestJS / Zod 4 / Orval / Google OAuth / RS256
- Identify: Rust / Axum / Argon2id / RS256 / Redis Refresh Rotation
- Uptime: Rust / Axum / Tokio / TimescaleDB / /upward protocol / widgets validation
- Docs Portal: Fastify / Swagger UI multi-spec hub
- Storage: uptimedb (TimescaleDB 5434), identifydb (Postgres 5432), Redis caches
- DevOps: Moonrepo, devenv (Nix), Docker Compose
"""

import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SVG_PATH = os.path.join(BASE_DIR, "screenshots", "scheme_project_structure.svg")
PNG_PATH = os.path.join(BASE_DIR, "screenshots", "scheme_project_structure.png")

def generate_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1160 820" width="1160" height="820" style="background:#f8fafc; font-family:'Segoe UI', Arial, sans-serif;">
  <defs>
    <filter id="shadow" x="-2%" y="-2%" width="104%" height="106%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#334155"/>
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#2563eb"/>
    </marker>
    <marker id="arrow-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#0d9488"/>
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#7c3aed"/>
    </marker>
  </defs>

  <!-- Title Header -->
  <rect x="30" y="15" width="1100" height="52" rx="8" fill="#1e293b" filter="url(#shadow)"/>
  <text x="580" y="38" fill="#ffffff" font-size="16" font-weight="bold" text-anchor="middle">АРХИТЕКТУРНО-СТРУКТУРНАЯ СХЕМА МОНОРЕПОЗИТОРИЯ «UPWARD»</text>
  <text x="580" y="56" fill="#94a3b8" font-size="11.5" text-anchor="middle">Микросервисная экосистема: Frontend SPA, BFF Gateway, Identify, Uptime Core &amp; Docs Portal</text>

  <!-- External Clients Layer -->
  <rect x="30" y="80" width="1100" height="75" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="45" y="100" fill="#64748b" font-size="10.5" font-weight="bold">КЛИЕНТСКИЙ И ВНЕШНИЙ КОНТУР</text>
  
  <rect x="45" y="108" width="310" height="38" rx="6" fill="#eff6ff" stroke="#93c5fd"/>
  <text x="200" y="132" fill="#1e40af" font-size="11.5" font-weight="bold" text-anchor="middle">Client SPA (React 19 / FSD / TanStack)</text>

  <rect x="385" y="108" width="220" height="38" rx="6" fill="#f0fdf4" stroke="#86efac"/>
  <text x="495" y="132" fill="#166534" font-size="11.5" font-weight="bold" text-anchor="middle">Google OAuth 2.0 Auth</text>

  <rect x="635" y="108" width="230" height="38" rx="6" fill="#faf5ff" stroke="#d8b4fe"/>
  <text x="750" y="132" fill="#6b21a8" font-size="11.5" font-weight="bold" text-anchor="middle">Developer Docs Portal (:5000)</text>

  <rect x="895" y="108" width="215" height="38" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="1002" y="132" fill="#334155" font-size="11.5" font-weight="bold" text-anchor="middle">Target Sites (/upward probe)</text>

  <!-- Ingress / Reverse Proxy -->
  <rect x="30" y="170" width="1100" height="65" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.8" filter="url(#shadow)"/>
  <text x="45" y="193" fill="#1d4ed8" font-size="11.5" font-weight="bold">ВХОДНОЙ ШЛЮЗ: NGINX REVERSE PROXY &amp; L7-БАЛАНСИРОВЩИК (Порты: 80 / 443 HTTPS)</text>
  <text x="45" y="215" fill="#334155" font-size="10.5">SSL/TLS Терминация | Защита от DoS (limit_req) | Балансировка least_conn | Маршрутизация: /api -> BFF (:4000), /docs -> Docs (:5000)</text>

  <!-- Down Arrows from Ingress to Microservices -->
  <path d="M 200 235 L 200 255" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow-blue)"/>
  <path d="M 580 235 L 580 255" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow-blue)"/>
  <path d="M 960 235 L 960 255" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow-blue)"/>

  <!-- ==================== MICROSERVICES LAYER ==================== -->
  
  <!-- 1. Frontend SPA -->
  <g transform="translate(30, 255)" filter="url(#shadow)">
    <rect x="0" y="0" width="255" height="300" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="0" y="0" width="255" height="30" rx="8" fill="#0284c7"/>
    <rect x="0" y="24" width="255" height="6" fill="#0284c7"/>
    <text x="127" y="20" fill="#ffffff" font-size="11.5" font-weight="bold" text-anchor="middle">services/frontend (React 19 SPA)</text>
    
    <text x="12" y="48" fill="#0f172a" font-size="10" font-weight="bold">Архитектура FSD:</text>
    <text x="18" y="65" fill="#475569" font-size="9">• app: провайдеры, роутер</text>
    <text x="18" y="80" fill="#475569" font-size="9">• pages: Dashboard, Sites, Login</text>
    <text x="18" y="95" fill="#475569" font-size="9">• widgets: StatusWidget, Charts</text>
    <text x="18" y="110" fill="#475569" font-size="9">• features: Auth, SiteVerify</text>
    <text x="18" y="125" fill="#475569" font-size="9">• entities: Site, Ping, User</text>
    <text x="18" y="140" fill="#475569" font-size="9">• shared: UI Kit, API Client</text>
    
    <text x="12" y="165" fill="#0f172a" font-size="10" font-weight="bold">Инструментальный стек:</text>
    <text x="18" y="182" fill="#475569" font-size="9">• Vite 8 + TypeScript</text>
    <text x="18" y="197" fill="#475569" font-size="9">• TanStack Router (file-routes)</text>
    <text x="18" y="212" fill="#475569" font-size="9">• TanStack Query v5 (кэш API)</text>
    <text x="18" y="227" fill="#475569" font-size="9">• Orval: автогенерация хуков</text>
    <text x="18" y="242" fill="#475569" font-size="9">• Oxlint: сверхбыстрый линтер</text>
    
    <rect x="10" y="260" width="235" height="28" rx="4" fill="#f0f9ff" stroke="#bae6fd"/>
    <text x="127" y="278" fill="#0369a1" font-size="9.5" font-weight="bold" text-anchor="middle">Порт: 5173 / Client Build</text>
  </g>

  <!-- 2. BFF Gateway -->
  <g transform="translate(300, 255)" filter="url(#shadow)">
    <rect x="0" y="0" width="265" height="300" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="0" y="0" width="265" height="30" rx="8" fill="#2563eb"/>
    <rect x="0" y="24" width="265" height="6" fill="#2563eb"/>
    <text x="132" y="20" fill="#ffffff" font-size="11.5" font-weight="bold" text-anchor="middle">services/bff (NestJS Gateway)</text>
    
    <text x="12" y="48" fill="#0f172a" font-size="10" font-weight="bold">Роль в архитектуре:</text>
    <text x="18" y="65" fill="#475569" font-size="9">• Единая клиентская точка входа</text>
    <text x="18" y="80" fill="#475569" font-size="9">• Валидация схем через Zod 4</text>
    <text x="18" y="95" fill="#475569" font-size="9">• Авторизация сессий (Passport)</text>
    <text x="18" y="110" fill="#475569" font-size="9">• Google OAuth 2.0 интеграция</text>
    <text x="18" y="125" fill="#475569" font-size="9">• Локальная RS256 JWT проверка</text>
    <text x="18" y="140" fill="#475569" font-size="9">• KeyService: кэш публичного ключа</text>
    
    <text x="12" y="165" fill="#0f172a" font-size="10" font-weight="bold">Модули сервиса:</text>
    <text x="18" y="182" fill="#475569" font-size="9">• AuthModule (/auth/login, /refresh)</text>
    <text x="18" y="197" fill="#475569" font-size="9">• SitesModule (/sites, /verify)</text>
    <text x="18" y="212" fill="#475569" font-size="9">• Orval: генерация клиентов</text>
    <text x="18" y="227" fill="#475569" font-size="9">• Централизованный перехват ошибок</text>
    <text x="18" y="242" fill="#475569" font-size="9">• Swagger UI на /docs</text>
    
    <rect x="10" y="260" width="245" height="28" rx="4" fill="#eff6ff" stroke="#bfdbfe"/>
    <text x="132" y="278" fill="#1d4ed8" font-size="9.5" font-weight="bold" text-anchor="middle">Порт: 4000 (Внутренний шлюз)</text>
  </g>

  <!-- 3. Identify Service -->
  <g transform="translate(580, 255)" filter="url(#shadow)">
    <rect x="0" y="0" width="265" height="300" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="0" y="0" width="265" height="30" rx="8" fill="#7c3aed"/>
    <rect x="0" y="24" width="265" height="6" fill="#7c3aed"/>
    <text x="132" y="20" fill="#ffffff" font-size="11.5" font-weight="bold" text-anchor="middle">services/identify (Rust Auth)</text>
    
    <text x="12" y="48" fill="#0f172a" font-size="10" font-weight="bold">Безопасность и Ключи:</text>
    <text x="18" y="65" fill="#475569" font-size="9">• Хранение RSA 2048-bit (RS256)</text>
    <text x="18" y="80" fill="#475569" font-size="9">• Приватный ключ certs/private.pem</text>
    <text x="18" y="95" fill="#475569" font-size="9">• Раздача ключа: /keys/public (JSON)</text>
    <text x="18" y="110" fill="#475569" font-size="9">• Raw PEM ключ: /keys/public.pem</text>
    <text x="18" y="125" fill="#475569" font-size="9">• Argon2id хеш паролей со солью</text>
    
    <text x="12" y="150" fill="#0f172a" font-size="10" font-weight="bold">Управление токенами:</text>
    <text x="18" y="167" fill="#475569" font-size="9">• Access Token (RS256, TTL 15 мин)</text>
    <text x="18" y="182" fill="#475569" font-size="9">• Refresh Token Rotation в Redis</text>
    <text x="18" y="197" fill="#475569" font-size="9">• Атомарный GETDEL при обновлении</text>
    <text x="18" y="212" fill="#475569" font-size="9">• Google OAuth аккаунты без пароля</text>
    <text x="18" y="227" fill="#475569" font-size="9">• Axum + Tokio + SQLx PostgreSQL</text>
    <text x="18" y="242" fill="#475569" font-size="9">• utoipa: генерация OpenAPI 3.0</text>
    
    <rect x="10" y="260" width="245" height="28" rx="4" fill="#f5f3ff" stroke="#ddd6fe"/>
    <text x="132" y="278" fill="#6d28d9" font-size="9.5" font-weight="bold" text-anchor="middle">Порт: 3001 (Безопасный контур)</text>
  </g>

  <!-- 4. Uptime Core -->
  <g transform="translate(860, 255)" filter="url(#shadow)">
    <rect x="0" y="0" width="270" height="300" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="0" y="0" width="270" height="30" rx="8" fill="#0d9488"/>
    <rect x="0" y="24" width="270" height="6" fill="#0d9488"/>
    <text x="135" y="20" fill="#ffffff" font-size="11.5" font-weight="bold" text-anchor="middle">services/uptime (Monitoring Core)</text>
    
    <text x="12" y="48" fill="#0f172a" font-size="10" font-weight="bold">Конвейер зондирования:</text>
    <text x="18" y="65" fill="#475569" font-size="9">• Tokio stream buffer_unordered(25)</text>
    <text x="18" y="80" fill="#475569" font-size="9">• FOR UPDATE SKIP LOCKED захват</text>
    <text x="18" y="95" fill="#475569" font-size="9">• Dead Worker Recovery (3 мин)</text>
    <text x="18" y="110" fill="#475569" font-size="9">• Batch Insert сотен строк в 1 запрос</text>
    
    <text x="12" y="135" fill="#0f172a" font-size="10" font-weight="bold">Протокол /upward и UI-виджеты:</text>
    <text x="18" y="152" fill="#475569" font-size="9">• Опрос эндпоинта {url}/upward</text>
    <text x="18" y="167" fill="#475569" font-size="9">• Валидация по таблице widgets</text>
    <text x="18" y="182" fill="#475569" font-size="9">• HTTP-01 Challenge подтверждение</text>
    
    <text x="12" y="205" fill="#0f172a" font-size="10" font-weight="bold">Защита периметра (Zero-Trust):</text>
    <text x="18" y="222" fill="#475569" font-size="9">• SSRF фильтр RFC 1918 &amp; forbidden_ip</text>
    <text x="18" y="237" fill="#475569" font-size="9">• DNS Rebinding: resolve_to_addrs</text>
    <text x="18" y="252" fill="#475569" font-size="9">• Потоковый лимит MAX_PAYLOAD 512КБ</text>
    
    <rect x="10" y="260" width="250" height="28" rx="4" fill="#f0fdfa" stroke="#99f6e4"/>
    <text x="135" y="278" fill="#0f766e" font-size="9.5" font-weight="bold" text-anchor="middle">Порт: 3000 (Кластер воркеров)</text>
  </g>

  <!-- Horizontal Inter-Service Connection Arrows -->
  <path d="M 285 380 L 300 380" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow-blue)"/>
  <path d="M 565 380 L 580 380" fill="none" stroke="#7c3aed" stroke-width="2" marker-end="url(#arrow-purple)"/>
  <path d="M 845 380 L 860 380" fill="none" stroke="#0d9488" stroke-width="2" marker-end="url(#arrow-teal)"/>

  <!-- ==================== STORAGE & INFRASTRUCTURE LAYER ==================== -->
  <rect x="30" y="575" width="1100" height="185" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="45" y="598" fill="#64748b" font-size="11" font-weight="bold">СЛОЙ ХРАНЕНИЯ ДАННЫХ И ДЕКЛАРАТИВНОЙ ИНФРАСТРУКТУРЫ (STORAGE &amp; DEVOPS)</text>

  <!-- DB 1: uptimedb (TimescaleDB) -->
  <g transform="translate(45, 610)">
    <rect x="0" y="0" width="260" height="135" rx="6" fill="#f0fdfa" stroke="#0d9488" stroke-width="1.2"/>
    <text x="12" y="20" fill="#0f766e" font-size="11" font-weight="bold">uptimedb (TimescaleDB / Postgres)</text>
    <text x="12" y="38" fill="#0f172a" font-size="9.5" font-weight="bold">Порт: 5434 | Расширение Timescale</text>
    <text x="12" y="56" fill="#475569" font-size="9">• site_pings: гипертаблица RTT</text>
    <text x="12" y="72" fill="#475569" font-size="9">• add_retention_policy('30 days')</text>
    <text x="12" y="88" fill="#475569" font-size="9">• sites: реестр ресурсов (active, idle)</text>
    <text x="12" y="104" fill="#475569" font-size="9">• forbidden_ip: SSRF черный список</text>
    <text x="12" y="120" fill="#475569" font-size="9">• widgets: каталог типов виджетов</text>
  </g>

  <!-- DB 2: identifydb (PostgreSQL) -->
  <g transform="translate(320, 610)">
    <rect x="0" y="0" width="245" height="135" rx="6" fill="#f5f3ff" stroke="#7c3aed" stroke-width="1.2"/>
    <text x="12" y="20" fill="#6d28d9" font-size="11" font-weight="bold">identifydb (PostgreSQL 16)</text>
    <text x="12" y="38" fill="#0f172a" font-size="9.5" font-weight="bold">Порт: 5432 | База пользователей</text>
    <text x="12" y="56" fill="#475569" font-size="9">• users: профили, email (unique),</text>
    <text x="18" y="72" fill="#475569" font-size="9">  password_hash (Argon2id)</text>
    <text x="12" y="88" fill="#475569" font-size="9">• oauth_accounts: Google OAuth</text>
    <text x="18" y="104" fill="#475569" font-size="9">  (provider, provider_user_id)</text>
    <text x="12" y="120" fill="#475569" font-size="9">• Миграции через SQLx CLI</text>
  </g>

  <!-- Cache: Redis Instances -->
  <g transform="translate(580, 610)">
    <rect x="0" y="0" width="265" height="135" rx="6" fill="#fff7ed" stroke="#ea580c" stroke-width="1.2"/>
    <text x="12" y="20" fill="#c2410c" font-size="11" font-weight="bold">Redis In-Memory Data Stores</text>
    <text x="12" y="38" fill="#0f172a" font-size="9.5" font-weight="bold">uptime-redis (:6379) &amp; identify-redis (:6380)</text>
    <text x="12" y="56" fill="#475569" font-size="9">• challenge:{site_id}:{token}</text>
    <text x="18" y="72" fill="#475569" font-size="9">  TTL 24ч для валидации владения</text>
    <text x="12" y="88" fill="#475569" font-size="9">• refresh:{uuid} -> user_id</text>
    <text x="18" y="104" fill="#475569" font-size="9">  TTL 30 дней с ротацией GETDEL</text>
    <text x="12" y="120" fill="#475569" font-size="9">• Изолированные docker-сети</text>
  </g>

  <!-- DevOps & Central Docs Portal -->
  <g transform="translate(860, 610)">
    <rect x="0" y="0" width="255" height="135" rx="6" fill="#f8fafc" stroke="#475569" stroke-width="1.2"/>
    <text x="12" y="20" fill="#1e293b" font-size="11" font-weight="bold">Оркестрация &amp; Документация</text>
    <text x="12" y="38" fill="#0f172a" font-size="9.5" font-weight="bold">Moonrepo, devenv (Nix), Fastify Docs</text>
    <text x="12" y="56" fill="#475569" font-size="9">• services/docs: Fastify (:5000)</text>
    <text x="18" y="72" fill="#475569" font-size="9">  Единый портал Swagger UI (BFF,</text>
    <text x="18" y="88" fill="#475569" font-size="9">  Uptime, Identify спецификации)</text>
    <text x="12" y="104" fill="#475569" font-size="9">• Moonrepo: кэширование сборки</text>
    <text x="12" y="120" fill="#475569" font-size="9">• devenv: Rust, Node, pnpm, SQLx</text>
  </g>

  <!-- Footer Info -->
  <text x="580" y="785" fill="#64748b" font-size="11" text-anchor="middle">Разработчик: Шахсинов М. В. | Курсовой проект «Upward» | АНО ПОО «КЭПиИТ», Москва, 2026</text>
</svg>'''

def main():
    print("1. Generating updated scheme_project_structure.svg...")
    with open(SVG_PATH, "w", encoding="utf-8") as f:
        f.write(generate_svg())
    print(f"Saved SVG to {SVG_PATH}")

    print("2. Rendering PNG via Headless Chromium...")
    html_content = f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ margin: 0; padding: 0; background: transparent; }}
  </style>
</head>
<body>
  {generate_svg()}
</body>
</html>'''
    temp_html = "/tmp/scheme_structure_render.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    cmd = [
        "/etc/profiles/per-user/zerok/bin/chromium",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--window-size=1160,820",
        f"--screenshot={PNG_PATH}",
        temp_html
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"PNG rendered successfully -> {PNG_PATH} ({os.path.getsize(PNG_PATH)} bytes)")
    except Exception as e:
        print(f"Error rendering PNG with Chromium: {e}")

if __name__ == "__main__":
    main()

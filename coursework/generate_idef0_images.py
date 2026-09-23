#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор векторных SVG и PNG изображений диаграмм IDEF0 для курсового проекта
"""

import subprocess
import os

OUTPUT_DIR = "/home/zerok/projects/upward/screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_a0_context_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 700" width="1100" height="700" style="background:#ffffff; font-family:'Times New Roman', serif;">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#0f172a"/>
    </marker>
  </defs>

  <!-- Заголовок -->
  <text x="550" y="40" font-size="17" font-weight="bold" text-anchor="middle" fill="#0f172a">КОНТЕКСТНАЯ ФУНКЦИОНАЛЬНАЯ ДИАГРАММА IDEF0: А-0</text>
  <text x="550" y="65" font-size="14" text-anchor="middle" fill="#334155">Мониторинг доступности внутренней инфраструктуры веб-приложений «Upward»</text>

  <!-- Центральный функциональный блок А0 -->
  <rect x="350" y="240" width="400" height="190" fill="#f8fafc" stroke="#1e293b" stroke-width="2.5" rx="4"/>
  <text x="550" y="315" font-size="15" font-weight="bold" text-anchor="middle" fill="#0f172a">Осуществлять распределенный</text>
  <text x="550" y="340" font-size="15" font-weight="bold" text-anchor="middle" fill="#0f172a">мониторинг доступности внутренней</text>
  <text x="550" y="365" font-size="15" font-weight="bold" text-anchor="middle" fill="#0f172a">инфраструктуры веб-приложений «Upward»</text>
  <text x="730" y="415" font-size="13" font-weight="bold" fill="#475569">А0</text>

  <!-- УПРАВЛЕНИЕ (СВЕРХУ) -->
  <!-- Стрелка 1: SLA -->
  <line x1="420" y1="90" x2="420" y2="240" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow)"/>
  <text x="410" y="140" font-size="11.5" text-anchor="end" fill="#0f172a">Соглашения SLA/SLO;</text>
  <text x="410" y="155" font-size="11.5" text-anchor="end" fill="#0f172a">Целевая доступность 99.9%</text>

  <!-- Стрелка 2: SSRF и черные списки -->
  <line x1="550" y1="90" x2="550" y2="240" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow)"/>
  <text x="550" y="130" font-size="11.5" text-anchor="middle" fill="#0f172a">Политики ИБ (фильтрация RFC 1918,</text>
  <text x="550" y="145" font-size="11.5" text-anchor="middle" fill="#0f172a">SSRF, черный список forbidden_ip)</text>

  <!-- Стрелка 3: Конфиг воркера -->
  <line x1="680" y1="90" x2="680" y2="240" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow)"/>
  <text x="690" y="140" font-size="11.5" text-anchor="start" fill="#0f172a">Параметры воркера (таймаут 10 с,</text>
  <text x="690" y="155" font-size="11.5" text-anchor="start" fill="#0f172a">concurrency=25, retention=30d)</text>

  <!-- ВХОДЫ (СЛЕВА) -->
  <!-- Вход 1: URL и user_id -->
  <line x1="60" y1="285" x2="350" y2="285" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow)"/>
  <text x="70" y="275" font-size="12" fill="#0f172a">Целевые URL сайтов (http/https); user_id</text>

  <!-- Вход 2: Сетевые ответы -->
  <line x1="60" y1="345" x2="350" y2="345" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow)"/>
  <text x="70" y="335" font-size="12" fill="#0f172a">Сетевые HTTP/TCP ответы веб-узлов (RTT, статус)</text>

  <!-- Вход 3: Challenge токены -->
  <line x1="60" y1="395" x2="350" y2="395" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow)"/>
  <text x="70" y="385" font-size="12" fill="#0f172a">Токены подтверждения владения (HTTP-01)</text>

  <!-- ВЫХОДЫ (СПРАВА) -->
  <!-- Выход 1: Временные ряды -->
  <line x1="750" y1="285" x2="1040" y2="285" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow)"/>
  <text x="765" y="275" font-size="12" fill="#0f172a">Временные ряды замеров (duration_ms, time) в TimescaleDB</text>

  <!-- Выход 2: Статусы сайтов -->
  <line x1="750" y1="345" x2="1040" y2="345" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow)"/>
  <text x="765" y="335" font-size="12" fill="#0f172a">Реестр подтвержденных сайтов (idle, active)</text>

  <!-- Выход 3: OpenAPI / Health -->
  <line x1="750" y1="395" x2="1040" y2="395" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow)"/>
  <text x="765" y="385" font-size="12" fill="#0f172a">Интерактивный интерфейс Swagger UI и Health-статусы</text>

  <!-- МЕХАНИЗМЫ (СНИЗУ) -->
  <!-- Механизм 1: Uptime Rust -->
  <line x1="420" y1="610" x2="420" y2="430" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow)"/>
  <text x="410" y="540" font-size="11.5" text-anchor="end" fill="#0f172a">Сервис Uptime (Rust/Axum);</text>
  <text x="410" y="555" font-size="11.5" text-anchor="end" fill="#0f172a">воркер buffer_unordered</text>

  <!-- Механизм 2: TimescaleDB и Redis -->
  <line x1="550" y1="610" x2="550" y2="430" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow)"/>
  <text x="550" y="540" font-size="11.5" text-anchor="middle" fill="#0f172a">СУБД PostgreSQL/TimescaleDB;</text>
  <text x="550" y="555" font-size="11.5" text-anchor="middle" fill="#0f172a">In-Memory хранилище Redis</text>

  <!-- Механизм 3: Nginx, BFF, SRE -->
  <line x1="680" y1="610" x2="680" y2="430" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow)"/>
  <text x="690" y="540" font-size="11.5" text-anchor="start" fill="#0f172a">L7 Nginx балансировщик; BFF;</text>
  <text x="690" y="555" font-size="11.5" text-anchor="start" fill="#0f172a">SRE-инженеры и администраторы</text>
</svg>'''

def generate_a0_decomp_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1150 780" width="1150" height="780" style="background:#ffffff; font-family:'Times New Roman', serif;">
  <defs>
    <marker id="arrow2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#0f172a"/>
    </marker>
  </defs>

  <!-- Заголовок -->
  <text x="575" y="35" font-size="17" font-weight="bold" text-anchor="middle" fill="#0f172a">ДИАГРАММА ДЕКОМПОЗИЦИИ IDEF0: А0</text>
  <text x="575" y="58" font-size="13.5" text-anchor="middle" fill="#334155">Декомпозиция процессов распределенного мониторинга «Upward»</text>

  <!-- БЛОК А1 -->
  <rect x="90" y="140" width="190" height="95" fill="#f8fafc" stroke="#1e293b" stroke-width="2" rx="3"/>
  <text x="185" y="175" font-size="12" font-weight="bold" text-anchor="middle" fill="#0f172a">Регистрировать ресурсы</text>
  <text x="185" y="195" font-size="12" font-weight="bold" text-anchor="middle" fill="#0f172a">и верифицировать права</text>
  <text x="265" y="225" font-size="11" font-weight="bold" fill="#475569">А1</text>

  <!-- БЛОК А2 -->
  <rect x="350" y="270" width="190" height="95" fill="#f8fafc" stroke="#1e293b" stroke-width="2" rx="3"/>
  <text x="445" y="305" font-size="12" font-weight="bold" text-anchor="middle" fill="#0f172a">Атомарно захватывать</text>
  <text x="445" y="325" font-size="12" font-weight="bold" text-anchor="middle" fill="#0f172a">и распределять батчи</text>
  <text x="525" y="355" font-size="11" font-weight="bold" fill="#475569">А2</text>

  <!-- БЛОК А3 -->
  <rect x="610" y="400" width="190" height="95" fill="#f8fafc" stroke="#1e293b" stroke-width="2" rx="3"/>
  <text x="705" y="435" font-size="12" font-weight="bold" text-anchor="middle" fill="#0f172a">Выполнять параллельный</text>
  <text x="705" y="455" font-size="12" font-weight="bold" text-anchor="middle" fill="#0f172a">опрос веб-узлов</text>
  <text x="785" y="485" font-size="11" font-weight="bold" fill="#475569">А3</text>

  <!-- БЛОК А4 -->
  <rect x="870" y="530" width="190" height="95" fill="#f8fafc" stroke="#1e293b" stroke-width="2" rx="3"/>
  <text x="965" y="565" font-size="12" font-weight="bold" text-anchor="middle" fill="#0f172a">Пакетно сохранять телеметрию</text>
  <text x="965" y="585" font-size="12" font-weight="bold" text-anchor="middle" fill="#0f172a">и отдавать аналитику</text>
  <text x="1045" y="615" font-size="11" font-weight="bold" fill="#475569">А4</text>

  <!-- ================= СТРЕЛКИ И СВЯЗИ ================= -->
  <!-- Вход в А1 -->
  <line x1="20" y1="180" x2="90" y2="180" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow2)"/>
  <text x="25" y="165" font-size="11" fill="#0f172a">URL и user_id</text>

  <!-- Управление А1 -->
  <line x1="185" y1="75" x2="185" y2="140" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow2)"/>
  <text x="185" y="105" font-size="10.5" text-anchor="middle" fill="#0f172a">SSRF фильтрация</text>

  <!-- Связь А1 -> А2 -->
  <path d="M 280 185 L 315 185 L 315 310 L 350 310" fill="none" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow2)"/>
  <text x="320" y="245" font-size="10.5" fill="#0f172a">Активные сайты</text>
  <text x="320" y="260" font-size="10.5" fill="#0f172a">(active=true)</text>

  <!-- Управление А2 -->
  <line x1="445" y1="75" x2="445" y2="270" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow2)"/>
  <text x="450" y="110" font-size="10.5" fill="#0f172a">SKIP LOCKED, batch_size</text>

  <!-- Связь А2 -> А3 -->
  <path d="M 540 315 L 575 315 L 575 440 L 610 440" fill="none" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow2)"/>
  <text x="580" y="375" font-size="10.5" fill="#0f172a">Батч сайтов</text>
  <text x="580" y="390" font-size="10.5" fill="#0f172a">(processing)</text>

  <!-- Вход в А3 (сеть) -->
  <path d="M 20 455 L 610 455" fill="none" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow2)"/>
  <text x="30" y="445" font-size="11" fill="#0f172a">Ответы целевых веб-узлов (RTT, статус)</text>

  <!-- Управление А3 -->
  <line x1="705" y1="75" x2="705" y2="400" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow2)"/>
  <text x="710" y="110" font-size="10.5" fill="#0f172a">buffer_unordered(25), таймаут 10 с</text>

  <!-- Связь А3 -> А4 -->
  <path d="M 800 445 L 835 445 L 835 570 L 870 570" fill="none" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow2)"/>
  <text x="840" y="505" font-size="10.5" fill="#0f172a">Результаты замеров</text>
  <text x="840" y="520" font-size="10.5" fill="#0f172a">Vec&lt;PingRecord&gt;</text>

  <!-- Управление А4 -->
  <line x1="965" y1="75" x2="965" y2="530" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow2)"/>
  <text x="970" y="110" font-size="10.5" fill="#0f172a">Retention 30 дней; JWT</text>

  <!-- Выход из А4: обратная связь в А2 -->
  <path d="M 935 625 L 935 670 L 415 670 L 415 365" fill="none" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow2)"/>
  <text x="675" y="660" font-size="11" text-anchor="middle" fill="#0f172a">Фиксация last_check и сброс status='idle' для следующего цикла</text>

  <!-- Выход из А4: финальная телеметрия -->
  <line x1="1060" y1="575" x2="1130" y2="575" stroke="#0f172a" stroke-width="1.8" marker-end="url(#arrow2)"/>
  <text x="1065" y="555" font-size="10.5" fill="#0f172a">Метрики в БД;</text>
  <text x="1065" y="570" font-size="10.5" fill="#0f172a">API Swagger</text>

  <!-- Механизмы снизу -->
  <line x1="185" y1="720" x2="185" y2="235" stroke="#0f172a" stroke-width="1.6" marker-end="url(#arrow2)"/>
  <text x="185" y="740" font-size="10" text-anchor="middle" fill="#475569">IpValidator; Redis</text>

  <line x1="445" y1="720" x2="445" y2="365" stroke="#0f172a" stroke-width="1.6" marker-end="url(#arrow2)"/>
  <text x="445" y="740" font-size="10" text-anchor="middle" fill="#475569">SiteRepo; CTE SQL</text>

  <line x1="705" y1="720" x2="705" y2="495" stroke="#0f172a" stroke-width="1.6" marker-end="url(#arrow2)"/>
  <text x="705" y="740" font-size="10" text-anchor="middle" fill="#475569">HttpPinger; Tokio</text>

  <line x1="965" y1="720" x2="965" y2="625" stroke="#0f172a" stroke-width="1.6" marker-end="url(#arrow2)"/>
  <text x="965" y="740" font-size="10" text-anchor="middle" fill="#475569">PingRepo; TimescaleDB</text>
</svg>'''

def main():
    svg1_path = os.path.join(OUTPUT_DIR, "idef0_a0_context.svg")
    svg2_path = os.path.join(OUTPUT_DIR, "idef0_a0_decomp.svg")
    png1_path = os.path.join(OUTPUT_DIR, "idef0_a0_context.png")
    png2_path = os.path.join(OUTPUT_DIR, "idef0_a0_decomp.png")

    with open(svg1_path, "w", encoding="utf-8") as f:
        f.write(generate_a0_context_svg())
    with open(svg2_path, "w", encoding="utf-8") as f:
        f.write(generate_a0_decomp_svg())

    print("Converting SVGs to high-res PNGs via Chromium...")
    cmd1 = [
        "/etc/profiles/per-user/zerok/bin/chromium",
        "--headless=new",
        "--disable-gpu",
        "--window-size=1200,750",
        f"--screenshot={png1_path}",
        f"file://{svg1_path}"
    ]
    subprocess.run(cmd1, check=True)

    cmd2 = [
        "/etc/profiles/per-user/zerok/bin/chromium",
        "--headless=new",
        "--disable-gpu",
        "--window-size=1250,850",
        f"--screenshot={png2_path}",
        f"file://{svg2_path}"
    ]
    subprocess.run(cmd2, check=True)

    print(f"Saved: {png1_path} ({os.path.getsize(png1_path)} bytes)")
    print(f"Saved: {png2_path} ({os.path.getsize(png2_path)} bytes)")

if __name__ == "__main__":
    main()

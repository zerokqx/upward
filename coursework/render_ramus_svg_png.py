#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Рендерер векторных диаграмм IDEF0 в стандарте и стиле CASE-системы Ramus
для курсового проекта Шахсинова М. В.
Идеальная геометрия без малейших пересечений надписей и блоков.
"""

import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def svg_header(author="Шахсинов М. В.", project="ИС мониторинга Upward", date="22.09.2026", context="ВЕРХ"):
    return f'''
    <!-- Ramus Frame Border -->
    <rect x="20" y="20" width="1200" height="780" fill="#FFFEEB" stroke="#000000" stroke-width="2"/>
    
    <!-- Top Header Table -->
    <rect x="20" y="20" width="180" height="75" fill="none" stroke="#000000" stroke-width="1"/>
    <text x="28" y="38" font-size="10" font-family="Arial" font-weight="bold" fill="#000000">ИСПОЛЬЗУЕТСЯ В:</text>
    
    <rect x="200" y="20" width="270" height="75" fill="none" stroke="#000000" stroke-width="1"/>
    <text x="208" y="38" font-size="10" font-family="Arial" font-weight="bold" fill="#000000">АВТОР: <tspan font-weight="normal">{author}</tspan></text>
    <text x="208" y="54" font-size="10" font-family="Arial" font-weight="bold" fill="#000000">ПРОЕКТ: <tspan font-weight="normal">{project}</tspan></text>
    <text x="208" y="82" font-size="9" font-family="Arial" font-weight="bold" fill="#000000">ЗАМЕЧАНИЯ: 1 2 3 4 5 6 7 8 9 10</text>
    
    <rect x="470" y="20" width="150" height="75" fill="none" stroke="#000000" stroke-width="1"/>
    <text x="478" y="38" font-size="10" font-family="Arial" font-weight="bold" fill="#000000">ДАТА: <tspan font-weight="normal">{date}</tspan></text>
    <text x="478" y="54" font-size="10" font-family="Arial" font-weight="bold" fill="#000000">РЕВИЗИЯ: <tspan font-weight="normal">{date}</tspan></text>
    
    <rect x="620" y="20" width="190" height="75" fill="none" stroke="#000000" stroke-width="1"/>
    <text x="628" y="36" font-size="9" font-family="Arial" font-weight="bold" fill="#000000">■ РАЗРАБАТЫВАЕТСЯ</text>
    <text x="628" y="50" font-size="9" font-family="Arial" fill="#000000">□ ЧЕРНОВИК</text>
    <text x="628" y="64" font-size="9" font-family="Arial" fill="#000000">□ РЕКОМЕНДОВАНО</text>
    <text x="628" y="78" font-size="9" font-family="Arial" fill="#000000">□ ПУБЛИКАЦИЯ</text>
    
    <rect x="810" y="20" width="190" height="75" fill="none" stroke="#000000" stroke-width="1"/>
    <text x="818" y="38" font-size="10" font-family="Arial" fill="#000000">ЧИТАТЕЛЬ</text>
    <text x="918" y="38" font-size="10" font-family="Arial" fill="#000000">ДАТА</text>
    <line x1="810" y1="44" x2="1000" y2="44" stroke="#000000" stroke-width="0.7"/>
    
    <rect x="1000" y="20" width="220" height="75" fill="none" stroke="#000000" stroke-width="1"/>
    <text x="1008" y="38" font-size="10" font-family="Arial" font-weight="bold" fill="#000000">КОНТЕКСТ:</text>
    <text x="1110" y="64" font-size="14" font-family="Arial" font-weight="bold" text-anchor="middle" fill="#000000">{context}</text>
    '''

def svg_footer(node="Ветка: А-0", title="Название процесса", num=1):
    return f'''
    <!-- Bottom Footer Table -->
    <rect x="20" y="760" width="200" height="40" fill="none" stroke="#000000" stroke-width="1"/>
    <text x="30" y="785" font-size="11" font-family="Arial" font-weight="bold" fill="#000000">Ветка: {node}</text>
    
    <rect x="220" y="760" width="800" height="40" fill="none" stroke="#000000" stroke-width="1"/>
    <text x="620" y="785" font-size="12" font-family="Arial" font-weight="bold" text-anchor="middle" fill="#000000">Название: {title}</text>
    
    <rect x="1020" y="760" width="200" height="40" fill="none" stroke="#000000" stroke-width="1"/>
    <text x="1120" y="785" font-size="11" font-family="Arial" font-weight="bold" text-anchor="middle" fill="#000000">Номер: {num}</text>
    '''

def svg_block(text_lines, code, x, y, w, h, is_decomposed=False, is_purple=False):
    fill = "#F3E8FF" if is_purple else "#FFFFFF"
    stroke = "#9333EA" if is_purple else "#000000"
    txt_col = "#581C87" if is_purple else "#000000"
    
    lines_svg = []
    line_h = 16
    start_y = y + (h - len(text_lines) * line_h) // 2 + 12
    for i, line in enumerate(text_lines):
        lines_svg.append(f'<text x="{x + w//2}" y="{start_y + i*line_h}" font-size="11" font-family="Arial" font-weight="bold" text-anchor="middle" fill="{txt_col}">{line}</text>')
    
    decomp_svg = ""
    if is_decomposed:
        decomp_svg = f'<line x1="{x}" y1="{y+16}" x2="{x+16}" y2="{y}" stroke="{stroke}" stroke-width="1.8"/>'
        
    return f'''
    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>
    {decomp_svg}
    {"".join(lines_svg)}
    <text x="{x + w - 8}" y="{y + h - 8}" font-size="11" font-family="Arial" font-weight="bold" text-anchor="end" fill="{txt_col}">{code}</text>
    '''

def svg_arrow(path_d, label, lx, ly, is_purple=False, align="left", font_size="9.5"):
    stroke = "#9333EA" if is_purple else "#000000"
    txt_col = "#7E22CE" if is_purple else "#000000"
    m_url = "url(#arr-purple)" if is_purple else "url(#arr-black)"
    
    anchor = "start" if align == "left" else ("middle" if align == "center" else "end")
    return f'''
    <path d="{path_d}" fill="none" stroke="{stroke}" stroke-width="1.8" marker-end="{m_url}"/>
    <text x="{lx}" y="{ly}" font-size="{font_size}" font-family="Arial" text-anchor="{anchor}" fill="{txt_col}">{label}</text>
    '''

def wrap_svg(inner_content):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1240 820" width="1240" height="820" style="background:#ECE9D8;">
  <defs>
    <marker id="arr-black" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#000000"/>
    </marker>
    <marker id="arr-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#9333EA"/>
    </marker>
  </defs>
  {inner_content}
</svg>'''

# 1. AS-IS A-0
def get_as_is_a0_ctx_svg():
    header = svg_header("Шахсинов М. В.", "Мониторинг веб-ресурсов (AS-IS)", "22.09.2026", "ВЕРХ")
    footer = svg_footer("А-0", "Мониторинг доступности веб-ресурсов предприятия вручную (AS-IS)", 1)
    box = svg_block(["Мониторинг доступности", "веб-ресурсов предприятия", "вручную"], "А0", 430, 330, 360, 150, is_decomposed=True)
    
    arrows = [
        svg_arrow("M 50 375 L 430 375", "Заявки на мониторинг узлов", 60, 365, align="left", font_size="10"),
        svg_arrow("M 50 435 L 430 435", "Сведения о целевых веб-ресурсах", 60, 425, align="left", font_size="10"),
        
        svg_arrow("M 520 120 L 520 330", "Регламент контроля доступности", 510, 210, align="right", font_size="10"),
        svg_arrow("M 700 120 L 700 330", "Нормативы SLA и задержки", 710, 210, align="left", font_size="10"),
        
        svg_arrow("M 520 710 L 520 480", "Дежурный инженер мониторинга", 510, 620, align="right", font_size="10"),
        svg_arrow("M 700 710 L 700 480", "ПК с утилитами cURL и ping", 710, 620, align="left", font_size="10"),
        
        svg_arrow("M 790 375 L 1180 375", "Журнал инцидентов и отказов (Excel)", 810, 365, align="left", font_size="10"),
        svg_arrow("M 790 435 L 1180 435", "Извещения по почте и телефону", 810, 425, align="left", font_size="10"),
    ]
    return wrap_svg(header + footer + box + "".join(arrows))

# 2. AS-IS A0 Decomp
def get_as_is_a0_decomp_svg():
    header = svg_header("Шахсинов М. В.", "Мониторинг веб-ресурсов (AS-IS)", "22.09.2026", "А-0")
    footer = svg_footer("А0", "Мониторинг доступности веб-ресурсов предприятия (AS-IS)", 2)
    
    b1 = svg_block(["Прием и регистрация", "заявок на мониторинг"], "А1", 180, 150, 175, 90, is_decomposed=False)
    b2 = svg_block(["Ручной опрос и", "тестирование узлов"], "А2", 410, 285, 175, 90, is_decomposed=True)
    b3 = svg_block(["Анализ телеметрии и", "фиксация отказов"], "А3", 640, 420, 175, 90, is_decomposed=False)
    b4 = svg_block(["Ручное оповещение и", "составление отчетов"], "А4", 870, 555, 175, 90, is_decomposed=False)

    arrows = [
        svg_arrow("M 30 170 L 180 170", "Заявки на мониторинг", 175, 163, align="right", font_size="9"),
        svg_arrow("M 30 210 L 180 210", "Сведения о ресурсах", 175, 203, align="right", font_size="9"),
        
        svg_arrow("M 355 195 L 385 195 L 385 330 L 410 330", "Реестр адресов", 380, 260, align="right", font_size="9"),
        svg_arrow("M 585 330 L 615 330 L 615 465 L 640 465", "Протокол ответов", 610, 395, align="right", font_size="9"),
        svg_arrow("M 815 465 L 845 465 L 845 600 L 870 600", "Записи инцидентов", 840, 530, align="right", font_size="9"),
        
        svg_arrow("M 1045 580 L 1195 580", "Журнал отказов (Excel)", 1055, 573, align="left", font_size="9.5"),
        svg_arrow("M 1045 620 L 1195 620", "Извещения по почте", 1055, 613, align="left", font_size="9.5"),
        
        svg_arrow("M 267 100 L 267 150", "Регламент контроля", 260, 135, align="right", font_size="9"),
        svg_arrow("M 497 100 L 497 285", "Нормативы SLA", 490, 140, align="right", font_size="9"),
        svg_arrow("M 727 100 L 727 420", "Нормативы SLA", 720, 140, align="right", font_size="9"),
        svg_arrow("M 957 100 L 957 555", "Регламент оповещения", 950, 140, align="right", font_size="9"),
        
        svg_arrow("M 267 745 L 267 240", "Дежурный инженер", 260, 735, align="right", font_size="9"),
        svg_arrow("M 497 745 L 497 375", "Утилиты cURL и ping", 490, 735, align="right", font_size="9"),
        svg_arrow("M 727 745 L 727 510", "Таблицы Excel", 720, 735, align="right", font_size="9"),
        svg_arrow("M 957 745 L 957 645", "Корпоративная почта", 950, 735, align="right", font_size="9"),
    ]
    return wrap_svg(header + footer + b1 + b2 + b3 + b4 + "".join(arrows))

# 3. AS-IS A2 Decomp
def get_as_is_a2_decomp_svg():
    header = svg_header("Шахсинов М. В.", "Мониторинг веб-ресурсов (AS-IS)", "22.09.2026", "А2")
    footer = svg_footer("А2", "Ручной опрос и тестирование узлов (AS-IS)", 3)
    
    b1 = svg_block(["Формирование разового", "списка адресов"], "А21", 180, 150, 175, 90, is_decomposed=False)
    b2 = svg_block(["Последовательный запуск", "HTTP/ICMP утилит"], "А22", 410, 285, 175, 90, is_decomposed=False)
    b3 = svg_block(["Ручной замер сетевых", "задержек и кодов"], "А23", 640, 420, 175, 90, is_decomposed=False)
    b4 = svg_block(["Формирование итогового", "протокола опроса"], "А24", 870, 555, 175, 90, is_decomposed=False)

    arrows = [
        svg_arrow("M 30 195 L 180 195", "Реестр адресов", 175, 187, align="right", font_size="9"),
        svg_arrow("M 355 195 L 385 195 L 385 330 L 410 330", "Список для консоли", 380, 260, align="right", font_size="9"),
        svg_arrow("M 585 330 L 615 330 L 615 465 L 640 465", "Вывод терминала", 610, 395, align="right", font_size="9"),
        svg_arrow("M 815 465 L 845 465 L 845 600 L 870 600", "Сводка таймингов", 840, 530, align="right", font_size="9"),
        svg_arrow("M 1045 600 L 1195 600", "Протокол ответов", 1055, 592, align="left", font_size="9.5"),
        
        svg_arrow("M 267 100 L 267 150", "График ручных обходов", 260, 135, align="right", font_size="9"),
        svg_arrow("M 497 100 L 497 285", "Инструкция по cURL", 490, 140, align="right", font_size="9"),
        svg_arrow("M 727 100 L 727 420", "Нормативы задержки SLA", 720, 140, align="right", font_size="9"),
        svg_arrow("M 957 100 L 957 555", "Шаблон протокола", 950, 140, align="right", font_size="9"),

        svg_arrow("M 267 745 L 267 240", "Дежурный инженер", 260, 735, align="right", font_size="9"),
        svg_arrow("M 497 745 L 497 375", "Утилиты cURL и ping", 490, 735, align="right", font_size="9"),
        svg_arrow("M 727 745 L 727 510", "Дежурный инженер", 720, 735, align="right", font_size="9"),
        svg_arrow("M 957 745 L 957 645", "Дежурный инженер", 950, 735, align="right", font_size="9"),
    ]
    return wrap_svg(header + footer + b1 + b2 + b3 + b4 + "".join(arrows))

# 4. TO-BE A-0
def get_to_be_a0_ctx_svg():
    header = svg_header("Шахсинов М. В.", "ИС мониторинга Upward (TO-BE)", "22.09.2026", "ВЕРХ")
    footer = svg_footer("А-0", "Автоматизированный мониторинг веб-ресурсов системой Upward (TO-BE)", 4)
    box = svg_block(["Автоматизированный мониторинг", "доступности и телеметрии веб-ресурсов", "информационной системой «Upward»"], "А0", 410, 330, 400, 150, is_decomposed=True, is_purple=True)

    arrows = [
        svg_arrow("M 40 370 L 410 370", "Конфигурации целевых веб-ресурсов", 50, 360, align="left", font_size="10"),
        svg_arrow("M 40 435 L 410 435", "Запросы узлов через REST API / Swagger", 50, 425, is_purple=True, align="left", font_size="10"),

        svg_arrow("M 510 120 L 510 330", "Политики безопасности и правила SSRF", 500, 200, is_purple=True, align="right", font_size="10"),
        svg_arrow("M 710 120 L 710 330", "Нормативы SLA и расписания фонового опроса", 720, 200, align="left", font_size="10"),

        svg_arrow("M 510 710 L 510 480", "Системный администратор и инженеры", 500, 620, align="right", font_size="10"),
        svg_arrow("M 710 710 L 710 480", "ИС Upward (Rust worker, TimescaleDB, Redis, Nginx, BFF)", 720, 620, is_purple=True, align="left", font_size="10"),

        svg_arrow("M 810 370 L 1180 370", "Метрики (DNS, TLS, TTFB) в гипертаблице TimescaleDB", 825, 360, is_purple=True, align="left", font_size="10"),
        svg_arrow("M 810 420 L 1180 420", "Мгновенные вебхук-уведомления об авариях", 825, 410, is_purple=True, align="left", font_size="10"),
        svg_arrow("M 810 460 L 1180 460", "Аналитические отчеты об аптайме веб-ресурсов", 825, 450, align="left", font_size="10"),
    ]
    return wrap_svg(header + footer + box + "".join(arrows))

# 5. TO-BE A0 Decomp
def get_to_be_a0_decomp_svg():
    header = svg_header("Шахсинов М. В.", "ИС мониторинга Upward (TO-BE)", "22.09.2026", "А-0")
    footer = svg_footer("А0", "Автоматизированный мониторинг веб-ресурсов системой Upward (TO-BE)", 5)

    b1 = svg_block(["Регистрация, валидация SSRF", "и верификация ресурсов"], "А1", 180, 150, 175, 90, is_decomposed=True, is_purple=True)
    b2 = svg_block(["Атомарный захват батчей", "и параллельный опрос узлов"], "А2", 410, 285, 175, 90, is_decomposed=True, is_purple=True)
    b3 = svg_block(["Анализ ответов, запись в гипер-", "таблицу и детекция сбоев"], "А3", 640, 420, 175, 90, is_decomposed=False, is_purple=True)
    b4 = svg_block(["Агрегация метрик, отображение", "в Swagger/BFF и алертинг"], "А4", 870, 555, 175, 90, is_decomposed=False, is_purple=True)

    arrows = [
        # Входы в А1
        svg_arrow("M 30 170 L 180 170", "Запросы REST API / Swagger", 175, 163, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 30 210 L 180 210", "Конфигурации ресурсов", 175, 203, align="right", font_size="9"),
        
        # Связи
        svg_arrow("M 355 195 L 385 195 L 385 330 L 410 330", "Сайты в БД (active=true)", 380, 260, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 585 330 L 615 330 L 615 465 L 640 465", "Замеры сетевых зондов", 610, 395, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 815 465 L 845 465 L 845 600 L 870 600", "Метрики и инциденты", 840, 530, is_purple=True, align="right", font_size="9"),
        
        # Обратная связь
        svg_arrow("M 930 645 L 930 675 L 440 675 L 440 375", "Фиксация last_check и сброс status=idle", 685, 668, is_purple=True, align="center", font_size="9"),
        
        # Выходы
        svg_arrow("M 1045 580 L 1195 580", "Временные ряды TimescaleDB", 1055, 573, is_purple=True, align="left", font_size="9.5"),
        svg_arrow("M 1045 620 L 1195 620", "Вебхук-алерты об авариях", 1055, 613, is_purple=True, align="left", font_size="9.5"),
        
        # Управление
        svg_arrow("M 267 100 L 267 150", "Политики безопасности SSRF", 260, 135, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 497 100 L 497 285", "SKIP LOCKED и buffer_unordered", 490, 140, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 727 100 L 727 420", "Пороги SLA и критерии аварий", 720, 140, align="right", font_size="9"),
        svg_arrow("M 957 100 L 957 555", "Спецификация OpenAPI/Swagger", 950, 140, is_purple=True, align="right", font_size="9"),
        
        # Механизмы
        svg_arrow("M 267 745 L 267 240", "Контроллер sites и SSRF-фильтр", 260, 735, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 510 745 L 510 375", "Воркер Tokio и SQLx (SKIP LOCKED)", 500, 735, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 727 745 L 727 510", "СУБД TimescaleDB (гипертаблица)", 720, 735, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 957 745 L 957 645", "Шлюз BFF (NestJS) и Swagger UI", 950, 735, is_purple=True, align="right", font_size="9"),
    ]
    return wrap_svg(header + footer + b1 + b2 + b3 + b4 + "".join(arrows))

# 6. TO-BE A1 Decomp
def get_to_be_a1_decomp_svg():
    header = svg_header("Шахсинов М. В.", "ИС мониторинга Upward (TO-BE)", "22.09.2026", "А1")
    footer = svg_footer("А1", "Регистрация, валидация SSRF и верификация ресурсов (TO-BE)", 6)

    b1 = svg_block(["Прием параметров узла через", "REST API / Swagger"], "А11", 180, 150, 175, 90, is_decomposed=False, is_purple=True)
    b2 = svg_block(["Инспекция IP-адресов на", "SSRF и приватные сети"], "А12", 410, 285, 175, 90, is_decomposed=False, is_purple=True)
    b3 = svg_block(["Верификация владения доменом", "(DNS TXT / Meta-tag)"], "А13", 640, 420, 175, 90, is_decomposed=False, is_purple=True)
    b4 = svg_block(["Фиксация конфигурации", "ресурса в таблице sites"], "А14", 870, 555, 175, 90, is_decomposed=False, is_purple=True)

    arrows = [
        svg_arrow("M 30 195 L 180 195", "Запросы добавления узлов", 175, 187, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 355 195 L 385 195 L 385 330 L 410 330", "Модель параметров сайта", 380, 260, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 585 330 L 615 330 L 615 465 L 640 465", "Безопасный публичный URL", 610, 395, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 815 465 L 845 465 L 845 600 L 870 600", "Подтвержденный домен", 840, 530, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 1045 600 L 1195 600", "Верифицированные сайты в БД", 1055, 592, is_purple=True, align="left", font_size="9.5"),

        svg_arrow("M 267 100 L 267 150", "Схема DTO CreateSiteDto", 260, 135, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 497 100 L 497 285", "Список RFC 1918 и loopback", 490, 140, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 727 100 L 727 420", "Протокол DNS TXT / Meta", 720, 140, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 957 100 L 957 555", "Схема PostgreSQL", 950, 140, align="right", font_size="9"),

        svg_arrow("M 267 745 L 267 240", "Маршрутизатор Axum", 260, 735, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 497 745 L 497 375", "Модуль dns_guard (Rust)", 490, 735, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 727 745 L 727 510", "Верификатор токенов", 720, 735, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 957 745 L 957 645", "SiteRepository (SQLx)", 950, 735, is_purple=True, align="right", font_size="9"),
    ]
    return wrap_svg(header + footer + b1 + b2 + b3 + b4 + "".join(arrows))

# 7. TO-BE A2 Decomp
def get_to_be_a2_decomp_svg():
    header = svg_header("Шахсинов М. В.", "ИС мониторинга Upward (TO-BE)", "22.09.2026", "А2")
    footer = svg_footer("А2", "Атомарный захват батчей и параллельный опрос узлов (TO-BE)", 7)

    b1 = svg_block(["Атомарный захват батча", "без гонок реплик"], "А21", 180, 150, 175, 90, is_decomposed=False, is_purple=True)
    b2 = svg_block(["Мультиплексирование", "асинхронных зондов"], "А22", 410, 285, 175, 90, is_decomposed=False, is_purple=True)
    b3 = svg_block(["Прецизионный замер фаз", "сетевого соединения"], "А23", 640, 420, 175, 90, is_decomposed=False, is_purple=True)
    b4 = svg_block(["Сборка результатов и", "сериализация телеметрии"], "А24", 870, 555, 175, 90, is_decomposed=False, is_purple=True)

    arrows = [
        svg_arrow("M 30 195 L 180 195", "Верифицированные сайты в БД", 175, 187, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 355 195 L 385 195 L 385 330 L 410 330", "Изолированный батч сайтов", 380, 260, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 585 330 L 615 330 L 615 465 L 640 465", "Потоки сетевых HTTP-зондов", 610, 395, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 815 465 L 845 465 L 845 600 L 870 600", "Сводка таймингов (DNS/TLS)", 840, 530, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 1045 600 L 1195 600", "Сырые замеры зондов", 1055, 592, is_purple=True, align="left", font_size="9.5"),

        svg_arrow("M 267 100 L 267 150", "FOR UPDATE SKIP LOCKED", 260, 135, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 497 100 L 497 285", "Лимит buffer_unordered", 490, 140, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 727 100 L 727 420", "Тайм-ауты сетевых сокетов", 720, 140, align="right", font_size="9"),
        svg_arrow("M 957 100 L 957 555", "Схема DTO PingRecord", 950, 140, is_purple=True, align="right", font_size="9"),

        svg_arrow("M 267 745 L 267 240", "Пул соединений SQLx", 260, 735, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 497 745 L 497 375", "Среда исполнения Tokio", 490, 735, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 727 745 L 727 510", "Клиент Reqwest и Instant", 720, 735, is_purple=True, align="right", font_size="9"),
        svg_arrow("M 957 745 L 957 645", "Библиотека Serde JSON", 950, 735, is_purple=True, align="right", font_size="9"),
    ]
    return wrap_svg(header + footer + b1 + b2 + b3 + b4 + "".join(arrows))

def main():
    diagrams = [
        ("idef0_as_is_a0_context", get_as_is_a0_ctx_svg()),
        ("idef0_as_is_a0_decomp", get_as_is_a0_decomp_svg()),
        ("idef0_as_is_a2_decomp", get_as_is_a2_decomp_svg()),
        ("idef0_to_be_a0_context", get_to_be_a0_ctx_svg()),
        ("idef0_to_be_a0_decomp", get_to_be_a0_decomp_svg()),
        ("idef0_to_be_a1_decomp", get_to_be_a1_decomp_svg()),
        ("idef0_to_be_a2_decomp", get_to_be_a2_decomp_svg()),
    ]

    chromium_path = "/etc/profiles/per-user/zerok/bin/chromium"

    for name, svg_content in diagrams:
        svg_path = os.path.join(OUTPUT_DIR, f"{name}.svg")
        png_path = os.path.join(OUTPUT_DIR, f"{name}.png")
        
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        
        cmd = [
            chromium_path,
            "--headless=new",
            "--disable-gpu",
            "--window-size=1280,850",
            f"--screenshot={png_path}",
            f"file://{svg_path}"
        ]
        subprocess.run(cmd, check=True)
        size_kb = os.path.getsize(png_path) / 1024
        print(f"Rendered {name}.png ({size_kb:.1f} KB)")

if __name__ == "__main__":
    main()

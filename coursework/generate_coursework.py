#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт генерации курсового проекта в формате OpenDocument Text (.odt)
по теме: «Разработка веб-приложения распределенного мониторинга внутренней инфраструктуры «Upward»»
Включает:
- Строгое соответствие титульного листа официальному шаблону методички (АНО ПОО «КЭПиИТ»):
  «Курсовой проект», тема с подписью «(тема курсового проекта)», структурированные поля
  специальности с кодом, квалификации, обучающегося и руководителя с полями подписей.
- Интеграция полной схемы базы данных (ER-диаграмма и гипертаблицы TimescaleDB, Рисунок 8),
  спроектированной на основе реальных миграций PostgreSQL/TimescaleDB/Redis.
- Встраивание всех 7 диаграмм IDEF0 (CASE-пакет Ramus Educational) в Главе 1 с ГОСТ-подписями (Рисунки 1–7).
- Встраивание скриншотов Swagger UI в Главе 2 (Рисунки 9–10).
- Встраивание архитектурной схемы монорепозитория (Рисунок 11) и таблицы структуры (Таблица 5) в разделе 2.4.
- Полное пересоздание всех таблиц (Таблицы 1–5) как нативных OpenDocument-таблиц
  со стандартными рамками 0.5pt, выверенными ширинами столбцов, отступами и центрированными заголовками.
- Оформление программного кода шрифтом Courier New 10pt строго без фонового цвета (без затенения).
"""

import os
import io
import zipfile
import html

from coursework_data import TITLE_DATA, TOC_ITEMS, INTRO_PARAGRAPHS
from coursework_chapter1 import (
    CHAPTER_1_TITLE,
    SEC_1_1_TITLE, SEC_1_1_TEXT,
    SEC_1_2_TITLE, SEC_1_2_TEXT,
    SEC_1_3_TITLE, SEC_1_3_TEXT,
    SEC_1_4_TITLE, SEC_1_4_TEXT,
)
from coursework_chapter2 import (
    CHAPTER_2_TITLE,
    SEC_2_1_TITLE, SEC_2_1_TEXT,
    SEC_2_2_TITLE, SEC_2_2_TEXT,
    SEC_2_3_TITLE, SEC_2_3_TEXT,
    SEC_2_4_TITLE, SEC_2_4_TEXT,
)
from coursework_conclusion_and_bib import (
    CONCLUSION_TITLE, CONCLUSION_TEXT,
    BIBLIOGRAPHY_TITLE, BIBLIOGRAPHY_ITEMS,
    APPENDIX_A_TITLE, APPENDIX_A_CODE,
    APPENDIX_B_TITLE, APPENDIX_B_CODE,
    APPENDIX_C_TITLE, APPENDIX_C_CODE,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_ODT = os.path.join(BASE_DIR, "Курсовая_работа_Шахсинов_Мурда.odt")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")

TABLE_COLUMN_STYLES = []

def esc(s):
    return html.escape(str(s))

def make_manifest_xml():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.3">
 <manifest:file-entry manifest:full-path="/" manifest:version="1.3" manifest:media-type="application/vnd.oasis.opendocument.text"/>
 <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="Pictures/idef0_as_is_a0_context.png" manifest:media-type="image/png"/>
 <manifest:file-entry manifest:full-path="Pictures/idef0_as_is_a0_decomp.png" manifest:media-type="image/png"/>
 <manifest:file-entry manifest:full-path="Pictures/idef0_as_is_a2_decomp.png" manifest:media-type="image/png"/>
 <manifest:file-entry manifest:full-path="Pictures/idef0_to_be_a0_context.png" manifest:media-type="image/png"/>
 <manifest:file-entry manifest:full-path="Pictures/idef0_to_be_a0_decomp.png" manifest:media-type="image/png"/>
 <manifest:file-entry manifest:full-path="Pictures/idef0_to_be_a1_decomp.png" manifest:media-type="image/png"/>
 <manifest:file-entry manifest:full-path="Pictures/idef0_to_be_a2_decomp.png" manifest:media-type="image/png"/>
 <manifest:file-entry manifest:full-path="Pictures/db_schema_upward.png" manifest:media-type="image/png"/>
 <manifest:file-entry manifest:full-path="Pictures/swagger_overview.png" manifest:media-type="image/png"/>
 <manifest:file-entry manifest:full-path="Pictures/swagger_sites_create_full.png" manifest:media-type="image/png"/>
 <manifest:file-entry manifest:full-path="Pictures/scheme_project_structure.png" manifest:media-type="image/png"/>
</manifest:manifest>'''

def make_meta_xml():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
 xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 office:version="1.3">
 <office:meta>
  <dc:title>Разработка веб-приложения распределенного мониторинга внутренней инфраструктуры «Upward»</dc:title>
  <dc:creator>Шахсинов М. В.</dc:creator>
  <meta:creation-date>2026-09-22T12:00:00Z</meta:creation-date>
  <dc:language>ru-RU</dc:language>
 </office:meta>
</office:document-meta>'''

def make_styles_xml():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
 xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
 xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
 xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
 xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
 office:version="1.3">
 
 <office:font-face-decls>
  <style:font-face style:name="Times New Roman" svg:font-family="&apos;Times New Roman&apos;" style:font-family-generic="roman" style:font-pitch="variable"/>
  <style:font-face style:name="Courier New" svg:font-family="&apos;Courier New&apos;" style:font-family-generic="modern" style:font-pitch="fixed"/>
 </office:font-face-decls>

 <office:styles>
  <style:default-style style:family="paragraph">
   <style:paragraph-properties fo:hyphenation-ladder-count="no-limit" style:text-autospace="ideograph-alpha" style:punctuation-wrap="hanging" style:line-break="strict"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="14pt" fo:language="ru" fo:country="RU"/>
  </style:default-style>
  
  <style:style style:name="Footer_Style" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:margin-top="0cm" fo:margin-bottom="0cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="11pt"/>
  </style:style>
 </office:styles>

 <office:automatic-styles>
  <style:page-layout style:name="PL_First">
   <style:page-layout-properties fo:page-width="21.0cm" fo:page-height="29.7cm"
    fo:margin-top="2.0cm" fo:margin-bottom="2.0cm" fo:margin-left="3.0cm" fo:margin-right="1.0cm"
    style:print-orientation="portrait"/>
  </style:page-layout>
  
  <style:page-layout style:name="PL_Standard">
   <style:page-layout-properties fo:page-width="21.0cm" fo:page-height="29.7cm"
    fo:margin-top="2.0cm" fo:margin-bottom="2.0cm" fo:margin-left="3.0cm" fo:margin-right="1.0cm"
    style:print-orientation="portrait"/>
   <style:footer-style>
    <style:header-footer-properties fo:min-height="0.6cm" fo:margin-top="0.4cm"/>
   </style:footer-style>
  </style:page-layout>
 </office:automatic-styles>

 <office:master-styles>
  <style:master-page style:name="First_Page" style:page-layout-name="PL_First" style:next-style-name="Standard"/>
  <style:master-page style:name="Standard" style:page-layout-name="PL_Standard">
   <style:footer>
    <text:p text:style-name="Footer_Style"><text:page-number text:select-page="current"/></text:p>
   </style:footer>
  </style:master-page>
 </office:master-styles>

</office:document-styles>'''

def make_fig_block(img_href, caption, width="15.5cm", height="10.3cm", fig_id=1):
    return (
        f'<text:p text:style-name="P_Fig_Image">'
        f'<draw:frame draw:name="Fig_{fig_id}" draw:style-name="Graphic1" text:anchor-type="as-char" svg:width="{width}" svg:height="{height}" draw:z-index="{fig_id}">'
        f'<draw:image xlink:href="{img_href}" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>'
        f'</draw:frame></text:p>'
        f'<text:p text:style-name="P_Fig_Caption">{esc(caption)}</text:p>'
    )

def build_odt_table(name, headers, rows, col_widths=None, center_cols=None):
    if center_cols is None:
        center_cols = set()
    else:
        center_cols = set(center_cols)

    xml = [f'<table:table table:name="{name}" table:style-name="Table_Bordered">']
    
    if col_widths:
        for idx, width in enumerate(col_widths):
            style_name = f"{name}_Col_{idx}"
            TABLE_COLUMN_STYLES.append(
                f'<style:style style:name="{style_name}" style:family="table-column">\n'
                f' <style:table-column-properties style:column-width="{width}"/>\n'
                f'</style:style>'
            )
            xml.append(f'<table:table-column table:style-name="{style_name}"/>')
    else:
        for _ in headers:
            xml.append('<table:table-column/>')
    
    # Headers
    xml.append('<table:table-header-rows><table:table-row>')
    for h in headers:
        xml.append(f'<table:table-cell table:style-name="Cell_Header" office:value-type="string">'
                   f'<text:p text:style-name="P_Table_Header">{esc(h)}</text:p>'
                   f'</table:table-cell>')
    xml.append('</table:table-row></table:table-header-rows>')
    
    # Data Rows
    for row in rows:
        xml.append('<table:table-row>')
        for idx, cell in enumerate(row):
            cell_style = "Cell_Data_Center" if idx in center_cols else "Cell_Data"
            p_style = "P_Table_Center" if idx in center_cols else "P_Table_Text"
            xml.append(f'<table:table-cell table:style-name="{cell_style}" office:value-type="string">'
                       f'<text:p text:style-name="{p_style}">{esc(cell)}</text:p>'
                       f'</table:table-cell>')
        xml.append('</table:table-row>')
        
    xml.append('</table:table>')
    return "\n".join(xml)

def render_comparison_table():
    headers = ["Критерий сравнения", "До автоматизации (AS-IS)", "После автоматизации (TO-BE, «Upward»)"]
    col_widths = ["4.0cm", "6.5cm", "6.5cm"]
    rows = [
        ["Способ инициации проверок", "Ручной запуск администратором либо несогласованные cron-скрипты", "Автоматический непрерывный асинхронный конвейер воркеров"],
        ["Периодичность контроля узлов", "Нерегулярная (1 раз в 15–45 минут)", "Детерминированная (настраиваемый интервал: от 5 до 60 секунд)"],
        ["Среднее время обнаружения аварии (MTTD)", "20–50 минут (часто по звонкам или жалобам пользователей)", "5–10 секунд (мгновенная фиксация сетевого таймаута)"],
        ["Масштабируемость (емкость узлов)", "До 50–100 хостов (исчерпание дескрипторов ОС и памяти)", "Свыше 10 000 хостов на один инстанс сервиса (Tokio/epoll)"],
        ["Защита от атак SSRF", "Отсутствует (cURL опрашивает любые введенные адреса)", "Многоуровневый фильтр (RFC 1918, loopback, forbidden_ip)"],
        ["Верификация прав на ресурс", "Отсутствует (риск нелегитимного сканирования)", "Протокол HTTP-01 Challenge с сохранением ключей в Redis"],
        ["Хранение и глубина аналитики метрик", "Разрозненные текстовые лог-файлы, фрагменты в Excel", "Гипертаблицы TimescaleDB с глубиной 30 дней и авто-ротацией"],
        ["Точность замера задержки (RTT)", "Низкая (искажения из-за форка cURL и нагрузки ОС)", "Субмикросекундная точность языка Rust без пауз GC"],
        ["Трудозатраты дежурного SRE-персонала", "Высокие (до 30% рабочего времени на рутину)", "Минимальные (реагирование на автоматические алерты)"]
    ]
    return build_odt_table("Table1", headers, rows, col_widths=col_widths)

def render_table_2():
    headers = ["Критерий сравнения", "Rust (Tokio)", "Go (Golang)", "Node.js (TS)", "Python (Asyncio)"]
    col_widths = ["4.2cm", "3.2cm", "3.2cm", "3.2cm", "3.2cm"]
    rows = [
        ["Модель управления памятью", "RAII / Borrow Checker (без GC)", "Garbage Collector (паузы Stop-the-World)", "Garbage Collector (V8 Engine)", "Reference Counting + GC"],
        ["Накладные расходы на задачу", "64 байта – 2 КБ (стейт-машина)", "2–4 КБ (динамический стек)", "Высокие (объекты Promise)", "Высокие (объекты Task)"],
        ["Предсказуемость задержки (Latency)", "Детерминированная (субмикросекунды)", "Всплески задержек из-за GC", "Задержки деоптимизации JIT", "Высокая вариативность"],
        ["Безопасность конкурентности", "Send/Sync на этапе компиляции", "Риск Data Race в рантайме", "Однопоточный Event Loop", "GIL (Global Interpreter Lock)"],
        ["Потребление памяти (10k задач)", "~15–25 МБайт", "~40–80 МБайт", "~150–300 МБайт", "~250–500 МБайт"]
    ]
    return build_odt_table("Table2", headers, rows, col_widths=col_widths)

def render_table_3():
    headers = ["Критерий", "TimescaleDB", "PostgreSQL (Vanilla)", "ClickHouse", "MongoDB"]
    col_widths = ["4.2cm", "3.2cm", "3.2cm", "3.2cm", "3.2cm"]
    rows = [
        ["Специализация на Time-Series", "Высокая (гипертаблицы)", "Базовая (ручные партиции)", "Экстремальная (OLAP)", "Time Series Collections"],
        ["Поддержка ACID-транзакций", "Полная (PostgreSQL)", "Полная", "Ограниченная (блочные вставки)", "Ограниченная"],
        ["UPDATE с FOR UPDATE SKIP LOCKED", "Да (нативно)", "Да", "Нет (неприменимо)", "Да (поточечные блокировки)"],
        ["Авто-ротация (Data Retention)", "Да (add_retention_policy)", "Внешние скрипты / cron", "Да (TTL на таблицы)", "Да (TTL индексы)"],
        ["Интеграция с реляционными связями", "Родная (FK, JOIN)", "Родная", "Затруднена", "Нет"]
    ]
    return build_odt_table("Table3", headers, rows, col_widths=col_widths)

def render_table_4():
    headers = ["№", "Входные данные", "Вводимое значение", "Ожидаемая реакция программы", "Фактическая реакция программы", "Ошибка"]
    col_widths = ["0.8cm", "3.2cm", "3.6cm", "4.0cm", "3.9cm", "1.5cm"]
    center_cols = [0, 5]
    rows = [
        ["1", "POST /sites (Корректный URL)", "user_id: usr_01, site: https://yandex.ru", "HTTP 201 Created, pending_verification", "HTTP 201 Created, токен в Redis", "Нет"],
        ["2", "POST /sites (Схема ftp://)", "user_id: usr_01, site: ftp://google.com", "HTTP 400 Bad Request, сообщение схемы", "HTTP 400 Bad Request, схема отклонена", "Нет"],
        ["3", "POST /sites (SSRF на 127.0.0.1)", "user_id: usr_01, site: http://127.0.0.1:8080", "HTTP 403 Forbidden, Private IP not allowed", "HTTP 403 Forbidden, заблокировано", "Нет"],
        ["4", "POST /sites (Черный список IP)", "user_id: usr_01, site: https://malicious.org", "HTTP 403 Forbidden, IP is in forbidden list", "HTTP 403 Forbidden, отсечено по БД", "Нет"],
        ["5", "POST /sites/{id}/verify", "site_id, токен /.well-known/upward", "HTTP 200 OK, active = true", "HTTP 200 OK, сайт активирован", "Нет"],
        ["6", "GET /health (Liveness проба)", "Запрос без параметров", "HTTP 200 OK, status: ok", "HTTP 200 OK, сервис в норме", "Нет"],
        ["7", "Фоновый опрос (Стресс-тест)", "batch_size=500, concurrency=25", "Опрос ровно по 25 сокетов, Batch Insert", "Выполнен за 1.8 с, без утечек дескрипторов", "Нет"]
    ]
    return build_odt_table("Table4", headers, rows, col_widths=col_widths, center_cols=center_cols)

def render_table_5():
    headers = ["Каталог / Компонент", "Стек технологий", "Функциональное назначение в системе «Upward»", "Роль в мониторинге"]
    col_widths = ["3.8cm", "3.0cm", "7.2cm", "3.0cm"]
    center_cols = [1, 3]
    rows = [
        ["devenv.nix, devenv.yaml", "Nix / Devenv", "Декларативное описание изолированной среды разработки (Rust 1.80+, Node.js 20+, pnpm, OCaml, Moonrepo, SQLx CLI)", "Единая среда сборки"],
        [".moon/ (workspace.yml)", "Moonrepo", "Конфигурация монорепозитория, пайплайнов сборки, линтинга, тестирования и кэширования артефактов", "Оркестратор задач"],
        ["services/uptime/src/main.rs", "Rust, Tokio", "Точка входа ядра мониторинга: запуск HTTP-сервера Axum и непрерывного фонового конвейера опроса", "Управление воркерами"],
        ["services/uptime/src/domain.rs", "Rust (Newtypes)", "Строго типизированные структуры предметной области: SiteId, UserId, SiteUrl, SiteStatus", "Доменная модель"],
        ["services/uptime/src/site/", "Rust, Axum, SQLx", "Модуль управления сайтами: REST API регистрации, верификация владения HTTP-01 Challenge, выборка батчей", "Реестр и верификация"],
        ["services/uptime/src/ping/", "Rust, Axum, SQLx", "Модуль зондирования: выполнение проверок, замер сетевой задержки (RTT), получение исторических выборок", "Сбор телеметрии"],
        ["services/uptime/src/infrastructure.rs", "Rust, Reqwest", "Клиент асинхронного сетевого зондирования, многоуровневый фильтр SSRF (RFC 1918, loopback, БД)", "Сетевой клиент и защита"],
        ["services/uptime/migrations/", "SQL, SQLx CLI", "Идемпотентные миграции БД: таблицы sites, forbidden_ip и гипертаблица site_pings", "Схема TimescaleDB"],
        ["services/uptime/compose.infra.yml", "Docker Compose", "Контейнеризация локальных сервисов хранения данных: TimescaleDB (Postgres 16) и Redis 7", "Локальные хранилища"],
        ["services/bff/src/", "NestJS, TypeScript", "Шлюз Backend-for-Frontend: клиентская авторизация по открытому ключу JWKS, агрегация прикладных API", "Клиентский шлюз API"],
        ["services/identify/", "Rust, Axum (Ed25519)", "Сервис идентификации: выпуск JWT-токенов, хранение приватного ключа, трансляция JWKS для микросервисов", "Провайдер ключей и JWT"]
    ]
    return build_odt_table("Table5", headers, rows, col_widths=col_widths, center_cols=center_cols)

def render_title_page_meta_table():
    """
    Таблица метаданных и подписей титульного листа по точному образцу методички колледжа.
    Ширина столбцов: 5.5cm, 3.8cm, 7.7cm (общая ширина 17.0cm).
    """
    xml = [
        '<table:table table:name="TableTitleMeta" table:style-name="Table_Title_Meta">',
        ' <table:table-column table:style-name="TitleMeta_Col_0"/>',
        ' <table:table-column table:style-name="TitleMeta_Col_1"/>',
        ' <table:table-column table:style-name="TitleMeta_Col_2"/>',
        
        # Row 1: Specialty
        ' <table:table-row>',
        f'  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Label">{esc(TITLE_DATA["specialty_label"])}</text:p></table:table-cell>',
        f'  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Val_Center">{esc(TITLE_DATA["specialty_code"])}</text:p></table:table-cell>',
        f'  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Val_Bold">{esc(TITLE_DATA["specialty_name"])}</text:p></table:table-cell>',
        ' </table:table-row>',
        
        # Row 2: (код), (наименование)
        ' <table:table-row>',
        '  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Label"/></table:table-cell>',
        f'  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Sub">{esc(TITLE_DATA["specialty_code_sub"])}</text:p></table:table-cell>',
        f'  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Sub">{esc(TITLE_DATA["specialty_name_sub"])}</text:p></table:table-cell>',
        ' </table:table-row>',

        # Row 3: Qualification
        ' <table:table-row>',
        f'  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Label">{esc(TITLE_DATA["qualification_label"])}</text:p></table:table-cell>',
        f'  <table:table-cell table:style-name="Cell_Meta" table:number-columns-spanned="2" office:value-type="string"><text:p text:style-name="P_Meta_Val_Bold">{esc(TITLE_DATA["qualification_name"])}</text:p></table:table-cell>',
        ' </table:table-row>',

        # Row 4: (название квалификации)
        ' <table:table-row>',
        '  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Label"/></table:table-cell>',
        f'  <table:table-cell table:style-name="Cell_Meta" table:number-columns-spanned="2" office:value-type="string"><text:p text:style-name="P_Meta_Sub">{esc(TITLE_DATA["qualification_sub"])}</text:p></table:table-cell>',
        ' </table:table-row>',

        # Row 5: Student
        ' <table:table-row>',
        f'  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Label">{esc(TITLE_DATA["student_label"])}</text:p></table:table-cell>',
        f'  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Val_Center">{esc(TITLE_DATA["signature_line"])}</text:p></table:table-cell>',
        f'  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Val_Bold">{esc(TITLE_DATA["student_name"])}</text:p></table:table-cell>',
        ' </table:table-row>',

        # Row 6: (подпись), (Фамилия и Инициалы)
        ' <table:table-row>',
        '  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Label"/></table:table-cell>',
        f'  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Sub">{esc(TITLE_DATA["signature_sub"])}</text:p></table:table-cell>',
        f'  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Sub">{esc(TITLE_DATA["student_sub"])}</text:p></table:table-cell>',
        ' </table:table-row>',

        # Row 7: Supervisor
        ' <table:table-row>',
        f'  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Label">Руководитель курсового<text:line-break/>проекта</text:p></table:table-cell>',
        f'  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Val_Center">{esc(TITLE_DATA["signature_line"])}</text:p></table:table-cell>',
        f'  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Val_Bold">{esc(TITLE_DATA["supervisor_name"])}</text:p></table:table-cell>',
        ' </table:table-row>',

        # Row 8: (подпись), (ученая степень, звание...)
        ' <table:table-row>',
        '  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Label"/></table:table-cell>',
        f'  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Sub">{esc(TITLE_DATA["signature_sub"])}</text:p></table:table-cell>',
        f'  <table:table-cell table:style-name="Cell_Meta" office:value-type="string"><text:p text:style-name="P_Meta_Sub">{esc(TITLE_DATA["supervisor_sub"])}</text:p></table:table-cell>',
        ' </table:table-row>',

        '</table:table>'
    ]
    return "\n".join(xml)

def make_content_xml():
    global TABLE_COLUMN_STYLES
    TABLE_COLUMN_STYLES = []
    
    # Регистрация колонок для таблицы метаданных титульного листа
    TABLE_COLUMN_STYLES.append('<style:style style:name="TitleMeta_Col_0" style:family="table-column"><style:table-column-properties style:column-width="5.5cm"/></style:style>')
    TABLE_COLUMN_STYLES.append('<style:style style:name="TitleMeta_Col_1" style:family="table-column"><style:table-column-properties style:column-width="3.8cm"/></style:style>')
    TABLE_COLUMN_STYLES.append('<style:style style:name="TitleMeta_Col_2" style:family="table-column"><style:table-column-properties style:column-width="7.7cm"/></style:style>')

    body_parts = []
    
    # 1. ТИТУЛЬНЫЙ ЛИСТ (Строго по шаблону методички АНО ПОО «КЭПиИТ»)
    body_parts.append(f'<text:p text:style-name="P_Title_Org_First">{esc(TITLE_DATA["org_line1"])}</text:p>')
    body_parts.append(f'<text:p text:style-name="P_Title_Org">{esc(TITLE_DATA["org_line2"])}</text:p>')
    body_parts.append(f'<text:p text:style-name="P_Title_Org">{esc(TITLE_DATA["org_line3"])}</text:p>')
    
    body_parts.append(f'<text:p text:style-name="P_Title_Project">{esc(TITLE_DATA["doc_type"])}</text:p>')
    body_parts.append(f'<text:p text:style-name="P_Title_Topic">{esc(TITLE_DATA["topic"])}</text:p>')
    body_parts.append(f'<text:p text:style-name="P_Title_Topic_Sub">{esc(TITLE_DATA["topic_sub"])}</text:p>')
    
    body_parts.append(render_title_page_meta_table())
    
    body_parts.append(f'<text:p text:style-name="P_Title_City">{esc(TITLE_DATA["city_year"])}</text:p>')
    
    # 2. СОДЕРЖАНИЕ (Page Break)
    body_parts.append('<text:p text:style-name="P_Heading_1_PB">СОДЕРЖАНИЕ</text:p>')
    for title, page in TOC_ITEMS:
        body_parts.append(f'<text:p text:style-name="P_TOC"><text:span>{esc(title)}</text:span><text:tab/><text:span>{esc(page)}</text:span></text:p>')
    
    # 3. ВВЕДЕНИЕ (Page Break)
    body_parts.append('<text:p text:style-name="P_Heading_1_PB">ВВЕДЕНИЕ</text:p>')
    for p in INTRO_PARAGRAPHS:
        body_parts.append(f'<text:p text:style-name="P_Body">{esc(p)}</text:p>')
        
    # 4. ГЛАВА 1 (Page Break)
    body_parts.append(f'<text:p text:style-name="P_Heading_1_PB">{esc(CHAPTER_1_TITLE)}</text:p>')
    
    # 1.1.
    body_parts.append(f'<text:p text:style-name="P_Heading_2">{esc(SEC_1_1_TITLE)}</text:p>')
    for p in SEC_1_1_TEXT:
        body_parts.append(f'<text:p text:style-name="P_Body">{esc(p)}</text:p>')
        
    # 1.2.
    body_parts.append(f'<text:p text:style-name="P_Heading_2">{esc(SEC_1_2_TITLE)}</text:p>')
    for p in SEC_1_2_TEXT:
        body_parts.append(f'<text:p text:style-name="P_Body">{esc(p)}</text:p>')
        
    # 1.3.
    body_parts.append(f'<text:p text:style-name="P_Heading_2">{esc(SEC_1_3_TITLE)}</text:p>')
    for p in SEC_1_3_TEXT:
        if p == "[[FIGURE_1]]":
            body_parts.append(make_fig_block("Pictures/idef0_as_is_a0_context.png",
                                             "Рисунок 1 – Контекстная диаграмма IDEF0 (А-0) процесса мониторинга «AS-IS» (До автоматизации)",
                                             width="15.5cm", height="10.3cm", fig_id=1))
        elif p == "[[FIGURE_2]]":
            body_parts.append(make_fig_block("Pictures/idef0_as_is_a0_decomp.png",
                                             "Рисунок 2 – Диаграмма декомпозиции первого уровня IDEF0 (А0) процесса «AS-IS»",
                                             width="15.5cm", height="10.3cm", fig_id=2))
        elif p == "[[FIGURE_3]]":
            body_parts.append(make_fig_block("Pictures/idef0_as_is_a2_decomp.png",
                                             "Рисунок 3 – Диаграмма декомпозиции второго уровня IDEF0 (А2) «Ручная проверка доступности узла» («AS-IS»)",
                                             width="15.5cm", height="10.3cm", fig_id=3))
        elif p == "[[FIGURE_4]]":
            body_parts.append(make_fig_block("Pictures/idef0_to_be_a0_context.png",
                                             "Рисунок 4 – Контекстная диаграмма IDEF0 (А-0) процесса мониторинга «TO-BE» в системе «Upward»",
                                             width="15.5cm", height="10.3cm", fig_id=4))
        elif p == "[[FIGURE_5]]":
            body_parts.append(make_fig_block("Pictures/idef0_to_be_a0_decomp.png",
                                             "Рисунок 5 – Диаграмма декомпозиции первого уровня IDEF0 (А0) процесса «TO-BE»",
                                             width="15.5cm", height="10.3cm", fig_id=5))
        elif p == "[[FIGURE_6]]":
            body_parts.append(make_fig_block("Pictures/idef0_to_be_a1_decomp.png",
                                             "Рисунок 6 – Диаграмма декомпозиции второго уровня IDEF0 (А1) «Регистрация и валидация ресурса» («TO-BE»)",
                                             width="15.5cm", height="10.3cm", fig_id=6))
        elif p == "[[FIGURE_7]]":
            body_parts.append(make_fig_block("Pictures/idef0_to_be_a2_decomp.png",
                                             "Рисунок 7 – Диаграмма декомпозиции второго уровня IDEF0 (А2) «Асинхронное распределенное зондирование» («TO-BE»)",
                                             width="15.5cm", height="10.3cm", fig_id=7))
        elif p.startswith("Таблица 1"):
            body_parts.append(f'<text:p text:style-name="P_Table_Caption">{esc(p)}</text:p>')
            body_parts.append(render_comparison_table())
        elif p.startswith("|"):
            continue
        else:
            body_parts.append(f'<text:p text:style-name="P_Body">{esc(p)}</text:p>')
        
    # 1.4.
    body_parts.append(f'<text:p text:style-name="P_Heading_2">{esc(SEC_1_4_TITLE)}</text:p>')
    for p in SEC_1_4_TEXT:
        if p.startswith("Таблица 2"):
            body_parts.append(f'<text:p text:style-name="P_Table_Caption">{esc(p)}</text:p>')
            body_parts.append(render_table_2())
        elif p.startswith("Таблица 3"):
            body_parts.append(f'<text:p text:style-name="P_Table_Caption">{esc(p)}</text:p>')
            body_parts.append(render_table_3())
        elif p.startswith("|"):
            continue
        else:
            body_parts.append(f'<text:p text:style-name="P_Body">{esc(p)}</text:p>')

    # 5. ГЛАВА 2 (Page Break)
    body_parts.append(f'<text:p text:style-name="P_Heading_1_PB">{esc(CHAPTER_2_TITLE)}</text:p>')
    
    # 2.1.
    body_parts.append(f'<text:p text:style-name="P_Heading_2">{esc(SEC_2_1_TITLE)}</text:p>')
    for p in SEC_2_1_TEXT:
        if p == "[[FIGURE_8]]":
            body_parts.append(make_fig_block("Pictures/db_schema_upward.png",
                                             "Рисунок 8 – Схема базы данных (ER-диаграмма и структура гипертаблицы TimescaleDB)",
                                             width="15.5cm", height="9.46cm", fig_id=8))
        else:
            body_parts.append(f'<text:p text:style-name="P_Body">{esc(p)}</text:p>')
        
    # 2.2.
    body_parts.append(f'<text:p text:style-name="P_Heading_2">{esc(SEC_2_2_TITLE)}</text:p>')
    for p in SEC_2_2_TEXT:
        if p.startswith("```rust") or p.startswith("```sql"):
            code_content = p.split("\n", 1)[1].rsplit("\n", 1)[0]
            for line in code_content.splitlines():
                body_parts.append(f'<text:p text:style-name="P_Code">{esc(line)}</text:p>')
        else:
            body_parts.append(f'<text:p text:style-name="P_Body">{esc(p)}</text:p>')
            
    # Embed Screenshots 9 and 10 in Section 2.2
    body_parts.append(make_fig_block("Pictures/swagger_overview.png",
                                     "Рисунок 9 – Общий вид интерактивной документации Swagger UI сервиса Uptime",
                                     width="14.5cm", height="12.42cm", fig_id=9))
    body_parts.append(make_fig_block("Pictures/swagger_sites_create_full.png",
                                     "Рисунок 10 – Спецификация параметров и ответов эндпоинта регистрации сайтов",
                                     width="14.5cm", height="12.56cm", fig_id=10))
    
    # 2.3.
    body_parts.append(f'<text:p text:style-name="P_Heading_2">{esc(SEC_2_3_TITLE)}</text:p>')
    for p in SEC_2_3_TEXT:
        if p.startswith("Таблица 4"):
            body_parts.append(f'<text:p text:style-name="P_Table_Caption">{esc(p)}</text:p>')
            body_parts.append(render_table_4())
        elif p.startswith("|"):
            continue
        else:
            body_parts.append(f'<text:p text:style-name="P_Body">{esc(p)}</text:p>')
            
    # 2.4.
    body_parts.append(f'<text:p text:style-name="P_Heading_2">{esc(SEC_2_4_TITLE)}</text:p>')
    for p in SEC_2_4_TEXT:
        if p == "[[FIGURE_11]]":
            body_parts.append(make_fig_block("Pictures/scheme_project_structure.png",
                                             "Рисунок 11 – Архитектурно-структурная схема монорепозитория «Upward»",
                                             width="15.5cm", height="10.33cm", fig_id=11))
        elif p.startswith("Таблица 5"):
            body_parts.append(f'<text:p text:style-name="P_Table_Caption">{esc(p)}</text:p>')
            body_parts.append(render_table_5())
        elif p.startswith("|"):
            continue
        elif p.startswith("```text") or p.startswith("```"):
            code_content = p.split("\n", 1)[1].rsplit("\n", 1)[0]
            for line in code_content.splitlines():
                body_parts.append(f'<text:p text:style-name="P_Code">{esc(line)}</text:p>')
        else:
            body_parts.append(f'<text:p text:style-name="P_Body">{esc(p)}</text:p>')
            
    # 6. ЗАКЛЮЧЕНИЕ (Page Break)
    body_parts.append(f'<text:p text:style-name="P_Heading_1_PB">{esc(CONCLUSION_TITLE)}</text:p>')
    for p in CONCLUSION_TEXT:
        body_parts.append(f'<text:p text:style-name="P_Body">{esc(p)}</text:p>')
        
    # 7. СПИСОК ИСТОЧНИКОВ (Page Break)
    body_parts.append(f'<text:p text:style-name="P_Heading_1_PB">{esc(BIBLIOGRAPHY_TITLE)}</text:p>')
    for num, item in BIBLIOGRAPHY_ITEMS:
        if item is None:
            body_parts.append(f'<text:p text:style-name="P_Heading_Bib_Sec">{esc(num)}</text:p>')
        else:
            body_parts.append(f'<text:p text:style-name="P_Bib_Item">{esc(num)}. {esc(item)}</text:p>')
            
    # 8. ПРИЛОЖЕНИЯ (Page Break)
    body_parts.append(f'<text:p text:style-name="P_Heading_1_PB">{esc(APPENDIX_A_TITLE)}</text:p>')
    for line in APPENDIX_A_CODE.splitlines():
        body_parts.append(f'<text:p text:style-name="P_Code">{esc(line)}</text:p>')
        
    body_parts.append(f'<text:p text:style-name="P_Heading_1_PB">{esc(APPENDIX_B_TITLE)}</text:p>')
    for line in APPENDIX_B_CODE.splitlines():
        body_parts.append(f'<text:p text:style-name="P_Code">{esc(line)}</text:p>')
        
    body_parts.append(f'<text:p text:style-name="P_Heading_1_PB">{esc(APPENDIX_C_TITLE)}</text:p>')
    for line in APPENDIX_C_CODE.splitlines():
        body_parts.append(f'<text:p text:style-name="P_Code">{esc(line)}</text:p>')

    body_xml = "\n".join(body_parts)
    column_styles_xml = "\n".join(TABLE_COLUMN_STYLES)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
 xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
 xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
 xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
 xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
 xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
 xmlns:xlink="http://www.w3.org/1999/xlink"
 xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
 office:version="1.3">
 
 <office:font-face-decls>
  <style:font-face style:name="Times New Roman" svg:font-family="&apos;Times New Roman&apos;" style:font-family-generic="roman" style:font-pitch="variable"/>
  <style:font-face style:name="Courier New" svg:font-family="&apos;Courier New&apos;" style:font-family-generic="modern" style:font-pitch="fixed"/>
 </office:font-face-decls>
 
 <office:automatic-styles>
  <!-- Стили колонок таблиц -->
{column_styles_xml}

  <!-- Основные стили абзацев -->
  <style:style style:name="P_Body" style:family="paragraph">
   <style:paragraph-properties fo:text-align="justify" fo:line-height="150%" fo:text-indent="1.25cm" fo:margin-top="0cm" fo:margin-bottom="0cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="14pt"/>
  </style:style>
  
  <!-- Стили титульного листа (АНО ПОО «КЭПиИТ») -->
  <style:style style:name="P_Title_Org_First" style:family="paragraph" style:master-page-name="First_Page">
   <style:paragraph-properties fo:text-align="center" fo:line-height="120%" fo:margin-top="0cm" fo:margin-bottom="0.1cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="12pt" fo:font-weight="bold"/>
  </style:style>

  <style:style style:name="P_Title_Org" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:line-height="120%" fo:margin-top="0cm" fo:margin-bottom="0.1cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="12pt" fo:font-weight="bold"/>
  </style:style>
  
  <style:style style:name="P_Title_Project" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:line-height="130%" fo:margin-top="2.0cm" fo:margin-bottom="0.4cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="16pt" fo:font-weight="bold"/>
  </style:style>

  <style:style style:name="P_Title_Topic" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:line-height="135%" fo:margin-top="0.2cm" fo:margin-bottom="0.1cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="14pt" fo:font-weight="bold"/>
  </style:style>

  <style:style style:name="P_Title_Topic_Sub" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:line-height="120%" fo:margin-top="0cm" fo:margin-bottom="1.2cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="10.5pt" fo:font-style="italic"/>
  </style:style>
  
  <style:style style:name="Table_Title_Meta" style:family="table">
   <style:table-properties fo:margin-top="0.5cm" fo:margin-bottom="0.8cm" table:align="margins" style:width="17.0cm"/>
  </style:style>

  <style:style style:name="Cell_Meta" style:family="table-cell">
   <style:table-cell-properties fo:padding-top="0.06cm" fo:padding-bottom="0.06cm" fo:padding-left="0.05cm" fo:padding-right="0.05cm" fo:border="none"/>
  </style:style>

  <style:style style:name="P_Meta_Label" style:family="paragraph">
   <style:paragraph-properties fo:text-align="start" fo:line-height="115%" fo:margin-top="0cm" fo:margin-bottom="0cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="11.5pt"/>
  </style:style>
  
  <style:style style:name="P_Meta_Val_Bold" style:family="paragraph">
   <style:paragraph-properties fo:text-align="start" fo:line-height="115%" fo:margin-top="0cm" fo:margin-bottom="0cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="11.5pt" fo:font-weight="bold"/>
  </style:style>

  <style:style style:name="P_Meta_Val_Center" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:line-height="115%" fo:margin-top="0cm" fo:margin-bottom="0cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="11.5pt"/>
  </style:style>

  <style:style style:name="P_Meta_Sub" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:line-height="100%" fo:margin-top="0cm" fo:margin-bottom="0.25cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="9pt" fo:font-style="italic"/>
  </style:style>

  <style:style style:name="P_Title_City" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:line-height="120%" fo:margin-top="1.8cm" fo:margin-bottom="0cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="13pt"/>
  </style:style>
  
  <!-- Заголовки разделов -->
  <style:style style:name="P_Heading_1_PB" style:family="paragraph" style:master-page-name="Standard">
   <style:paragraph-properties fo:text-align="center" fo:line-height="150%" fo:break-before="page" fo:keep-with-next="always" fo:margin-top="0.5cm" fo:margin-bottom="0.5cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="15pt" fo:font-weight="bold"/>
  </style:style>
  
  <style:style style:name="P_Heading_2" style:family="paragraph">
   <style:paragraph-properties fo:text-align="justify" fo:line-height="150%" fo:text-indent="1.25cm" fo:keep-with-next="always" fo:margin-top="0.4cm" fo:margin-bottom="0.3cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="14pt" fo:font-weight="bold"/>
  </style:style>
  
  <style:style style:name="P_Heading_Bib_Sec" style:family="paragraph">
   <style:paragraph-properties fo:text-align="start" fo:line-height="140%" fo:text-indent="1.25cm" fo:keep-with-next="always" fo:margin-top="0.4cm" fo:margin-bottom="0.2cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="13pt" fo:font-weight="bold"/>
  </style:style>
  
  <style:style style:name="P_TOC" style:family="paragraph">
   <style:paragraph-properties fo:text-align="justify" fo:line-height="140%" fo:margin-top="0.05cm" fo:margin-bottom="0.05cm">
    <style:tab-stops>
     <style:tab-stop style:position="17.0cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
    </style:tab-stops>
   </style:paragraph-properties>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="13pt"/>
  </style:style>
  
  <style:style style:name="P_Bib_Item" style:family="paragraph">
   <style:paragraph-properties fo:text-align="justify" fo:line-height="135%" fo:text-indent="1.25cm" fo:margin-top="0.1cm" fo:margin-bottom="0.1cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="13pt"/>
  </style:style>
  
  <!-- Стили подписей и ячеек таблиц -->
  <style:style style:name="P_Table_Caption" style:family="paragraph">
   <style:paragraph-properties fo:text-align="start" fo:line-height="130%" fo:text-indent="1.25cm" fo:keep-with-next="always" fo:margin-top="0.4cm" fo:margin-bottom="0.2cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="12pt" fo:font-weight="bold"/>
  </style:style>
  
  <style:style style:name="P_Table_Header" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:line-height="115%" fo:margin-top="0.05cm" fo:margin-bottom="0.05cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="10.5pt" fo:font-weight="bold"/>
  </style:style>
  
  <style:style style:name="P_Table_Text" style:family="paragraph">
   <style:paragraph-properties fo:text-align="start" fo:line-height="115%" fo:margin-top="0.05cm" fo:margin-bottom="0.05cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="10pt"/>
  </style:style>

  <style:style style:name="P_Table_Center" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:line-height="115%" fo:margin-top="0.05cm" fo:margin-bottom="0.05cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="10pt"/>
  </style:style>
  
  <!-- Листинги кода: Courier New, 10pt, строго БЕЗ фона -->
  <style:style style:name="P_Code" style:family="paragraph">
   <style:paragraph-properties fo:text-align="start" fo:line-height="115%" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:margin-left="0.5cm"/>
   <style:text-properties style:font-name="Courier New" fo:font-size="10pt"/>
  </style:style>
  
  <!-- Рисунки и графические объекты -->
  <style:style style:name="P_Fig_Image" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:margin-top="0.4cm" fo:margin-bottom="0.1cm"/>
  </style:style>
  
  <style:style style:name="P_Fig_Caption" style:family="paragraph">
   <style:paragraph-properties fo:text-align="center" fo:line-height="120%" fo:margin-top="0.1cm" fo:margin-bottom="0.5cm"/>
   <style:text-properties style:font-name="Times New Roman" fo:font-size="12pt" fo:font-style="italic"/>
  </style:style>

  <!-- Стили таблиц: четкие границы 0.5pt, выравнивание по ширине страницы 17.0 см -->
  <style:style style:name="Table_Bordered" style:family="table">
   <style:table-properties fo:margin-top="0.3cm" fo:margin-bottom="0.5cm" table:align="margins" style:width="17.0cm"/>
  </style:style>
  
  <style:style style:name="Cell_Header" style:family="table-cell">
   <style:table-cell-properties fo:background-color="#f1f5f9" fo:padding="0.18cm"
    fo:border="0.5pt solid #000000" style:vertical-align="middle"/>
  </style:style>
  
  <style:style style:name="Cell_Data" style:family="table-cell">
   <style:table-cell-properties fo:padding="0.15cm"
    fo:border="0.5pt solid #000000" style:vertical-align="middle"/>
  </style:style>

  <style:style style:name="Cell_Data_Center" style:family="table-cell">
   <style:table-cell-properties fo:padding="0.15cm"
    fo:border="0.5pt solid #000000" style:vertical-align="middle"/>
  </style:style>

  <style:style style:name="Graphic1" style:family="graphic">
   <style:graphic-properties style:horizontal-pos="center" style:horizontal-rel="paragraph" style:wrap="none"/>
  </style:style>
 </office:automatic-styles>

 <office:body>
  <office:text text:use-soft-page-breaks="true">
{body_xml}
  </office:text>
 </office:body>
</office:document-content>'''

def generate_odt():
    print(f"Generating coursework ODT -> {OUTPUT_ODT}")
    
    odt_buffer = io.BytesIO()
    with zipfile.ZipFile(odt_buffer, 'w', zipfile.ZIP_DEFLATED) as z:
        # 1. mimetype (MUST be first, uncompressed)
        z.writestr('mimetype', 'application/vnd.oasis.opendocument.text', compress_type=zipfile.ZIP_STORED)
        
        # 2. META-INF/manifest.xml
        z.writestr('META-INF/manifest.xml', make_manifest_xml())
        
        # 3. meta.xml
        z.writestr('meta.xml', make_meta_xml())
        
        # 4. styles.xml
        z.writestr('styles.xml', make_styles_xml())
        
        # 5. content.xml
        z.writestr('content.xml', make_content_xml())
        
        # 6. Images
        all_imgs = [
            ("Pictures/idef0_as_is_a0_context.png", "idef0_as_is_a0_context.png"),
            ("Pictures/idef0_as_is_a0_decomp.png", "idef0_as_is_a0_decomp.png"),
            ("Pictures/idef0_as_is_a2_decomp.png", "idef0_as_is_a2_decomp.png"),
            ("Pictures/idef0_to_be_a0_context.png", "idef0_to_be_a0_context.png"),
            ("Pictures/idef0_to_be_a0_decomp.png", "idef0_to_be_a0_decomp.png"),
            ("Pictures/idef0_to_be_a1_decomp.png", "idef0_to_be_a1_decomp.png"),
            ("Pictures/idef0_to_be_a2_decomp.png", "idef0_to_be_a2_decomp.png"),
            ("Pictures/db_schema_upward.png", "db_schema_upward.png"),
            ("Pictures/swagger_overview.png", "swagger_overview.png"),
            ("Pictures/swagger_sites_create_full.png", "swagger_sites_create_full.png"),
            ("Pictures/scheme_project_structure.png", "scheme_project_structure.png"),
        ]
        for dest, src in all_imgs:
            src_path = os.path.join(SCREENSHOTS_DIR, src)
            if os.path.exists(src_path):
                with open(src_path, "rb") as f:
                    z.writestr(dest, f.read())
                print(f"Added {dest} ({os.path.getsize(src_path)} bytes)")
            else:
                print(f"WARNING: image missing: {src_path}")

    with open(OUTPUT_ODT, "wb") as f:
        f.write(odt_buffer.getvalue())
        
    size_kb = len(odt_buffer.getvalue()) / 1024
    print(f"Coursework ODT successfully generated! Size: {size_kb:.1f} KB")

if __name__ == "__main__":
    generate_odt()

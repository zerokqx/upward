import os
import shutil
import glob
import subprocess
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, "Курсовая_работа_Шахсинов_Мурда.pdf")

pdftotext_bin = shutil.which("pdftotext")
if not pdftotext_bin:
    store_matches = glob.glob("/nix/store/*poppler-utils*/bin/pdftotext")
    if store_matches:
        pdftotext_bin = store_matches[0]
    else:
        pdftotext_bin = "pdftotext"

pdfinfo_bin = shutil.which("pdfinfo")
if not pdfinfo_bin:
    store_matches = glob.glob("/nix/store/*poppler-utils*/bin/pdfinfo")
    if store_matches:
        pdfinfo_bin = store_matches[0]
    else:
        pdfinfo_bin = "pdfinfo"

total_pages = 70
try:
    info_res = subprocess.run([pdfinfo_bin, PDF_PATH], capture_output=True, text=True)
    for line in info_res.stdout.splitlines():
        if "Pages:" in line:
            total_pages = int(re.search(r'\d+', line).group())
except Exception:
    pass

targets = [
    ("ВВЕДЕНИЕ", "ВВЕДЕНИЕ"),
    ("ГЛАВА 1. ПРЕДПРОЕКТНОЕ ИССЛЕДОВАНИЕ", "ГЛАВА 1. ПРЕДПРОЕКТНОЕ ИССЛЕДОВАНИЕ"),
    ("  1.1. Описание предметной области", "1.1. Описание предметной области"),
    ("  1.2. Описание технологии обработки задач", "1.2. Описание технологии обработки задач"),
    ("  1.3. Информационно-логическая модель и моделирование процессов в нотации IDEF0", "1.3. Информационно-логическая модель"),
    ("  1.4. Характеристика инструментальных средств разработки", "1.4. Характеристика инструментальных средств разработки"),
    ("ГЛАВА 2. РАБОЧИЙ ПРОЕКТ", "ГЛАВА 2. РАБОЧИЙ ПРОЕКТ"),
    ("  2.1. Анализ требований и разработка спецификаций", "2.1. Анализ требований и разработка спецификаций"),
    ("  2.2. Разработка веб-приложения распределенного мониторинга", "2.2. Разработка веб-приложения распределенного мониторинга"),
    ("  2.3. Отладка и тестирование веб-приложения", "2.3. Отладка и тестирование веб-приложения"),
    ("  2.4. Руководство программиста и эксплуатация", "2.4. Руководство программиста и эксплуатация"),
    ("ЗАКЛЮЧЕНИЕ", "ЗАКЛЮЧЕНИЕ"),
    ("СПИСОК ИСПОЛЬЗУЕМЫХ ИСТОЧНИКОВ", "СПИСОК ИСПОЛЬЗУЕМЫХ ИСТОЧНИКОВ"),
    ("ПРИЛОЖЕНИЕ А. Модуль фонового распределенного опроса целевых ресурсов", "ПРИЛОЖЕНИЕ А"),
    ("ПРИЛОЖЕНИЕ Б. Многоуровневый модуль сетевой безопасности, защиты от SSRF и потокового лимитирования", "ПРИЛОЖЕНИЕ Б"),
    ("ПРИЛОЖЕНИЕ В. Схема базы данных (DDL миграции PostgreSQL и TimescaleDB)", "ПРИЛОЖЕНИЕ В"),
]

found = {}
for p in range(3, total_pages + 1):
    res = subprocess.run([pdftotext_bin, "-f", str(p), "-l", str(p), PDF_PATH, "-"], capture_output=True, text=True)
    text = res.stdout
    for name, pattern in targets:
        if name not in found and pattern in text:
            found[name] = p

print('TOC_ITEMS = [')
for name, _ in targets:
    print(f'    ("{name}", "{found.get(name)}"),')
print(']')

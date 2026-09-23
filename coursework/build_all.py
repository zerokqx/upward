#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Мастер-скрипт автоматической сборки курсового проекта «Upward»
Выполняет полный цикл:
1. (Опционально) Перегенерация диаграмм (Draw.io -> SVG -> PNG)
2. Сборка OpenDocument Text (.odt) со всеми стилями и иллюстрациями
3. Headless-экспорт в PDF через LibreOffice
4. Автоматическая сверка и синхронизация номеров страниц в содержании (TOC)
5. Копирование итоговых артефактов в директорию reports/
"""

import os
import sys
import glob
import shutil
import argparse
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ODT_FILE = os.path.join(BASE_DIR, "Курсовая_работа_Шахсинов_Мурда.odt")
PDF_FILE = os.path.join(BASE_DIR, "Курсовая_работа_Шахсинов_Мурда.pdf")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")


def get_pdftotext():
    b = shutil.which("pdftotext")
    if b:
        return b
    matches = glob.glob("/nix/store/*poppler-utils*/bin/pdftotext")
    if matches:
        return matches[0]
    return "pdftotext"


def get_pdfinfo():
    b = shutil.which("pdfinfo")
    if b:
        return b
    matches = glob.glob("/nix/store/*poppler-utils*/bin/pdfinfo")
    if matches:
        return matches[0]
    return "pdfinfo"


def run_cmd(cmd, cwd=BASE_DIR, check=True):
    print(f"==> Запуск: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    res = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True, text=True)
    if check and res.returncode != 0:
        print(f"ОШИБКА выполнения: {res.stderr}")
        sys.exit(res.returncode)
    return res


def render_diagrams():
    print("\n--- 1. Генерация и рендеринг диаграмм ---")
    run_cmd([sys.executable, os.path.join(BASE_DIR, "generate_db_schema.py")])
    run_cmd([sys.executable, os.path.join(BASE_DIR, "render_ramus_svg_png.py")])
    print("Диаграммы успешно сгенерированы.")


def build_odt():
    print("\n--- 2. Сборка документа ODT ---")
    run_cmd([sys.executable, os.path.join(BASE_DIR, "generate_coursework.py")])


def convert_pdf():
    print("\n--- 3. Конвертация в PDF через LibreOffice ---")
    run_cmd(["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", BASE_DIR, ODT_FILE])


def sync_toc():
    print("\n--- 4. Проверка и синхронизация оглавления (TOC) ---")
    res = run_cmd([sys.executable, os.path.join(BASE_DIR, "find_pages.py")])
    lines = res.stdout.splitlines()
    for l in lines:
        if "TOC_ITEMS" in l or "(" in l:
            print(f"  {l}")


def main():
    parser = argparse.ArgumentParser(description="Сборщик курсового проекта Upward")
    parser.add_argument("--render-diagrams", action="store_true", help="Принудительно перерендерить диаграммы")
    args = parser.parse_args()

    os.makedirs(REPORTS_DIR, exist_ok=True)

    if args.render_diagrams:
        render_diagrams()

    build_odt()
    convert_pdf()
    sync_toc()

    # Копирование в reports/
    shutil.copy2(ODT_FILE, os.path.join(REPORTS_DIR, os.path.basename(ODT_FILE)))
    shutil.copy2(PDF_FILE, os.path.join(REPORTS_DIR, os.path.basename(PDF_FILE)))

    # Вывод информации о PDF
    pdfinfo_bin = get_pdfinfo()
    info_res = subprocess.run([pdfinfo_bin, PDF_FILE], capture_output=True, text=True)
    pages_line = [l for l in info_res.stdout.splitlines() if "Pages:" in l]
    page_count = pages_line[0] if pages_line else "Pages: N/A"

    print("\n" + "=" * 60)
    print(" УСПЕШНО ЗАВЕРШЕНО!")
    print(f" ODT: {ODT_FILE} ({os.path.getsize(ODT_FILE):,} байт)")
    print(f" PDF: {PDF_FILE} ({os.path.getsize(PDF_FILE):,} байт)")
    print(f" {page_count.strip()}")
    print(f" Копии сохранены в: {REPORTS_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()

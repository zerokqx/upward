#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор схемы базы данных (ER-диаграмма) в форматах:
1. Draw.io (.drawio XML)
2. SVG (векторный рендер высокого качества)
3. PNG (растровый рендер через headless Chromium)
Схема основана на реальных миграциях PostgreSQL / TimescaleDB сервиса Uptime
и подсистемы аутентификации Identify.
"""

import os
import subprocess
import html

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DRAWIO_PATH = os.path.join(BASE_DIR, "db_schema_upward.drawio")
SVG_PATH = os.path.join(BASE_DIR, "screenshots", "db_schema_upward.svg")
PNG_PATH = os.path.join(BASE_DIR, "screenshots", "db_schema_upward.png")

def generate_drawio_xml():
    xml = '''<mxfile host="app.diagrams.net" modified="2026-10-04T12:00:00.000Z" agent="Upward DB Schema Generator" version="21.6.8" type="device">
  <diagram id="db_schema_diagram" name="Схема базы данных (ERD)">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" background="#f8fafc">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- Заголовок -->
        <mxCell id="title" value="&lt;b style=&quot;font-size: 16px;&quot;&gt;СХЕМА БАЗЫ ДАННЫХ И ХРАНИЛИЩА ТЕЛЕМЕТРИИ СИСТЕМЫ «UPWARD»&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 12px; color: #475569;&quot;&gt;PostgreSQL 16 + Расширение TimescaleDB (Hypertables &amp; Data Retention) + Redis In-Memory Caches&lt;/span&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontFamily=Arial;" vertex="1" parent="1">
          <mxGeometry x="234" y="15" width="700" height="45" as="geometry"/>
        </mxCell>

        <!-- ==================== ТАБЛИЦА 1: SITES ==================== -->
        <mxCell id="tbl_sites_header" value="&lt;b&gt;sites (Реляционная таблица ресурсов)&lt;/b&gt;" style="swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#2563eb;strokeColor=#1d4ed8;fontColor=#ffffff;fontSize=13;fontFamily=Arial;" vertex="1" parent="1">
          <mxGeometry x="40" y="80" width="370" height="295" as="geometry"/>
        </mxCell>
        <mxCell id="site_f1" value="PK | id : UUID (gen_random_uuid())" style="text;strokeColor=none;fillColor=#eff6ff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;fontStyle=1;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="30" width="370" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="site_f2" value="     user_id : TEXT NOT NULL (Owner ID)" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="56" width="370" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="site_f3" value="     url : TEXT NOT NULL (http/https only)" style="text;strokeColor=none;fillColor=#f8fafc;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="82" width="370" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="site_f4" value="     created_at : TIMESTAMPTZ DEFAULT NOW()" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="108" width="370" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="site_f5" value="IX | last_check : TIMESTAMPTZ" style="text;strokeColor=none;fillColor=#f8fafc;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="134" width="370" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="site_f6" value="IX | status : VARCHAR(20) DEFAULT 'idle'" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="160" width="370" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="site_f7" value="IX | status_updated_at : TIMESTAMPTZ" style="text;strokeColor=none;fillColor=#f8fafc;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="186" width="370" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="site_f8" value="     active : BOOLEAN DEFAULT FALSE" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="212" width="370" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="site_f9" value="Индексы: sites_pkey, idx_sites_last_check, idx_sites_status_last_check" style="text;strokeColor=none;fillColor=#eff6ff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Arial;fontSize=9;fontColor=#475569;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="238" width="370" height="45" as="geometry"/>
        </mxCell>

        <!-- ==================== ТАБЛИЦА 2: SITE_PINGS ==================== -->
        <mxCell id="tbl_pings_header" value="&lt;b&gt;site_pings (TimescaleDB Hypertable)&lt;/b&gt;" style="swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#0d9488;strokeColor=#0f766e;fontColor=#ffffff;fontSize=13;fontFamily=Arial;" vertex="1" parent="1">
          <mxGeometry x="460" y="80" width="380" height="295" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f1" value="PK | time : TIMESTAMPTZ NOT NULL (Partition Key)" style="text;strokeColor=none;fillColor=#f0fdfa;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;fontStyle=1;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="30" width="380" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f2" value="FK | site_id : UUID NOT NULL (FK -> sites.id)" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;fontStyle=1;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="56" width="380" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f3" value="     duration_ms : DOUBLE PRECISION NOT NULL" style="text;strokeColor=none;fillColor=#f8fafc;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="82" width="380" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f4" value="     extra : JSONB (status_code, error, widgets)" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="108" width="380" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f5" value="TimescaleDB Свойства и Политики:" style="text;strokeColor=none;fillColor=#ccfbf1;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Arial;fontSize=10;fontStyle=1;fontColor=#0f766e;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="134" width="380" height="24" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f6" value="• create_hypertable('site_pings', 'time')" style="text;strokeColor=none;fillColor=#f0fdfa;align=left;verticalAlign=middle;spacingLeft=12;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Courier New;fontSize=10;fontColor=#0f766e;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="158" width="380" height="24" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f7" value="• add_retention_policy('site_pings', INTERVAL '30 days')" style="text;strokeColor=none;fillColor=#f0fdfa;align=left;verticalAlign=middle;spacingLeft=12;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Courier New;fontSize=10;fontColor=#0f766e;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="182" width="380" height="24" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f8" value="• ON DELETE CASCADE по внешнему ключу site_id" style="text;strokeColor=none;fillColor=#f0fdfa;align=left;verticalAlign=middle;spacingLeft=12;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Courier New;fontSize=10;fontColor=#0f766e;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="206" width="380" height="24" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f9" value="Автоматическое секционирование чанков по времени" style="text;strokeColor=none;fillColor=#ccfbf1;align=center;verticalAlign=middle;overflow=hidden;rotatable=0;fontFamily=Arial;fontSize=9;fontColor=#115e59;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="230" width="380" height="53" as="geometry"/>
        </mxCell>

        <!-- Связь SITES -> SITE_PINGS -->
        <mxCell id="rel_sites_pings" value="1 : N&lt;br&gt;(ON DELETE CASCADE)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0f766e;strokeWidth=2;fontSize=10;fontFamily=Arial;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="site_f1" target="ping_f2">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="435" y="123"/>
              <mxPoint x="435" y="149"/>
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- ==================== ТАБЛИЦА 3: FORBIDDEN_IP ==================== -->
        <mxCell id="tbl_fip_header" value="&lt;b&gt;forbidden_ip (Черный список SSRF)&lt;/b&gt;" style="swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#e11d48;strokeColor=#be123c;fontColor=#ffffff;fontSize=13;fontFamily=Arial;" vertex="1" parent="1">
          <mxGeometry x="40" y="405" width="370" height="175" as="geometry"/>
        </mxCell>
        <mxCell id="fip_f1" value="PK | id : BIGSERIAL" style="text;strokeColor=none;fillColor=#fff1f2;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;fontStyle=1;" vertex="1" parent="tbl_fip_header">
          <mxGeometry y="30" width="370" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="fip_f2" value="UQ | ip : TEXT NOT NULL (IP / CIDR)" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;fontStyle=1;" vertex="1" parent="tbl_fip_header">
          <mxGeometry y="56" width="370" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="fip_f3" value="     created_at : TIMESTAMPTZ DEFAULT NOW()" style="text;strokeColor=none;fillColor=#f8fafc;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_fip_header">
          <mxGeometry y="82" width="370" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="fip_f4" value="Индекс: UNIQUE idx_forbidden_ip_ip ON forbidden_ip(ip)" style="text;strokeColor=none;fillColor=#ffe4e6;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Courier New;fontSize=9;fontColor=#9f1239;" vertex="1" parent="tbl_fip_header">
          <mxGeometry y="108" width="370" height="28" as="geometry"/>
        </mxCell>
        <mxCell id="fip_f5" value="Мгновенное отсечение приватных и скомпрометированных адресов" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Arial;fontSize=9;fontColor=#475569;" vertex="1" parent="tbl_fip_header">
          <mxGeometry y="136" width="370" height="34" as="geometry"/>
        </mxCell>

        <!-- ==================== ТАБЛИЦА 4: WIDGETS ==================== -->
        <mxCell id="tbl_widgets_header" value="&lt;b&gt;widgets (Справочник UI-виджетов телеметрии)&lt;/b&gt;" style="swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#7c3aed;strokeColor=#6d28d9;fontColor=#ffffff;fontSize=13;fontFamily=Arial;" vertex="1" parent="1">
          <mxGeometry x="460" y="405" width="380" height="175" as="geometry"/>
        </mxCell>
        <mxCell id="wid_f1" value="PK | id : SMALLSERIAL" style="text;strokeColor=none;fillColor=#f5f3ff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;fontStyle=1;" vertex="1" parent="tbl_widgets_header">
          <mxGeometry y="30" width="380" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="wid_f2" value="UQ | name : VARCHAR(100) NOT NULL UNIQUE" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;fontStyle=1;" vertex="1" parent="tbl_widgets_header">
          <mxGeometry y="56" width="380" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="wid_f3" value="     created_at : TIMESTAMPTZ DEFAULT NOW()" style="text;strokeColor=none;fillColor=#f8fafc;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_widgets_header">
          <mxGeometry y="82" width="380" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="wid_f4" value="Типы: badge, stat, gauge, sparkline, key_value, chart, row, col, text" style="text;strokeColor=none;fillColor=#ede9fe;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Courier New;fontSize=9;fontColor=#5b21b6;" vertex="1" parent="tbl_widgets_header">
          <mxGeometry y="108" width="380" height="28" as="geometry"/>
        </mxCell>
        <mxCell id="wid_f5" value="Валидация JSON-полей extra в validate_ping_widgets при опросе /upward" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Arial;fontSize=9;fontColor=#475569;" vertex="1" parent="tbl_widgets_header">
          <mxGeometry y="136" width="380" height="34" as="geometry"/>
        </mxCell>

        <!-- Связь WIDGETS -> SITE_PINGS (Валидация типов виджетов) -->
        <mxCell id="rel_wid_pings" value="Валидация extra" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#7c3aed;strokeWidth=1.5;fontSize=10;fontFamily=Arial;labelBackgroundColor=#ffffff;dashed=1;" edge="1" parent="1" source="wid_f2" target="ping_f4">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="850" y="474"/>
              <mxPoint x="850" y="201"/>
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- ==================== СУЩНОСТЬ 5: REDIS ==================== -->
        <mxCell id="tbl_redis_header" value="&lt;b&gt;Redis In-Memory (HTTP-01 Challenge &amp; Refresh Token Rotation)&lt;/b&gt;" style="swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#ea580c;strokeColor=#c2410c;fontColor=#ffffff;fontSize=13;fontFamily=Arial;" vertex="1" parent="1">
          <mxGeometry x="40" y="605" width="800" height="160" as="geometry"/>
        </mxCell>
        <mxCell id="red_f1" value="UPTIME CHALLENGE | KEY: challenge:{site_id}:{token} | TTL: 86400s (24h) | PATH: /upward" style="text;strokeColor=none;fillColor=#fff7ed;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=10.5;fontStyle=1;" vertex="1" parent="tbl_redis_header">
          <mxGeometry y="30" width="800" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="red_f2" value="IDENTIFY REFRESH  | KEY: refresh:{uuid} -> user_id  | TTL: 2592000s (30d) | Атомарная ротация GETDEL" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=10.5;fontStyle=1;" vertex="1" parent="tbl_redis_header">
          <mxGeometry y="56" width="800" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="red_f3" value="• Двухэтапная верификация: сайт регистрируется как active=false, после опроса {url}/upward активируется" style="text;strokeColor=none;fillColor=#fff7ed;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Arial;fontSize=9.5;fontColor=#9a3412;" vertex="1" parent="tbl_redis_header">
          <mxGeometry y="82" width="800" height="24" as="geometry"/>
        </mxCell>
        <mxCell id="red_f4" value="• Refresh Token Rotation: защита от перехвата сессий (при обновлении старый токен сжигается атомарным GETDEL)" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Arial;fontSize=9.5;fontColor=#9a3412;" vertex="1" parent="tbl_redis_header">
          <mxGeometry y="106" width="800" height="24" as="geometry"/>
        </mxCell>
        <mxCell id="red_f5" value="• Разделение инстансов: uptime-redis (порт 6379, challenge-токены) и identify-redis (порт 6380, сессии пользователей)" style="text;strokeColor=none;fillColor=#fff7ed;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Arial;fontSize=9.5;fontColor=#9a3412;" vertex="1" parent="tbl_redis_header">
          <mxGeometry y="130" width="800" height="24" as="geometry"/>
        </mxCell>

        <!-- ==================== БЛОК ПОЯСНЕНИЙ СПРАВА ==================== -->
        <mxCell id="notes_box" value="&lt;b&gt;АРХИТЕКТУРНЫЕ ОСОБЕННОСТИ&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;b&gt;1. Атомарность захвата:&lt;/b&gt;&lt;br&gt;Выборка сайтов воркерами выполняется через CTE с директивой &lt;i&gt;FOR UPDATE SKIP LOCKED&lt;/i&gt;, исключающей race conditions между репликами.&lt;br&gt;&lt;br&gt;&lt;b&gt;2. Dead Worker Recovery:&lt;/b&gt;&lt;br&gt;Поле &lt;i&gt;status_updated_at&lt;/i&gt; возвращает зависшие задачи в статус 'idle' через 3 минуты.&lt;br&gt;&lt;br&gt;&lt;b&gt;3. Time-Series Hypertable:&lt;/b&gt;&lt;br&gt;Таблица &lt;i&gt;site_pings&lt;/i&gt; партиционируется TimescaleDB по времени &lt;i&gt;time&lt;/i&gt;. Устаревшие чанки старше 30 дней удаляются мгновенно без блокировок.&lt;br&gt;&lt;br&gt;&lt;b&gt;4. Справочник UI-виджетов:&lt;/b&gt;&lt;br&gt;Каталог &lt;i&gt;widgets&lt;/i&gt; динамически валидирует структуру JSON-телеметрии протокола &lt;i&gt;/upward&lt;/i&gt;.&lt;br&gt;&lt;br&gt;&lt;b&gt;5. Многоуровневый SSRF-фильтр:&lt;/b&gt;&lt;br&gt;Запросы к loopback, RFC 1918 и адресам из &lt;i&gt;forbidden_ip&lt;/i&gt; отклоняются до открытия TCP-сокета.&lt;br&gt;&lt;br&gt;&lt;b&gt;6. Сессионная безопасность:&lt;/b&gt;&lt;br&gt;Асимметричные токены RS256 в паре с одноразовыми Refresh-токенами в Redis (GETDEL)." style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#cbd5e1;strokeWidth=1.5;align=left;verticalAlign=top;spacing=12;fontFamily=Arial;fontSize=10.5;lineHeight=1.35;" vertex="1" parent="1">
          <mxGeometry x="870" y="80" width="270" height="685" as="geometry"/>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    return xml

def generate_svg():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 800" width="1180" height="800" style="background:#f8fafc; font-family:'Segoe UI', Arial, sans-serif;">
  <defs>
    <filter id="shadow" x="-3%" y="-3%" width="106%" height="108%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.07"/>
    </filter>
    <marker id="arrow-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#0f766e"/>
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#ea580c"/>
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#7c3aed"/>
    </marker>
  </defs>

  <!-- Title Banner -->
  <rect x="30" y="15" width="1120" height="55" rx="8" fill="#1e293b" filter="url(#shadow)"/>
  <text x="590" y="39" fill="#ffffff" font-size="16" font-weight="bold" text-anchor="middle">СХЕМА БАЗЫ ДАННЫХ И ХРАНИЛИЩА ТЕЛЕМЕТРИИ СИСТЕМЫ «UPWARD»</text>
  <text x="590" y="58" fill="#94a3b8" font-size="11.5" text-anchor="middle">PostgreSQL 16 + Расширение TimescaleDB (Hypertables &amp; Data Retention) + Redis In-Memory Caches</text>

  <!-- ==================== ТАБЛИЦА SITES ==================== -->
  <g transform="translate(40, 85)" filter="url(#shadow)">
    <!-- Header -->
    <rect x="0" y="0" width="380" height="32" rx="6" fill="#2563eb"/>
    <rect x="0" y="26" width="380" height="6" fill="#2563eb"/>
    <text x="190" y="21" fill="#ffffff" font-size="12.5" font-weight="bold" text-anchor="middle">sites (Реляционная таблица ресурсов)</text>
    
    <!-- Body -->
    <rect x="0" y="32" width="380" height="268" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    
    <!-- Row 1: id -->
    <rect x="0" y="32" width="380" height="26" fill="#eff6ff"/>
    <text x="12" y="49" fill="#1d4ed8" font-size="10.5" font-weight="bold" font-family="'Courier New', monospace">PK | id : UUID DEFAULT gen_random_uuid()</text>
    
    <!-- Row 2: user_id -->
    <rect x="0" y="58" width="380" height="26" fill="#ffffff"/>
    <text x="12" y="75" fill="#0f172a" font-size="10.5" font-family="'Courier New', monospace">     user_id : TEXT NOT NULL (Owner ID)</text>
    
    <!-- Row 3: url -->
    <rect x="0" y="84" width="380" height="26" fill="#f8fafc"/>
    <text x="12" y="101" fill="#0f172a" font-size="10.5" font-family="'Courier New', monospace">     url : TEXT NOT NULL (http / https only)</text>
    
    <!-- Row 4: created_at -->
    <rect x="0" y="110" width="380" height="26" fill="#ffffff"/>
    <text x="12" y="127" fill="#0f172a" font-size="10.5" font-family="'Courier New', monospace">     created_at : TIMESTAMPTZ DEFAULT NOW()</text>
    
    <!-- Row 5: last_check -->
    <rect x="0" y="136" width="380" height="26" fill="#f8fafc"/>
    <text x="12" y="153" fill="#0369a1" font-size="10.5" font-weight="bold" font-family="'Courier New', monospace">IX | last_check : TIMESTAMPTZ</text>
    
    <!-- Row 6: status -->
    <rect x="0" y="162" width="380" height="26" fill="#ffffff"/>
    <text x="12" y="179" fill="#0369a1" font-size="10.5" font-weight="bold" font-family="'Courier New', monospace">IX | status : VARCHAR(20) DEFAULT 'idle'</text>
    
    <!-- Row 7: status_updated_at -->
    <rect x="0" y="188" width="380" height="26" fill="#f8fafc"/>
    <text x="12" y="205" fill="#0369a1" font-size="10.5" font-weight="bold" font-family="'Courier New', monospace">IX | status_updated_at : TIMESTAMPTZ</text>
    
    <!-- Row 8: active -->
    <rect x="0" y="214" width="380" height="26" fill="#ffffff"/>
    <text x="12" y="231" fill="#0f172a" font-size="10.5" font-family="'Courier New', monospace">     active : BOOLEAN DEFAULT FALSE</text>
    
    <!-- Indexes info footer -->
    <rect x="0" y="240" width="380" height="60" rx="0" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
    <text x="12" y="256" fill="#475569" font-size="9" font-weight="bold">ИНДЕКСЫ ТАБЛИЦЫ:</text>
    <text x="12" y="271" fill="#64748b" font-size="8.5" font-family="'Courier New', monospace">• idx_sites_last_check (last_check ASC NULLS FIRST)</text>
    <text x="12" y="285" fill="#64748b" font-size="8.5" font-family="'Courier New', monospace">• idx_sites_status_last_check (status, last_check)</text>
  </g>

  <!-- ==================== ТАБЛИЦА SITE_PINGS (HYPERTABLE) ==================== -->
  <g transform="translate(460, 85)" filter="url(#shadow)">
    <!-- Header -->
    <rect x="0" y="0" width="380" height="32" rx="6" fill="#0d9488"/>
    <rect x="0" y="26" width="380" height="6" fill="#0d9488"/>
    <text x="190" y="21" fill="#ffffff" font-size="12.5" font-weight="bold" text-anchor="middle">site_pings (TimescaleDB Hypertable)</text>
    
    <!-- Body -->
    <rect x="0" y="32" width="380" height="268" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    
    <!-- Row 1: time (PK, Partition) -->
    <rect x="0" y="32" width="380" height="26" fill="#f0fdfa"/>
    <text x="12" y="49" fill="#0f766e" font-size="10.5" font-weight="bold" font-family="'Courier New', monospace">PK | time : TIMESTAMPTZ (Partition Key)</text>
    
    <!-- Row 2: site_id (FK) -->
    <rect x="0" y="58" width="380" height="26" fill="#ffffff"/>
    <text x="12" y="75" fill="#0f766e" font-size="10.5" font-weight="bold" font-family="'Courier New', monospace">FK | site_id : UUID (FK -&gt; sites.id)</text>
    
    <!-- Row 3: duration_ms -->
    <rect x="0" y="84" width="380" height="26" fill="#f8fafc"/>
    <text x="12" y="101" fill="#0f172a" font-size="10.5" font-family="'Courier New', monospace">     duration_ms : DOUBLE PRECISION NOT NULL</text>
    
    <!-- Row 4: extra -->
    <rect x="0" y="110" width="380" height="26" fill="#ffffff"/>
    <text x="12" y="127" fill="#0f172a" font-size="10.5" font-family="'Courier New', monospace">     extra : JSONB (http_code, error, widgets)</text>
    
    <!-- TimescaleDB Features Box -->
    <rect x="0" y="136" width="380" height="164" fill="#f0fdfa" stroke="#99f6e4" stroke-width="1"/>
    <text x="12" y="156" fill="#0f766e" font-size="10" font-weight="bold">СВОЙСТВА И ПОЛИТИКИ TIMESCALEDB:</text>
    
    <rect x="10" y="165" width="360" height="26" rx="4" fill="#ffffff" stroke="#ccfbf1"/>
    <text x="18" y="182" fill="#115e59" font-size="9" font-family="'Courier New', monospace">SELECT create_hypertable('site_pings', 'time');</text>
    
    <rect x="10" y="196" width="360" height="26" rx="4" fill="#ffffff" stroke="#ccfbf1"/>
    <text x="18" y="213" fill="#115e59" font-size="9" font-family="'Courier New', monospace">SELECT add_retention_policy(..., '30 days');</text>
    
    <text x="12" y="238" fill="#475569" font-size="9">• Секционирование: автоматические чанки по временной оси</text>
    <text x="12" y="254" fill="#475569" font-size="9">• Каскадное удаление: ON DELETE CASCADE при удалении сайта</text>
    <text x="12" y="270" fill="#475569" font-size="9">• Пакетная запись: QueryBuilder вставляет сотни строк в 1 транзакцию</text>
  </g>

  <!-- ==================== СВЯЗЬ SITES -> SITE_PINGS ==================== -->
  <path d="M 420 152 L 460 152" fill="none" stroke="#0f766e" stroke-width="2.5" marker-end="url(#arrow-teal)"/>
  <rect x="424" y="138" width="32" height="16" rx="3" fill="#ffffff" stroke="#0f766e"/>
  <text x="440" y="150" fill="#0f766e" font-size="8.5" font-weight="bold" text-anchor="middle">1:N</text>

  <!-- ==================== ТАБЛИЦА FORBIDDEN_IP ==================== -->
  <g transform="translate(40, 405)" filter="url(#shadow)">
    <!-- Header -->
    <rect x="0" y="0" width="380" height="32" rx="6" fill="#e11d48"/>
    <rect x="0" y="26" width="380" height="6" fill="#e11d48"/>
    <text x="190" y="21" fill="#ffffff" font-size="12.5" font-weight="bold" text-anchor="middle">forbidden_ip (Черный список адресов SSRF)</text>
    
    <!-- Body -->
    <rect x="0" y="32" width="380" height="150" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    
    <!-- Row 1: id -->
    <rect x="0" y="32" width="380" height="26" fill="#fff1f2"/>
    <text x="12" y="49" fill="#be123c" font-size="10.5" font-weight="bold" font-family="'Courier New', monospace">PK | id : BIGSERIAL PRIMARY KEY</text>
    
    <!-- Row 2: ip -->
    <rect x="0" y="58" width="380" height="26" fill="#ffffff"/>
    <text x="12" y="75" fill="#be123c" font-size="10.5" font-weight="bold" font-family="'Courier New', monospace">UQ | ip : TEXT NOT NULL (IPv4 / IPv6 / CIDR)</text>
    
    <!-- Row 3: created_at -->
    <rect x="0" y="84" width="380" height="26" fill="#f8fafc"/>
    <text x="12" y="101" fill="#0f172a" font-size="10.5" font-family="'Courier New', monospace">     created_at : TIMESTAMPTZ DEFAULT NOW()</text>
    
    <!-- Details -->
    <rect x="0" y="110" width="380" height="72" fill="#fff1f2" stroke="#fecdd3" stroke-width="1"/>
    <text x="12" y="126" fill="#9f1239" font-size="9" font-weight="bold">НАЗНАЧЕНИЕ: Защита периметра от SSRF атак</text>
    <text x="12" y="141" fill="#475569" font-size="8.5">• Блокирует: Loopback (127.0.0.1), RFC 1918 (10.0/8, 172.16/12, 192.168/16)</text>
    <text x="12" y="156" fill="#475569" font-size="8.5">• Проверка в IpValidator: предварительный DNS-резолвинг до сокета</text>
    <text x="12" y="171" fill="#be123c" font-size="8.5" font-weight="bold">• Защита от DNS Rebinding через привязку к проверенным IP</text>
  </g>

  <!-- ==================== ТАБЛИЦА WIDGETS ==================== -->
  <g transform="translate(460, 405)" filter="url(#shadow)">
    <!-- Header -->
    <rect x="0" y="0" width="380" height="32" rx="6" fill="#7c3aed"/>
    <rect x="0" y="26" width="380" height="6" fill="#7c3aed"/>
    <text x="190" y="21" fill="#ffffff" font-size="12.5" font-weight="bold" text-anchor="middle">widgets (Справочник UI-виджетов телеметрии)</text>
    
    <!-- Body -->
    <rect x="0" y="32" width="380" height="150" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    
    <!-- Row 1: id -->
    <rect x="0" y="32" width="380" height="26" fill="#f5f3ff"/>
    <text x="12" y="49" fill="#6d28d9" font-size="10.5" font-weight="bold" font-family="'Courier New', monospace">PK | id : SMALLSERIAL PRIMARY KEY</text>
    
    <!-- Row 2: name -->
    <rect x="0" y="58" width="380" height="26" fill="#ffffff"/>
    <text x="12" y="75" fill="#6d28d9" font-size="10.5" font-weight="bold" font-family="'Courier New', monospace">UQ | name : VARCHAR(100) NOT NULL UNIQUE</text>
    
    <!-- Row 3: created_at -->
    <rect x="0" y="84" width="380" height="26" fill="#f8fafc"/>
    <text x="12" y="101" fill="#0f172a" font-size="10.5" font-family="'Courier New', monospace">     created_at : TIMESTAMPTZ DEFAULT NOW()</text>
    
    <!-- Details -->
    <rect x="0" y="110" width="380" height="72" fill="#f5f3ff" stroke="#ddd6fe" stroke-width="1"/>
    <text x="12" y="126" fill="#5b21b6" font-size="9" font-weight="bold">РАЗРЕШЕННЫЕ ВИДЖЕТЫ ПРОТОКОЛА /upward:</text>
    <text x="12" y="141" fill="#475569" font-size="8.5">• badge, stat, gauge, sparkline, key_value, chart, row, column, text</text>
    <text x="12" y="156" fill="#475569" font-size="8.5">• Строгая валидация в validate_ping_widgets перед вставкой в БД</text>
    <text x="12" y="171" fill="#6d28d9" font-size="8.5" font-weight="bold">• Ограничение размера ответа MAX_PAYLOAD_BYTES (512 КБ)</text>
  </g>

  <!-- ==================== СВЯЗЬ WIDGETS -> SITE_PINGS ==================== -->
  <path d="M 840 470 L 855 470 L 855 200 L 840 200" fill="none" stroke="#7c3aed" stroke-width="1.8" stroke-dasharray="4 3" marker-end="url(#arrow-purple)"/>
  <rect x="836" y="325" width="40" height="16" rx="3" fill="#ffffff" stroke="#7c3aed"/>
  <text x="856" y="337" fill="#7c3aed" font-size="8" font-weight="bold" text-anchor="middle">extra</text>

  <!-- ==================== СУЩНОСТЬ REDIS CACHE ==================== -->
  <g transform="translate(40, 595)" filter="url(#shadow)">
    <!-- Header -->
    <rect x="0" y="0" width="800" height="32" rx="6" fill="#ea580c"/>
    <rect x="0" y="26" width="800" height="6" fill="#ea580c"/>
    <text x="400" y="21" fill="#ffffff" font-size="12.5" font-weight="bold" text-anchor="middle">Redis In-Memory Key-Value Caches (HTTP-01 Challenge &amp; Refresh Token Rotation)</text>
    
    <!-- Body -->
    <rect x="0" y="32" width="800" height="138" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    
    <!-- Left Column: Uptime Challenge -->
    <rect x="10" y="40" width="380" height="120" rx="4" fill="#fff7ed" stroke="#fed7aa"/>
    <text x="20" y="58" fill="#9a3412" font-size="10.5" font-weight="bold">1. UPTIME: HTTP-01 CHALLENGE (Порт: 6379)</text>
    <text x="20" y="78" fill="#c2410c" font-size="9.5" font-family="'Courier New', monospace">KEY: challenge:{site_id}:{token}</text>
    <text x="20" y="94" fill="#0f172a" font-size="9">VAL: UUIDv4 (128-bit) | TTL: 86400с (24 часа)</text>
    <text x="20" y="110" fill="#475569" font-size="8.5">• Протокол: опрос {target_url}/upward на сервере владельца</text>
    <text x="20" y="126" fill="#475569" font-size="8.5">• При подтверждении токена: ключ удаляется, active = true</text>
    <text x="20" y="142" fill="#c2410c" font-size="8.5" font-weight="bold">Защищает от несанкционированного мониторинга чужих сайтов</text>

    <!-- Right Column: Identify Session -->
    <rect x="410" y="40" width="380" height="120" rx="4" fill="#eff6ff" stroke="#bfdbfe"/>
    <text x="420" y="58" fill="#1e40af" font-size="10.5" font-weight="bold">2. IDENTIFY: REFRESH TOKEN ROTATION (Порт: 6380)</text>
    <text x="420" y="78" fill="#1d4ed8" font-size="9.5" font-family="'Courier New', monospace">KEY: refresh:{refresh_token_uuid}</text>
    <text x="420" y="94" fill="#0f172a" font-size="9">VAL: user_id (UUID) | TTL: 2 592 000с (30 суток)</text>
    <text x="420" y="110" fill="#475569" font-size="8.5">• Атомарная ротация: операция Redis GETDEL при /auth/refresh</text>
    <text x="420" y="126" fill="#475569" font-size="8.5">• Исключает повторное использование токена при перехвате</text>
    <text x="420" y="142" fill="#1d4ed8" font-size="8.5" font-weight="bold">Интеграция с RS256 JWT (Access Token со сроком 15 мин)</text>
  </g>

  <!-- ==================== ПАНЕЛЬ АРХИТЕКТУРНЫХ ОСОБЕННОСТЕЙ СПРАВА ==================== -->
  <g transform="translate(865, 85)" filter="url(#shadow)">
    <rect x="0" y="0" width="275" height="650" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="0" y="0" width="275" height="32" rx="8" fill="#334155"/>
    <rect x="0" y="26" width="275" height="6" fill="#334155"/>
    <text x="137" y="21" fill="#ffffff" font-size="11.5" font-weight="bold" text-anchor="middle">ИНЖЕНЕРНЫЕ РЕШЕНИЯ БД</text>
    
    <g transform="translate(15, 42)">
      <!-- Item 1 -->
      <circle cx="8" cy="8" r="8" fill="#2563eb"/>
      <text x="8" y="12" fill="#ffffff" font-size="9.5" font-weight="bold" text-anchor="middle">1</text>
      <text x="24" y="12" fill="#0f172a" font-size="10.5" font-weight="bold">Атомарная блокировка CTE</text>
      <text x="24" y="28" fill="#475569" font-size="9">Запрос FOR UPDATE SKIP</text>
      <text x="24" y="42" fill="#475569" font-size="9">LOCKED захватывает батч</text>
      <text x="24" y="56" fill="#475569" font-size="9">сайтов без race condition.</text>

      <!-- Item 2 -->
      <circle cx="8" cy="80" r="8" fill="#0284c7"/>
      <text x="8" y="84" fill="#ffffff" font-size="9.5" font-weight="bold" text-anchor="middle">2</text>
      <text x="24" y="84" fill="#0f172a" font-size="10.5" font-weight="bold">Dead Worker Recovery</text>
      <text x="24" y="100" fill="#475569" font-size="9">Поле status_updated_at</text>
      <text x="24" y="114" fill="#475569" font-size="9">возвращает зависшие задачи</text>
      <text x="24" y="128" fill="#475569" font-size="9">в статус 'idle' через 3 мин.</text>

      <!-- Item 3 -->
      <circle cx="8" cy="152" r="8" fill="#0f766e"/>
      <text x="8" y="156" fill="#ffffff" font-size="9.5" font-weight="bold" text-anchor="middle">3</text>
      <text x="24" y="156" fill="#0f172a" font-size="10.5" font-weight="bold">TimescaleDB Hypertables</text>
      <text x="24" y="172" fill="#475569" font-size="9">Метрики задержек (RTT)</text>
      <text x="24" y="186" fill="#475569" font-size="9">сохраняются в гипертаблицу.</text>
      <text x="24" y="200" fill="#475569" font-size="9">Авто-удаление через 30 дней</text>
      <text x="24" y="214" fill="#475569" font-size="9">исключает фрагментацию диска.</text>

      <!-- Item 4 -->
      <circle cx="8" cy="238" r="8" fill="#7c3aed"/>
      <text x="8" y="242" fill="#ffffff" font-size="9.5" font-weight="bold" text-anchor="middle">4</text>
      <text x="24" y="242" fill="#0f172a" font-size="10.5" font-weight="bold">Справочник UI-виджетов</text>
      <text x="24" y="258" fill="#475569" font-size="9">Таблица widgets задает белый</text>
      <text x="24" y="272" fill="#475569" font-size="9">список типов виджетов,</text>
      <text x="24" y="286" fill="#475569" font-size="9">защищая от невалидного JSON.</text>

      <!-- Item 5 -->
      <circle cx="8" cy="310" r="8" fill="#e11d48"/>
      <text x="8" y="314" fill="#ffffff" font-size="9.5" font-weight="bold" text-anchor="middle">5</text>
      <text x="24" y="314" fill="#0f172a" font-size="10.5" font-weight="bold">Пакетная вставка (Batch)</text>
      <text x="24" y="330" fill="#475569" font-size="9">QueryBuilder вставляет до 500</text>
      <text x="24" y="344" fill="#475569" font-size="9">замеров в 1 SQL-запрос</text>
      <text x="24" y="358" fill="#475569" font-size="9">за 5–8 мс без нагрузки пула.</text>

      <!-- Item 6 -->
      <circle cx="8" cy="382" r="8" fill="#ea580c"/>
      <text x="8" y="386" fill="#ffffff" font-size="9.5" font-weight="bold" text-anchor="middle">6</text>
      <text x="24" y="386" fill="#0f172a" font-size="10.5" font-weight="bold">SSRF и Rebinding фильтр</text>
      <text x="24" y="402" fill="#475569" font-size="9">DNS-проверка, черные списки</text>
      <text x="24" y="416" fill="#475569" font-size="9">и привязка сокета resolve_to</text>
      <text x="24" y="430" fill="#475569" font-size="9">блокируют атаки на периметр.</text>

      <!-- Item 7 -->
      <circle cx="8" cy="454" r="8" fill="#16a34a"/>
      <text x="8" y="458" fill="#ffffff" font-size="9.5" font-weight="bold" text-anchor="middle">7</text>
      <text x="24" y="458" fill="#0f172a" font-size="10.5" font-weight="bold">Потоковый лимит 512 КБ</text>
      <text x="24" y="474" fill="#475569" font-size="9">Контроль Content-Length и</text>
      <text x="24" y="488" fill="#475569" font-size="9">потока bytes_stream исключает</text>
      <text x="24" y="502" fill="#475569" font-size="9">переполнение памяти (DoS).</text>
      
      <!-- Summary Box -->
      <rect x="0" y="530" width="245" height="52" rx="6" fill="#f8fafc" stroke="#e2e8f0"/>
      <text x="122" y="550" fill="#0f172a" font-size="9.5" font-weight="bold" text-anchor="middle">ПРОПУСКНАЯ СПОСОБНОСТЬ</text>
      <text x="122" y="568" fill="#16a34a" font-size="11" font-weight="bold" text-anchor="middle">&gt; 10 000 проверок / мин</text>
    </g>
  </g>

</svg>'''
    return svg

def main():
    print("1. Generating Draw.io XML...")
    with open(DRAWIO_PATH, "w", encoding="utf-8") as f:
        f.write(generate_drawio_xml())
    print(f"Saved Draw.io to {DRAWIO_PATH}")

    print("2. Generating SVG...")
    with open(SVG_PATH, "w", encoding="utf-8") as f:
        f.write(generate_svg())
    print(f"Saved SVG to {SVG_PATH}")

    print("3. Rendering PNG via Headless Chromium...")
    # Wrap SVG in minimal HTML for perfect headless rendering
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
    temp_html = "/tmp/db_schema_render.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    cmd = [
        "/etc/profiles/per-user/zerok/bin/chromium",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--window-size=1180,800",
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

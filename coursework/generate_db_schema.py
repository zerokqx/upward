#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор схемы базы данных (ER-диаграмма) в форматах:
1. Draw.io (.drawio XML)
2. SVG (векторный рендер высокого качества)
3. PNG (растровый рендер через headless Chromium)
Схема основана на реальных миграциях PostgreSQL / TimescaleDB сервиса Uptime.
"""

import os
import subprocess
import html

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DRAWIO_PATH = os.path.join(BASE_DIR, "db_schema_upward.drawio")
SVG_PATH = os.path.join(BASE_DIR, "screenshots", "db_schema_upward.svg")
PNG_PATH = os.path.join(BASE_DIR, "screenshots", "db_schema_upward.png")

def generate_drawio_xml():
    xml = '''<mxfile host="app.diagrams.net" modified="2026-09-22T12:00:00.000Z" agent="Upward DB Schema Generator" version="21.6.8" type="device">
  <diagram id="db_schema_diagram" name="Схема базы данных (ERD)">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" background="#f8fafc">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- Заголовок -->
        <mxCell id="title" value="&lt;b style=&quot;font-size: 16px;&quot;&gt;СХЕМА БАЗЫ ДАННЫХ И ХРАНИЛИЩА ТЕЛЕМЕТРИИ СИСТЕМЫ «UPWARD»&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;font-size: 12px; color: #475569;&quot;&gt;PostgreSQL 16 + Расширение TimescaleDB (Hypertables &amp; Data Retention) + Redis 7&lt;/span&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontFamily=Arial;" vertex="1" parent="1">
          <mxGeometry x="234" y="20" width="700" height="45" as="geometry"/>
        </mxCell>

        <!-- ==================== ТАБЛИЦА 1: SITES ==================== -->
        <mxCell id="tbl_sites_header" value="&lt;b&gt;sites (Реляционная таблица ресурсов)&lt;/b&gt;" style="swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#2563eb;strokeColor=#1d4ed8;fontColor=#ffffff;fontSize=13;fontFamily=Arial;" vertex="1" parent="1">
          <mxGeometry x="60" y="110" width="340" height="270" as="geometry"/>
        </mxCell>
        <mxCell id="site_f1" value="PK | id : UUID (gen_random_uuid())" style="text;strokeColor=none;fillColor=#eff6ff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;fontStyle=1;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="30" width="340" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="site_f2" value="     user_id : TEXT NOT NULL" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="56" width="340" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="site_f3" value="     url : TEXT NOT NULL (http/https)" style="text;strokeColor=none;fillColor=#f8fafc;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="82" width="340" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="site_f4" value="     created_at : TIMESTAMPTZ DEFAULT NOW()" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="108" width="340" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="site_f5" value="IX | last_check : TIMESTAMPTZ" style="text;strokeColor=none;fillColor=#f8fafc;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="134" width="340" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="site_f6" value="IX | status : VARCHAR(20) DEFAULT 'idle'" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="160" width="340" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="site_f7" value="IX | status_updated_at : TIMESTAMPTZ" style="text;strokeColor=none;fillColor=#f8fafc;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="186" width="340" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="site_f8" value="     active : BOOLEAN DEFAULT FALSE" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="212" width="340" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="site_f9" value="Индексы: sites_pkey, idx_sites_last_check, idx_status_last_check" style="text;strokeColor=none;fillColor=#eff6ff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Arial;fontSize=9;fontColor=#475569;" vertex="1" parent="tbl_sites_header">
          <mxGeometry y="238" width="340" height="32" as="geometry"/>
        </mxCell>

        <!-- ==================== ТАБЛИЦА 2: SITE_PINGS ==================== -->
        <mxCell id="tbl_pings_header" value="&lt;b&gt;site_pings (TimescaleDB Hypertable)&lt;/b&gt;" style="swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#0d9488;strokeColor=#0f766e;fontColor=#ffffff;fontSize=13;fontFamily=Arial;" vertex="1" parent="1">
          <mxGeometry x="490" y="110" width="360" height="270" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f1" value="PK | time : TIMESTAMPTZ NOT NULL (Partition Key)" style="text;strokeColor=none;fillColor=#f0fdfa;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;fontStyle=1;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="30" width="360" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f2" value="FK | site_id : UUID NOT NULL (FK -> sites.id)" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;fontStyle=1;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="56" width="360" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f3" value="     duration_ms : DOUBLE PRECISION NOT NULL" style="text;strokeColor=none;fillColor=#f8fafc;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="82" width="360" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f4" value="     extra : JSONB (status_code, error, ip, meta)" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="108" width="360" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f5" value="TimescaleDB Свойства:" style="text;strokeColor=none;fillColor=#ccfbf1;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Arial;fontSize=10;fontStyle=1;fontColor=#0f766e;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="134" width="360" height="24" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f6" value="• create_hypertable('site_pings', 'time')" style="text;strokeColor=none;fillColor=#f0fdfa;align=left;verticalAlign=middle;spacingLeft=12;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Courier New;fontSize=10;fontColor=#0f766e;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="158" width="360" height="24" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f7" value="• add_retention_policy(INTERVAL '30 days')" style="text;strokeColor=none;fillColor=#f0fdfa;align=left;verticalAlign=middle;spacingLeft=12;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Courier New;fontSize=10;fontColor=#0f766e;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="182" width="360" height="24" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f8" value="• ON DELETE CASCADE по внешнему ключу site_id" style="text;strokeColor=none;fillColor=#f0fdfa;align=left;verticalAlign=middle;spacingLeft=12;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Courier New;fontSize=10;fontColor=#0f766e;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="206" width="360" height="24" as="geometry"/>
        </mxCell>
        <mxCell id="ping_f9" value="Автоматическое секционирование чанков по времени" style="text;strokeColor=none;fillColor=#ccfbf1;align=center;verticalAlign=middle;overflow=hidden;rotatable=0;fontFamily=Arial;fontSize=9;fontColor=#115e59;" vertex="1" parent="tbl_pings_header">
          <mxGeometry y="230" width="360" height="40" as="geometry"/>
        </mxCell>

        <!-- ==================== СВЯЗЬ: SITES 1 - N SITE_PINGS ==================== -->
        <mxCell id="rel_sites_pings" value="1 : N&lt;br&gt;(ON DELETE CASCADE)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0f766e;strokeWidth=2;fontSize=10;fontFamily=Arial;labelBackgroundColor=#ffffff;" edge="1" parent="1" source="site_f1" target="ping_f2">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="445" y="153"/>
              <mxPoint x="445" y="179"/>
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- ==================== ТАБЛИЦА 3: FORBIDDEN_IP ==================== -->
        <mxCell id="tbl_fip_header" value="&lt;b&gt;forbidden_ip (Черный список SSRF)&lt;/b&gt;" style="swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#e11d48;strokeColor=#be123c;fontColor=#ffffff;fontSize=13;fontFamily=Arial;" vertex="1" parent="1">
          <mxGeometry x="60" y="440" width="340" height="170" as="geometry"/>
        </mxCell>
        <mxCell id="fip_f1" value="PK | id : BIGSERIAL" style="text;strokeColor=none;fillColor=#fff1f2;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;fontStyle=1;" vertex="1" parent="tbl_fip_header">
          <mxGeometry y="30" width="340" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="fip_f2" value="UQ | ip : TEXT NOT NULL (IP / CIDR)" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;fontStyle=1;" vertex="1" parent="tbl_fip_header">
          <mxGeometry y="56" width="340" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="fip_f3" value="     created_at : TIMESTAMPTZ DEFAULT NOW()" style="text;strokeColor=none;fillColor=#f8fafc;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_fip_header">
          <mxGeometry y="82" width="340" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="fip_f4" value="Индекс: UNIQUE idx_forbidden_ip_ip ON forbidden_ip(ip)" style="text;strokeColor=none;fillColor=#ffe4e6;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Courier New;fontSize=9;fontColor=#9f1239;" vertex="1" parent="tbl_fip_header">
          <mxGeometry y="108" width="340" height="28" as="geometry"/>
        </mxCell>
        <mxCell id="fip_f5" value="Используется модулем IpValidator для мгновенного отсечения запрещенных сетей" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Arial;fontSize=9;fontColor=#475569;" vertex="1" parent="tbl_fip_header">
          <mxGeometry y="136" width="340" height="34" as="geometry"/>
        </mxCell>

        <!-- ==================== СУЩНОСТЬ 4: REDIS ==================== -->
        <mxCell id="tbl_redis_header" value="&lt;b&gt;Redis In-Memory (Верификация HTTP-01)&lt;/b&gt;" style="swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#ea580c;strokeColor=#c2410c;fontColor=#ffffff;fontSize=13;fontFamily=Arial;" vertex="1" parent="1">
          <mxGeometry x="490" y="440" width="360" height="170" as="geometry"/>
        </mxCell>
        <mxCell id="red_f1" value="KEY | challenge:{site_id}:{token} (String)" style="text;strokeColor=none;fillColor=#fff7ed;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;fontStyle=1;" vertex="1" parent="tbl_redis_header">
          <mxGeometry y="30" width="360" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="red_f2" value="VAL | token : UUIDv4 (128-битный токен)" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_redis_header">
          <mxGeometry y="56" width="360" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="red_f3" value="TTL | 86400 секунд (Срок жизни 24 часа)" style="text;strokeColor=none;fillColor=#ffedd5;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;fontColor=#9a3412;" vertex="1" parent="tbl_redis_header">
          <mxGeometry y="82" width="360" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="red_f4" value="PATH| /.well-known/upward на сервере владельца" style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Courier New;fontSize=11;" vertex="1" parent="tbl_redis_header">
          <mxGeometry y="108" width="360" height="26" as="geometry"/>
        </mxCell>
        <mxCell id="red_f5" value="После подтверждения ключ удаляется, а в sites выставляется active = true" style="text;strokeColor=none;fillColor=#fff7ed;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Arial;fontSize=9;fontColor=#9a3412;" vertex="1" parent="tbl_redis_header">
          <mxGeometry y="134" width="360" height="36" as="geometry"/>
        </mxCell>

        <!-- ==================== СВЯЗЬ: SITES 1 - 1 REDIS ==================== -->
        <mxCell id="rel_sites_redis" value="1 : 1 (Временный токен HTTP-01)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#ea580c;strokeWidth=2;fontSize=10;fontFamily=Arial;labelBackgroundColor=#ffffff;dashed=1;" edge="1" parent="1" source="site_f8" target="red_f1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="445" y="335"/>
              <mxPoint x="445" y="483"/>
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- ==================== БЛОК ПОЯСНЕНИЙ СПРАВА ==================== -->
        <mxCell id="notes_box" value="&lt;b&gt;АРХИТЕКТУРНЫЕ ОСОБЕННОСТИ&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;b&gt;1. Атомарность захвата:&lt;/b&gt;&lt;br&gt;Выборка пачек сайтов воркерами выполняется через CTE с директивой &lt;i&gt;FOR UPDATE SKIP LOCKED&lt;/i&gt;, исключающей race condition между репликами.&lt;br&gt;&lt;br&gt;&lt;b&gt;2. Dead Worker Recovery:&lt;/b&gt;&lt;br&gt;Поле &lt;i&gt;status_updated_at&lt;/i&gt; возвращает зависшие задачи в статус 'idle' через 3 минуты.&lt;br&gt;&lt;br&gt;&lt;b&gt;3. Time-Series Hypertable:&lt;/b&gt;&lt;br&gt;Таблица &lt;i&gt;site_pings&lt;/i&gt; партиционируется TimescaleDB по времени &lt;i&gt;time&lt;/i&gt;. Устаревшие чанки старше 30 дней удаляются мгновенно без блокировок.&lt;br&gt;&lt;br&gt;&lt;b&gt;4. Многоуровневый SSRF-фильтр:&lt;/b&gt;&lt;br&gt;Запросы к loopback, RFC 1918 и адресам из &lt;i&gt;forbidden_ip&lt;/i&gt; отклоняются до открытия TCP-сокета." style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#cbd5e1;strokeWidth=1.5;align=left;verticalAlign=top;spacing=12;fontFamily=Arial;fontSize=11;lineHeight=1.4;" vertex="1" parent="1">
          <mxGeometry x="880" y="110" width="250" height="500" as="geometry"/>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    return xml

def generate_svg():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 720" width="1180" height="720" style="background:#f8fafc; font-family:'Segoe UI', Arial, sans-serif;">
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
    <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#e11d48"/>
    </marker>
  </defs>

  <!-- Title Banner -->
  <rect x="30" y="15" width="1120" height="55" rx="8" fill="#1e293b" filter="url(#shadow)"/>
  <text x="590" y="40" fill="#ffffff" font-size="17" font-weight="bold" text-anchor="middle">СХЕМА БАЗЫ ДАННЫХ И МОДЕЛЕЙ ХРАНЕНИЯ ДАННЫХ «UPWARD»</text>
  <text x="590" y="58" fill="#94a3b8" font-size="12" text-anchor="middle">PostgreSQL 16 + Расширение TimescaleDB (Hypertables / Data Retention) + Redis 7</text>

  <!-- ==================== ТАБЛИЦА SITES ==================== -->
  <g transform="translate(40, 90)" filter="url(#shadow)">
    <!-- Header -->
    <rect x="0" y="0" width="370" height="34" rx="6" fill="#2563eb"/>
    <rect x="0" y="28" width="370" height="6" fill="#2563eb"/>
    <text x="185" y="22" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">sites (Реляционная таблица ресурсов)</text>
    
    <!-- Body -->
    <rect x="0" y="34" width="370" height="286" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    
    <!-- Row 1: id -->
    <rect x="0" y="34" width="370" height="28" fill="#eff6ff"/>
    <text x="12" y="52" fill="#1d4ed8" font-size="11" font-weight="bold" font-family="'Courier New', monospace">PK | id : UUID DEFAULT gen_random_uuid()</text>
    
    <!-- Row 2: user_id -->
    <rect x="0" y="62" width="370" height="28" fill="#ffffff"/>
    <text x="12" y="80" fill="#0f172a" font-size="11" font-family="'Courier New', monospace">     user_id : TEXT NOT NULL</text>
    
    <!-- Row 3: url -->
    <rect x="0" y="90" width="370" height="28" fill="#f8fafc"/>
    <text x="12" y="108" fill="#0f172a" font-size="11" font-family="'Courier New', monospace">     url : TEXT NOT NULL (http / https)</text>
    
    <!-- Row 4: created_at -->
    <rect x="0" y="118" width="370" height="28" fill="#ffffff"/>
    <text x="12" y="136" fill="#0f172a" font-size="11" font-family="'Courier New', monospace">     created_at : TIMESTAMPTZ DEFAULT NOW()</text>
    
    <!-- Row 5: last_check -->
    <rect x="0" y="146" width="370" height="28" fill="#f8fafc"/>
    <text x="12" y="164" fill="#0369a1" font-size="11" font-weight="bold" font-family="'Courier New', monospace">IX | last_check : TIMESTAMPTZ</text>
    
    <!-- Row 6: status -->
    <rect x="0" y="174" width="370" height="28" fill="#ffffff"/>
    <text x="12" y="192" fill="#0369a1" font-size="11" font-weight="bold" font-family="'Courier New', monospace">IX | status : VARCHAR(20) DEFAULT 'idle'</text>
    
    <!-- Row 7: status_updated_at -->
    <rect x="0" y="202" width="370" height="28" fill="#f8fafc"/>
    <text x="12" y="220" fill="#0369a1" font-size="11" font-weight="bold" font-family="'Courier New', monospace">IX | status_updated_at : TIMESTAMPTZ</text>
    
    <!-- Row 8: active -->
    <rect x="0" y="230" width="370" height="28" fill="#ffffff"/>
    <text x="12" y="248" fill="#0f172a" font-size="11" font-family="'Courier New', monospace">     active : BOOLEAN DEFAULT FALSE</text>
    
    <!-- Indexes info footer -->
    <rect x="0" y="258" width="370" height="62" rx="0" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
    <text x="12" y="275" fill="#475569" font-size="9.5" font-weight="bold">ИНДЕКСЫ ТАБЛИЦЫ:</text>
    <text x="12" y="291" fill="#64748b" font-size="9" font-family="'Courier New', monospace">• idx_sites_last_check (last_check ASC NULLS FIRST)</text>
    <text x="12" y="306" fill="#64748b" font-size="9" font-family="'Courier New', monospace">• idx_sites_status_last_check (status, last_check)</text>
  </g>

  <!-- ==================== ТАБЛИЦА SITE_PINGS (HYPERTABLE) ==================== -->
  <g transform="translate(480, 90)" filter="url(#shadow)">
    <!-- Header -->
    <rect x="0" y="0" width="380" height="34" rx="6" fill="#0d9488"/>
    <rect x="0" y="28" width="380" height="6" fill="#0d9488"/>
    <text x="190" y="22" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">site_pings (TimescaleDB Hypertable)</text>
    
    <!-- Body -->
    <rect x="0" y="34" width="380" height="286" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    
    <!-- Row 1: time (PK, Partition) -->
    <rect x="0" y="34" width="380" height="28" fill="#f0fdfa"/>
    <text x="12" y="52" fill="#0f766e" font-size="11" font-weight="bold" font-family="'Courier New', monospace">PK | time : TIMESTAMPTZ (Partition Key)</text>
    
    <!-- Row 2: site_id (FK) -->
    <rect x="0" y="62" width="380" height="28" fill="#ffffff"/>
    <text x="12" y="80" fill="#0f766e" font-size="11" font-weight="bold" font-family="'Courier New', monospace">FK | site_id : UUID (FK -&gt; sites.id)</text>
    
    <!-- Row 3: duration_ms -->
    <rect x="0" y="90" width="380" height="28" fill="#f8fafc"/>
    <text x="12" y="108" fill="#0f172a" font-size="11" font-family="'Courier New', monospace">     duration_ms : DOUBLE PRECISION NOT NULL</text>
    
    <!-- Row 4: extra -->
    <rect x="0" y="118" width="380" height="28" fill="#ffffff"/>
    <text x="12" y="136" fill="#0f172a" font-size="11" font-family="'Courier New', monospace">     extra : JSONB (http_code, error, ip)</text>
    
    <!-- TimescaleDB Features Box -->
    <rect x="0" y="146" width="380" height="174" fill="#f0fdfa" stroke="#99f6e4" stroke-width="1"/>
    <text x="12" y="168" fill="#0f766e" font-size="10.5" font-weight="bold">СВОЙСТВА И ПОЛИТИКИ TIMESCALEDB:</text>
    
    <rect x="10" y="178" width="360" height="28" rx="4" fill="#ffffff" stroke="#ccfbf1"/>
    <text x="18" y="196" fill="#115e59" font-size="9.5" font-family="'Courier New', monospace">SELECT create_hypertable('site_pings', 'time');</text>
    
    <rect x="10" y="212" width="360" height="28" rx="4" fill="#ffffff" stroke="#ccfbf1"/>
    <text x="18" y="230" fill="#115e59" font-size="9.5" font-family="'Courier New', monospace">SELECT add_retention_policy(..., '30 days');</text>
    
    <text x="12" y="260" fill="#475569" font-size="9.5">• Секционирование: автоматические чанки по времени</text>
    <text x="12" y="278" fill="#475569" font-size="9.5">• Каскадное удаление: ON DELETE CASCADE при удалении сайта</text>
    <text x="12" y="296" fill="#475569" font-size="9.5">• Пакетная запись: Batch Insert сотен строк в 1 запрос</text>
  </g>

  <!-- ==================== СВЯЗЬ SITES -> SITE_PINGS ==================== -->
  <path d="M 410 162 L 445 162 L 445 162 L 480 162" fill="none" stroke="#0f766e" stroke-width="2.5" marker-end="url(#arrow-teal)"/>
  <rect x="420" y="140" width="50" height="20" rx="3" fill="#ffffff" stroke="#0f766e"/>
  <text x="445" y="154" fill="#0f766e" font-size="9" font-weight="bold" text-anchor="middle">1 : N</text>

  <!-- ==================== ТАБЛИЦА FORBIDDEN_IP ==================== -->
  <g transform="translate(40, 440)" filter="url(#shadow)">
    <!-- Header -->
    <rect x="0" y="0" width="370" height="34" rx="6" fill="#e11d48"/>
    <rect x="0" y="28" width="370" height="6" fill="#e11d48"/>
    <text x="185" y="22" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">forbidden_ip (Черный список адресов SSRF)</text>
    
    <!-- Body -->
    <rect x="0" y="34" width="370" height="216" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    
    <!-- Row 1: id -->
    <rect x="0" y="34" width="370" height="28" fill="#fff1f2"/>
    <text x="12" y="52" fill="#be123c" font-size="11" font-weight="bold" font-family="'Courier New', monospace">PK | id : BIGSERIAL PRIMARY KEY</text>
    
    <!-- Row 2: ip -->
    <rect x="0" y="62" width="370" height="28" fill="#ffffff"/>
    <text x="12" y="80" fill="#be123c" font-size="11" font-weight="bold" font-family="'Courier New', monospace">UQ | ip : TEXT NOT NULL (IPv4 / IPv6 / CIDR)</text>
    
    <!-- Row 3: created_at -->
    <rect x="0" y="90" width="370" height="28" fill="#f8fafc"/>
    <text x="12" y="108" fill="#0f172a" font-size="11" font-family="'Courier New', monospace">     created_at : TIMESTAMPTZ DEFAULT NOW()</text>
    
    <!-- Details -->
    <rect x="0" y="118" width="370" height="132" fill="#fff1f2" stroke="#fecdd3" stroke-width="1"/>
    <text x="12" y="138" fill="#9f1239" font-size="10" font-weight="bold">НАЗНАЧЕНИЕ И ЗАЩИТНЫЕ ФУНКЦИИ:</text>
    <text x="12" y="158" fill="#475569" font-size="9.5">• Индекс: CREATE UNIQUE INDEX idx_forbidden_ip_ip</text>
    <text x="12" y="176" fill="#475569" font-size="9.5">• Сверка в IpValidator: DNS-резолвинг хоста перед опросом</text>
    <text x="12" y="194" fill="#475569" font-size="9.5">• Блокировка: Loopback (127.0.0.1), RFC 1918 (10.0/8, 172.16/12,</text>
    <text x="12" y="210" fill="#475569" font-size="9.5">  192.168/16), Link-Local (169.254/16) и опасных доменов</text>
    <text x="12" y="232" fill="#be123c" font-size="9.5" font-weight="bold">Предотвращает сканирование внутренней сети и облака</text>
  </g>

  <!-- ==================== СУЩНОСТЬ REDIS CACHE ==================== -->
  <g transform="translate(480, 440)" filter="url(#shadow)">
    <!-- Header -->
    <rect x="0" y="0" width="380" height="34" rx="6" fill="#ea580c"/>
    <rect x="0" y="28" width="380" height="6" fill="#ea580c"/>
    <text x="190" y="22" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">Redis In-Memory (Токены HTTP-01 Challenge)</text>
    
    <!-- Body -->
    <rect x="0" y="34" width="380" height="216" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    
    <!-- Row 1: Key structure -->
    <rect x="0" y="34" width="380" height="28" fill="#fff7ed"/>
    <text x="12" y="52" fill="#c2410c" font-size="11" font-weight="bold" font-family="'Courier New', monospace">KEY | challenge:{site_id}:{token}</text>
    
    <!-- Row 2: Value -->
    <rect x="0" y="62" width="380" height="28" fill="#ffffff"/>
    <text x="12" y="80" fill="#0f172a" font-size="11" font-family="'Courier New', monospace">VAL | token : UUIDv4 (128-битный токен)</text>
    
    <!-- Row 3: TTL -->
    <rect x="0" y="90" width="380" height="28" fill="#fff7ed"/>
    <text x="12" y="108" fill="#c2410c" font-size="11" font-weight="bold" font-family="'Courier New', monospace">TTL | 86400 секунд (Срок жизни ровно 24 часа)</text>
    
    <!-- Details -->
    <rect x="0" y="118" width="380" height="132" fill="#fff7ed" stroke="#fed7aa" stroke-width="1"/>
    <text x="12" y="138" fill="#9a3412" font-size="10" font-weight="bold">ПРОТОКОЛ ВЕРИФИКАЦИИ ВЛАДЕНИЯ САЙТОМ:</text>
    <text x="12" y="158" fill="#475569" font-size="9.5">• Путь: /.well-known/upward на сервере владельца</text>
    <text x="12" y="176" fill="#475569" font-size="9.5">• При регистрации сайт создается со статусом active = false</text>
    <text x="12" y="194" fill="#475569" font-size="9.5">• Эндпоинт POST /sites/{id}/verify опрашивает контрольный URL</text>
    <text x="12" y="212" fill="#475569" font-size="9.5">• При совпадении токена: ключ в Redis удаляется,</text>
    <text x="12" y="230" fill="#c2410c" font-size="9.5" font-weight="bold">в PostgreSQL выставляется active = true, включается мониторинг</text>
  </g>

  <!-- ==================== СВЯЗЬ SITES -> REDIS ==================== -->
  <path d="M 225 380 L 225 410 L 670 410 L 670 440" fill="none" stroke="#ea580c" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#arrow-orange)"/>
  <rect x="400" y="400" width="100" height="20" rx="3" fill="#ffffff" stroke="#ea580c"/>
  <text x="450" y="414" fill="#ea580c" font-size="9" font-weight="bold" text-anchor="middle">1 : 1 Challenge</text>

  <!-- ==================== ПАНЕЛЬ АРХИТЕКТУРНЫХ ОСОБЕННОСТЕЙ СПРАВА ==================== -->
  <g transform="translate(890, 90)" filter="url(#shadow)">
    <rect x="0" y="0" width="260" height="566" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="0" y="0" width="260" height="34" rx="8" fill="#334155"/>
    <rect x="0" y="26" width="260" height="8" fill="#334155"/>
    <text x="130" y="22" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">ИНЖЕНЕРНЫЕ РЕШЕНИЯ БД</text>
    
    <g transform="translate(15, 48)">
      <!-- Item 1 -->
      <circle cx="8" cy="8" r="8" fill="#2563eb"/>
      <text x="8" y="12" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">1</text>
      <text x="24" y="12" fill="#0f172a" font-size="11" font-weight="bold">Атомарная блокировка CTE</text>
      <text x="24" y="30" fill="#475569" font-size="9.5">Запрос с FOR UPDATE SKIP</text>
      <text x="24" y="44" fill="#475569" font-size="9.5">LOCKED атомарно захватывает</text>
      <text x="24" y="58" fill="#475569" font-size="9.5">батч сайтов без гонок между</text>
      <text x="24" y="72" fill="#475569" font-size="9.5">репликами воркеров.</text>

      <!-- Item 2 -->
      <circle cx="8" cy="100" r="8" fill="#0d9488"/>
      <text x="8" y="104" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">2</text>
      <text x="24" y="104" fill="#0f172a" font-size="11" font-weight="bold">Dead Worker Recovery</text>
      <text x="24" y="122" fill="#475569" font-size="9.5">Если воркер аварийно упал,</text>
      <text x="24" y="136" fill="#475569" font-size="9.5">условие status_updated_at &lt;</text>
      <text x="24" y="150" fill="#475569" font-size="9.5">NOW() - 3 min возвращает</text>
      <text x="24" y="164" fill="#475569" font-size="9.5">задачи в очередь 'idle'.</text>

      <!-- Item 3 -->
      <circle cx="8" cy="192" r="8" fill="#0f766e"/>
      <text x="8" y="196" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">3</text>
      <text x="24" y="196" fill="#0f172a" font-size="11" font-weight="bold">TimescaleDB Hypertables</text>
      <text x="24" y="214" fill="#475569" font-size="9.5">Метрики задержек (RTT)</text>
      <text x="24" y="228" fill="#475569" font-size="9.5">сохраняются в гипертаблицу.</text>
      <text x="24" y="242" fill="#475569" font-size="9.5">Авто-удаление через 30 дней</text>
      <text x="24" y="256" fill="#475569" font-size="9.5">исключает фрагментацию диска.</text>

      <!-- Item 4 -->
      <circle cx="8" cy="284" r="8" fill="#e11d48"/>
      <text x="8" y="288" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">4</text>
      <text x="24" y="288" fill="#0f172a" font-size="11" font-weight="bold">Пакетная вставка (Batch)</text>
      <text x="24" y="306" fill="#475569" font-size="9.5">Метод save_pings_batch</text>
      <text x="24" y="320" fill="#475569" font-size="9.5">вставляет до 500 замеров в 1</text>
      <text x="24" y="334" fill="#475569" font-size="9.5">транзакционный SQL-запрос</text>
      <text x="24" y="348" fill="#475569" font-size="9.5">длительностью 5–8 мс.</text>

      <!-- Item 5 -->
      <circle cx="8" cy="376" r="8" fill="#ea580c"/>
      <text x="8" y="380" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">5</text>
      <text x="24" y="380" fill="#0f172a" font-size="11" font-weight="bold">Безопасность (SSRF)</text>
      <text x="24" y="398" fill="#475569" font-size="9.5">Трехуровневая фильтрация</text>
      <text x="24" y="412" fill="#475569" font-size="9.5">IP исключает атаки на петли</text>
      <text x="24" y="426" fill="#475569" font-size="9.5">и служебные порты облака.</text>
      
      <!-- Summary Box -->
      <rect x="0" y="450" width="230" height="56" rx="6" fill="#f8fafc" stroke="#e2e8f0"/>
      <text x="115" y="472" fill="#0f172a" font-size="10" font-weight="bold" text-anchor="middle">ПРОИЗВОДИТЕЛЬНОСТЬ</text>
      <text x="115" y="492" fill="#16a34a" font-size="11" font-weight="bold" text-anchor="middle">&gt; 10 000 проверок / мин</text>
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
        "--window-size=1180,720",
        "--default-background-color=00000000",
        f"--screenshot={PNG_PATH}",
        temp_html
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(PNG_PATH):
        print(f"PNG rendered successfully -> {PNG_PATH} ({os.path.getsize(PNG_PATH)} bytes)")
    else:
        print(f"Error rendering PNG: {res.stderr}")

if __name__ == "__main__":
    main()

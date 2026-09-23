#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор функциональной диаграммы IDEF0 в формате Draw.io (.drawio)
для курсового проекта «Разработка веб-приложения распределенного мониторинга внутренней инфраструктуры «Upward»»
"""

import html

def esc(text):
    return html.escape(str(text))

def build_drawio_xml():
    xml = '''<mxfile host="app.diagrams.net" modified="2026-09-22T11:00:00.000Z" agent="Upward IDEF0 Generator" version="21.6.8" type="device">
  <!-- ================================================================= -->
  <!-- СТРАНИЦА 1: КОНТЕКСТНАЯ ДИАГРАММА А-0                             -->
  <!-- ================================================================= -->
  <diagram id="diagram_a_minus_0" name="А-0 Контекстная диаграмма">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" background="#ffffff">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- Заголовок диаграммы -->
        <mxCell id="title_a0" value="&lt;b&gt;КОНТЕКСТНАЯ ДИАГРАММА IDEF0: А-0&lt;/b&gt;&lt;br&gt;Мониторинг доступности внутренней инфраструктуры веб-приложений «Upward»" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=15;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="334" y="30" width="500" height="40" as="geometry"/>
        </mxCell>

        <!-- Центральный функциональный блок А0 -->
        <mxCell id="box_a0" value="&lt;b style=&quot;font-size: 14px;&quot;&gt;Осуществлять распределенный мониторинг доступности внутренней инфраструктуры веб-приложений «Upward»&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;div style=&quot;text-align: right; font-size: 12px; font-weight: bold; color: #1e293b;&quot;&gt;А0&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#1e293b;strokeWidth=2;align=center;verticalAlign=middle;fontFamily=Times New Roman;fontSize=13;spacing=15;" vertex="1" parent="1">
          <mxGeometry x="384" y="270" width="400" height="180" as="geometry"/>
        </mxCell>

        <!-- ================= УПРАВЛЕНИЕ (СВЕРХУ) ================= -->
        <!-- Стрелка У1: SLA и регламенты -->
        <mxCell id="arrow_c1" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="450" y="100" as="sourcePoint"/>
            <mxPoint x="450" y="270" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_c1" value="Соглашения SLA/SLO;&lt;br&gt;Регламенты доступности 99.9%" style="text;html=1;align=center;verticalAlign=bottom;whiteSpace=wrap;rounded=0;fontSize=11;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="350" y="110" width="190" height="30" as="geometry"/>
        </mxCell>

        <!-- Стрелка У2: Политики безопасности и SSRF -->
        <mxCell id="arrow_c2" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="584" y="100" as="sourcePoint"/>
            <mxPoint x="584" y="270" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_c2" value="Политики ИБ (фильтрация RFC 1918,&lt;br&gt;правила SSRF, черный список forbidden_ip)" style="text;html=1;align=center;verticalAlign=bottom;whiteSpace=wrap;rounded=0;fontSize=11;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="480" y="150" width="210" height="30" as="geometry"/>
        </mxCell>

        <!-- Стрелка У3: Параметры воркера и Retention -->
        <mxCell id="arrow_c3" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="720" y="100" as="sourcePoint"/>
            <mxPoint x="720" y="270" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_c3" value="Конфигурация воркера (таймаут 10 с,&lt;br&gt;concurrency=25, retention 30 дней)" style="text;html=1;align=center;verticalAlign=bottom;whiteSpace=wrap;rounded=0;fontSize=11;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="640" y="110" width="200" height="30" as="geometry"/>
        </mxCell>

        <!-- ================= ВХОДЫ (СЛЕВА) ================= -->
        <!-- Стрелка В1: URL сайтов и user_id -->
        <mxCell id="arrow_i1" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="120" y="320" as="sourcePoint"/>
            <mxPoint x="384" y="320" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_i1" value="Целевые URL сайтов (http/https);&lt;br&gt;Идентификаторы пользователей user_id" style="text;html=1;align=left;verticalAlign=bottom;whiteSpace=wrap;rounded=0;fontSize=11;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="140" y="285" width="220" height="30" as="geometry"/>
        </mxCell>

        <!-- Стрелка В2: Ответы веб-узлов -->
        <mxCell id="arrow_i2" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="120" y="380" as="sourcePoint"/>
            <mxPoint x="384" y="380" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_i2" value="Сетевые HTTP/TCP ответы веб-узлов&lt;br&gt;(задержка RTT, статус-коды, ошибки)" style="text;html=1;align=left;verticalAlign=bottom;whiteSpace=wrap;rounded=0;fontSize=11;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="140" y="345" width="220" height="30" as="geometry"/>
        </mxCell>

        <!-- Стрелка В3: Challenge токены -->
        <mxCell id="arrow_i3" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="120" y="420" as="sourcePoint"/>
            <mxPoint x="384" y="420" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_i3" value="Токены подтверждения владения (HTTP-01)" style="text;html=1;align=left;verticalAlign=bottom;whiteSpace=wrap;rounded=0;fontSize=11;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="140" y="395" width="230" height="20" as="geometry"/>
        </mxCell>

        <!-- ================= ВЫХОДЫ (СПРАВА) ================= -->
        <!-- Стрелка О1: Временные ряды и метрики -->
        <mxCell id="arrow_o1" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="784" y="320" as="sourcePoint"/>
            <mxPoint x="1050" y="320" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_o1" value="Временные ряды телеметрии (duration_ms,&lt;br&gt;time, статус-коды) в TimescaleDB" style="text;html=1;align=left;verticalAlign=bottom;whiteSpace=wrap;rounded=0;fontSize=11;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="810" y="285" width="230" height="30" as="geometry"/>
        </mxCell>

        <!-- Стрелка О2: Статусы сайтов -->
        <mxCell id="arrow_o2" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="784" y="370" as="sourcePoint"/>
            <mxPoint x="1050" y="370" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_o2" value="Статусы доступности сайтов (idle, active);&lt;br&gt;Уведомления о подтверждении владения" style="text;html=1;align=left;verticalAlign=bottom;whiteSpace=wrap;rounded=0;fontSize=11;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="810" y="335" width="230" height="30" as="geometry"/>
        </mxCell>

        <!-- Стрелка О3: OpenAPI и Health -->
        <mxCell id="arrow_o3" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="784" y="420" as="sourcePoint"/>
            <mxPoint x="1050" y="420" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_o3" value="Интерфейс Swagger UI и Health-отчеты" style="text;html=1;align=left;verticalAlign=bottom;whiteSpace=wrap;rounded=0;fontSize=11;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="810" y="395" width="220" height="20" as="geometry"/>
        </mxCell>

        <!-- ================= МЕХАНИЗМЫ (СНИЗУ) ================= -->
        <!-- Стрелка М1: Uptime Rust -->
        <mxCell id="arrow_m1" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="440" y="620" as="sourcePoint"/>
            <mxPoint x="440" y="450" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_m1" value="Сервис Uptime (Rust/Axum/Tokio;&lt;br&gt;асинхронный воркер buffer_unordered)" style="text;html=1;align=center;verticalAlign=top;whiteSpace=wrap;rounded=0;fontSize=11;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="340" y="560" width="190" height="30" as="geometry"/>
        </mxCell>

        <!-- Стрелка М2: TimescaleDB & Redis -->
        <mxCell id="arrow_m2" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="584" y="620" as="sourcePoint"/>
            <mxPoint x="584" y="450" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_m2" value="СУБД PostgreSQL/TimescaleDB;&lt;br&gt;In-Memory хранилище Redis" style="text;html=1;align=center;verticalAlign=top;whiteSpace=wrap;rounded=0;fontSize=11;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="490" y="560" width="180" height="30" as="geometry"/>
        </mxCell>

        <!-- Стрелка М3: Nginx, BFF, SRE -->
        <mxCell id="arrow_m3" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="720" y="620" as="sourcePoint"/>
            <mxPoint x="720" y="450" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_m3" value="L7 Nginx балансировщик; BFF (NestJS);&lt;br&gt;SRE-инженеры и администраторы" style="text;html=1;align=center;verticalAlign=top;whiteSpace=wrap;rounded=0;fontSize=11;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="640" y="560" width="200" height="30" as="geometry"/>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>

  <!-- ================================================================= -->
  <!-- СТРАНИЦА 2: ДЕКОМПОЗИЦИЯ ДИАГРАММЫ А0 (4 ФУНКЦИОНАЛЬНЫХ БЛОКА)    -->
  <!-- ================================================================= -->
  <diagram id="diagram_a0_decomp" name="А0 Декомпозиция процессов">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" background="#ffffff">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- Заголовок страницы -->
        <mxCell id="title_a0_decomp" value="&lt;b&gt;ДИАГРАММА ДЕКОМПОЗИЦИИ IDEF0: А0&lt;/b&gt;&lt;br&gt;Декомпозиция процессов системы мониторинга «Upward»" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=15;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="334" y="20" width="500" height="40" as="geometry"/>
        </mxCell>

        <!-- ================= БЛОК А1 ================= -->
        <mxCell id="box_a1" value="&lt;b&gt;Регистрировать целевые ресурсы и валидировать права владения&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;div style=&quot;text-align: right; font-size: 11px; font-weight: bold;&quot;&gt;А1&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#1e293b;strokeWidth=1.5;align=center;verticalAlign=middle;fontFamily=Times New Roman;fontSize=12;spacing=8;" vertex="1" parent="1">
          <mxGeometry x="120" y="160" width="200" height="100" as="geometry"/>
        </mxCell>

        <!-- ================= БЛОК А2 ================= -->
        <mxCell id="box_a2" value="&lt;b&gt;Атомарно захватывать и распределять батчи целевых сайтов&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;div style=&quot;text-align: right; font-size: 11px; font-weight: bold;&quot;&gt;А2&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#1e293b;strokeWidth=1.5;align=center;verticalAlign=middle;fontFamily=Times New Roman;fontSize=12;spacing=8;" vertex="1" parent="1">
          <mxGeometry x="380" y="290" width="200" height="100" as="geometry"/>
        </mxCell>

        <!-- ================= БЛОК А3 ================= -->
        <mxCell id="box_a3" value="&lt;b&gt;Выполнять параллельный неблокирующий опрос веб-узлов&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;div style=&quot;text-align: right; font-size: 11px; font-weight: bold;&quot;&gt;А3&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#1e293b;strokeWidth=1.5;align=center;verticalAlign=middle;fontFamily=Times New Roman;fontSize=12;spacing=8;" vertex="1" parent="1">
          <mxGeometry x="640" y="420" width="200" height="100" as="geometry"/>
        </mxCell>

        <!-- ================= БЛОК А4 ================= -->
        <mxCell id="box_a4" value="&lt;b&gt;Пакетно сохранять телеметрию и предоставлять аналитику&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;div style=&quot;text-align: right; font-size: 11px; font-weight: bold;&quot;&gt;А4&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#1e293b;strokeWidth=1.5;align=center;verticalAlign=middle;fontFamily=Times New Roman;fontSize=12;spacing=8;" vertex="1" parent="1">
          <mxGeometry x="900" y="550" width="200" height="100" as="geometry"/>
        </mxCell>

        <!-- ================= ПОТОКИ И СВЯЗИ (МЕЖДУ БЛОКАМИ) ================= -->
        <!-- Вход в А1: URL и user_id -->
        <mxCell id="e_in_a1" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="30" y="200" as="sourcePoint"/>
            <mxPoint x="120" y="200" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_e_in_a1" value="URL и user_id" style="text;html=1;fontSize=10;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="35" y="180" width="80" height="20" as="geometry"/>
        </mxCell>

        <!-- Управление А1: Политики SSRF -->
        <mxCell id="e_ctrl_a1" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="220" y="80" as="sourcePoint"/>
            <mxPoint x="220" y="160" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_ctrl_a1" value="Правила SSRF;&lt;br&gt;Черный список IP" style="text;html=1;fontSize=10;fontFamily=Times New Roman;align=center;" vertex="1" parent="1">
          <mxGeometry x="150" y="90" width="130" height="25" as="geometry"/>
        </mxCell>

        <!-- Связь А1 -> А2: Подтвержденные сайты (active=true) -->
        <mxCell id="e_a1_a2" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="320" y="210" as="sourcePoint"/>
            <mxPoint x="380" y="330" as="targetPoint"/>
            <Array as="points">
              <mxPoint x="350" y="210"/>
              <mxPoint x="350" y="330"/>
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_a1_a2" value="Активные сайты&lt;br&gt;(active=true, idle)" style="text;html=1;fontSize=10;fontFamily=Times New Roman;align=center;" vertex="1" parent="1">
          <mxGeometry x="275" y="250" width="100" height="25" as="geometry"/>
        </mxCell>

        <!-- Управление А2: FOR UPDATE SKIP LOCKED -->
        <mxCell id="e_ctrl_a2" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="480" y="80" as="sourcePoint"/>
            <mxPoint x="480" y="290" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_ctrl_a2" value="Блокировки SKIP LOCKED;&lt;br&gt;Параметр batch_size=500" style="text;html=1;fontSize=10;fontFamily=Times New Roman;align=center;" vertex="1" parent="1">
          <mxGeometry x="410" y="100" width="140" height="25" as="geometry"/>
        </mxCell>

        <!-- Связь А2 -> А3: Захваченный батч сайтов (status=processing) -->
        <mxCell id="e_a2_a3" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="580" y="340" as="sourcePoint"/>
            <mxPoint x="640" y="460" as="targetPoint"/>
            <Array as="points">
              <mxPoint x="610" y="340"/>
              <mxPoint x="610" y="460"/>
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_a2_a3" value="Батч сайтов&lt;br&gt;(processing)" style="text;html=1;fontSize=10;fontFamily=Times New Roman;align=center;" vertex="1" parent="1">
          <mxGeometry x="545" y="380" width="90" height="25" as="geometry"/>
        </mxCell>

        <!-- Управление А3: Concurrency limit и таймауты -->
        <mxCell id="e_ctrl_a3" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="740" y="80" as="sourcePoint"/>
            <mxPoint x="740" y="420" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_ctrl_a3" value="Лимит buffer_unordered(25);&lt;br&gt;Таймаут 10 с, 5 редиректов" style="text;html=1;fontSize=10;fontFamily=Times New Roman;align=center;" vertex="1" parent="1">
          <mxGeometry x="670" y="120" width="150" height="25" as="geometry"/>
        </mxCell>

        <!-- Вход в А3: Ответы от внешних веб-серверов -->
        <mxCell id="e_in_a3_net" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="30" y="480" as="sourcePoint"/>
            <mxPoint x="640" y="480" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_in_a3_net" value="Сетевые ответы опрашиваемых узлов (HTTP 200/500, RTT)" style="text;html=1;fontSize=10;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="50" y="460" width="310" height="20" as="geometry"/>
        </mxCell>

        <!-- Связь А3 -> А4: Массив результатов замеров (PingRecord) -->
        <mxCell id="e_a3_a4" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="840" y="470" as="sourcePoint"/>
            <mxPoint x="900" y="590" as="targetPoint"/>
            <Array as="points">
              <mxPoint x="870" y="470"/>
              <mxPoint x="870" y="590"/>
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_a3_a4" value="Результаты замеров&lt;br&gt;Vec&amp;lt;PingRecord&amp;gt;" style="text;html=1;fontSize=10;fontFamily=Times New Roman;align=center;" vertex="1" parent="1">
          <mxGeometry x="800" y="510" width="110" height="25" as="geometry"/>
        </mxCell>

        <!-- Управление А4: Retention Policy -->
        <mxCell id="e_ctrl_a4" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1000" y="80" as="sourcePoint"/>
            <mxPoint x="1000" y="550" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_ctrl_a4" value="Retention policy (30 дней);&lt;br&gt;Авторизация JWT" style="text;html=1;fontSize=10;fontFamily=Times New Roman;align=center;" vertex="1" parent="1">
          <mxGeometry x="930" y="140" width="140" height="25" as="geometry"/>
        </mxCell>

        <!-- Выход из А4: Обратная связь (сброс статуса сайтов в idle) -->
        <mxCell id="e_feedback_idle" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="980" y="650" as="sourcePoint"/>
            <mxPoint x="450" y="390" as="targetPoint"/>
            <Array as="points">
              <mxPoint x="980" y="690"/>
              <mxPoint x="450" y="690"/>
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_feedback" value="Фиксация last_check и сброс status='idle' для следующего раунда" style="text;html=1;fontSize=10;fontFamily=Times New Roman;align=center;" vertex="1" parent="1">
          <mxGeometry x="510" y="670" width="370" height="20" as="geometry"/>
        </mxCell>

        <!-- Основной выход из А4: Сохраненные временные ряды и API ответы -->
        <mxCell id="e_out_final" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1100" y="600" as="sourcePoint"/>
            <mxPoint x="1160" y="600" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_out_final" value="Временные ряды site_pings;&lt;br&gt;Ответы REST API / Swagger" style="text;html=1;fontSize=10;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="1105" y="560" width="160" height="35" as="geometry"/>
        </mxCell>

        <!-- ================= МЕХАНИЗМЫ (СНИЗУ БЛОКОВ) ================= -->
        <!-- Механизм А1: IpValidator & Redis -->
        <mxCell id="m_a1" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="200" y="740" as="sourcePoint"/>
            <mxPoint x="200" y="260" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_m_a1" value="IpValidator; Redis;&lt;br&gt;ChallengeRepo" style="text;html=1;fontSize=9;fontFamily=Times New Roman;align=center;" vertex="1" parent="1">
          <mxGeometry x="145" y="710" width="110" height="25" as="geometry"/>
        </mxCell>

        <!-- Механизм А2: SiteRepo & Postgres CTE -->
        <mxCell id="m_a2" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="500" y="740" as="sourcePoint"/>
            <mxPoint x="500" y="390" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_m_a2" value="SiteRepository;&lt;br&gt;TimescaleDB CTE" style="text;html=1;fontSize=9;fontFamily=Times New Roman;align=center;" vertex="1" parent="1">
          <mxGeometry x="450" y="710" width="100" height="25" as="geometry"/>
        </mxCell>

        <!-- Механизм А3: HttpPinger, Tokio, epoll -->
        <mxCell id="m_a3" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="710" y="740" as="sourcePoint"/>
            <mxPoint x="710" y="520" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_m_a3" value="HttpPinger; Tokio Stream;&lt;br&gt;epoll_wait Linux" style="text;html=1;fontSize=9;fontFamily=Times New Roman;align=center;" vertex="1" parent="1">
          <mxGeometry x="640" y="710" width="140" height="25" as="geometry"/>
        </mxCell>

        <!-- Механизм А4: PingRepo QueryBuilder & Nginx -->
        <mxCell id="m_a4" value="" style="endArrow=classic;html=1;rounded=0;strokeColor=#0f172a;strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1020" y="740" as="sourcePoint"/>
            <mxPoint x="1020" y="650" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="lbl_m_a4" value="PingRepository Batch;&lt;br&gt;Nginx Reverse Proxy; Axum" style="text;html=1;fontSize=9;fontFamily=Times New Roman;align=center;" vertex="1" parent="1">
          <mxGeometry x="940" y="710" width="160" height="25" as="geometry"/>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    return xml

def main():
    output_path = "/home/zerok/projects/upward/idef0_monitoring_upward.drawio"
    xml_content = build_drawio_xml()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print(f"Draw.io IDEF0 diagram successfully saved -> {output_path} ({len(xml_content)} bytes)")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор полной IDEF0 модели в формате Draw.io (.drawio) по методичке Рамус
для курсового проекта: «Разработка веб-приложения распределенного мониторинга
внутренней инфраструктуры «Upward»»

Включает 7 страниц:
1. AS-IS: А-0 Контекстная диаграмма (Ручной мониторинг дежурным персоналом)
2. AS-IS: А0 Декомпозиция 2 уровня (4 процесса: >3 по методичке)
3. AS-IS: А2 Декомпозиция 3 уровня блока А2 (4 процесса)
4. TO-BE: А-0 Контекстная диаграмма (Автоматизация ИС Upward)
5. TO-BE: А0 Декомпозиция 2 уровня (4 процесса, новые элементы выделены пурпурным/фиолетовым)
6. TO-BE: А1 Декомпозиция 3 уровня блока А1 (Регистрация, SSRF, Challenge)
7. TO-BE: А2 Декомпозиция 3 уровня блока А2 (Батчинг SKIP LOCKED, параллельный опрос Tokio)
"""

import html

def esc(s):
    return html.escape(str(s))

def ramus_header(cell_prefix, author="Шахсинов М. В.", project="ИС мониторинга Upward",
                 date="22.09.2026", context="ВЕРХ", is_draft=False):
    """Генерирует стандартную рамку заголовка Ramus IDEF0"""
    stat_check = "■" if not is_draft else "□"
    draft_check = "■" if is_draft else "□"
    
    cells = []
    # Внешняя граница листа
    cells.append(f'''<mxCell id="{cell_prefix}_border" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFEEB;strokeColor=#000000;strokeWidth=2;" vertex="1" parent="1">
      <mxGeometry x="20" y="20" width="1120" height="770" as="geometry"/>
    </mxCell>''')

    # Заголовочная таблица Ramus (высота 80px)
    cells.append(f'''<mxCell id="{cell_prefix}_h_used" value="ИСПОЛЬЗУЕТСЯ В:" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;strokeWidth=1;align=left;verticalAlign=top;fontSize=10;fontFamily=Arial;spacingLeft=5;spacingTop=3;" vertex="1" parent="1">
      <mxGeometry x="20" y="20" width="160" height="80" as="geometry"/>
    </mxCell>''')

    cells.append(f'''<mxCell id="{cell_prefix}_h_meta" value="&lt;b&gt;АВТОР:&lt;/b&gt; {esc(author)}&lt;br&gt;&lt;b&gt;ПРОЕКТ:&lt;/b&gt; {esc(project)}&lt;br&gt;&lt;br&gt;&lt;b&gt;ЗАМЕЧАНИЯ:&lt;/b&gt; 1 2 3 4 5 6 7 8 9 10" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;strokeWidth=1;align=left;verticalAlign=top;fontSize=10;fontFamily=Arial;spacingLeft=5;spacingTop=3;" vertex="1" parent="1">
      <mxGeometry x="180" y="20" width="250" height="80" as="geometry"/>
    </mxCell>''')

    cells.append(f'''<mxCell id="{cell_prefix}_h_date" value="&lt;b&gt;ДАТА:&lt;/b&gt; {esc(date)}&lt;br&gt;&lt;b&gt;РЕВИЗИЯ:&lt;/b&gt; {esc(date)}" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;strokeWidth=1;align=left;verticalAlign=top;fontSize=10;fontFamily=Arial;spacingLeft=5;spacingTop=3;" vertex="1" parent="1">
      <mxGeometry x="430" y="20" width="140" height="80" as="geometry"/>
    </mxCell>''')

    cells.append(f'''<mxCell id="{cell_prefix}_h_status" value="{stat_check} РАЗРАБАТЫВАЕТСЯ&lt;br&gt;{draft_check} ЧЕРНОВИК&lt;br&gt;□ РЕКОМЕНДОВАНО&lt;br&gt;□ ПУБЛИКАЦИЯ" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;strokeWidth=1;align=left;verticalAlign=middle;fontSize=9.5;fontFamily=Arial;spacingLeft=5;" vertex="1" parent="1">
      <mxGeometry x="570" y="20" width="180" height="80" as="geometry"/>
    </mxCell>''')

    cells.append(f'''<mxCell id="{cell_prefix}_h_reader" value="ЧИТАТЕЛЬ&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;ДАТА&lt;br&gt;&lt;hr style=&quot;border:0.5px solid #000;&quot;&gt;&lt;br&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;strokeWidth=1;align=left;verticalAlign=top;fontSize=10;fontFamily=Arial;spacingLeft=5;spacingTop=3;" vertex="1" parent="1">
      <mxGeometry x="750" y="20" width="180" height="80" as="geometry"/>
    </mxCell>''')

    cells.append(f'''<mxCell id="{cell_prefix}_h_ctx" value="&lt;b&gt;КОНТЕКСТ:&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;center&gt;&lt;b style=&quot;font-size:13px;&quot;&gt;{esc(context)}&lt;/b&gt;&lt;/center&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;strokeWidth=1;align=left;verticalAlign=top;fontSize=10;fontFamily=Arial;spacingLeft=5;spacingTop=3;" vertex="1" parent="1">
      <mxGeometry x="930" y="20" width="210" height="80" as="geometry"/>
    </mxCell>''')

    return "\n".join(cells)

def ramus_footer(cell_prefix, node="Ветка: А-0", title="Мониторинг веб-ресурсов", page_num=1):
    """Генерирует нижнюю строку подвала Ramus IDEF0"""
    cells = []
    cells.append(f'''<mxCell id="{cell_prefix}_f_node" value="&lt;b&gt;Ветка: {esc(node)}&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;strokeWidth=1;align=left;verticalAlign=middle;fontSize=11;fontFamily=Arial;spacingLeft=10;" vertex="1" parent="1">
      <mxGeometry x="20" y="750" width="180" height="40" as="geometry"/>
    </mxCell>''')

    cells.append(f'''<mxCell id="{cell_prefix}_f_title" value="&lt;b&gt;Название:&lt;/b&gt; {esc(title)}" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;strokeWidth=1;align=center;verticalAlign=middle;fontSize=12;fontFamily=Arial;" vertex="1" parent="1">
      <mxGeometry x="200" y="750" width="740" height="40" as="geometry"/>
    </mxCell>''')

    cells.append(f'''<mxCell id="{cell_prefix}_f_num" value="&lt;b&gt;Номер: {page_num}&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;strokeWidth=1;align=center;verticalAlign=middle;fontSize=11;fontFamily=Arial;" vertex="1" parent="1">
      <mxGeometry x="940" y="750" width="200" height="40" as="geometry"/>
    </mxCell>''')

    return "\n".join(cells)

def ramus_block(cell_id, text, block_code, x, y, w, h, is_decomposed=False, is_purple=False):
    """Генерирует функциональный блок в стиле Ramus"""
    if is_purple:
        fill_col = "#F3E8FF"
        stroke_col = "#9333EA"
        txt_col = "#581C87"
    else:
        fill_col = "#FFFFFF"
        stroke_col = "#000000"
        txt_col = "#000000"

    decomp_html = ""
    if is_decomposed:
        decomp_html = f'''<mxCell id="{cell_id}_decomp_mark" value="" style="endArrow=none;html=1;strokeColor={stroke_col};strokeWidth=1.5;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="{x}" y="{y+15}" as="sourcePoint"/>
            <mxPoint x="{x+15}" y="{y}" as="targetPoint"/>
          </mxGeometry>
        </mxCell>'''

    block_xml = f'''<mxCell id="{cell_id}" value="&lt;div style=&quot;padding: 5px; font-weight: bold; color: {txt_col};&quot;&gt;{esc(text)}&lt;/div&gt;&lt;div style=&quot;position: absolute; right: 6px; bottom: 4px; text-align: right; font-weight: bold; font-size: 11px; color: {txt_col};&quot;&gt;{esc(block_code)}&lt;/div&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor={fill_col};strokeColor={stroke_col};strokeWidth=1.5;align=center;verticalAlign=middle;fontFamily=Arial;fontSize=11;" vertex="1" parent="1">
      <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
    </mxCell>
    {decomp_html}'''
    return block_xml

def ramus_arrow(arrow_id, label, points, is_purple=False, label_offset=(0, -10), align="center"):
    """
    Генерирует стрелку IDEF0 (ортогональную ломаную)
    """
    if is_purple:
        col = "#9333EA"
        font_col = "#7E22CE"
    else:
        col = "#000000"
        font_col = "#000000"

    p_start = points[0]
    p_end = points[-1]
    
    mid_points = ""
    if len(points) > 2:
        pts_xml = "\n".join([f'<mxPoint x="{p[0]}" y="{p[1]}"/>' for p in points[1:-1]])
        mid_points = f'''<Array as="points">
          {pts_xml}
        </Array>'''

    lx = points[0][0] + label_offset[0]
    ly = points[0][1] + label_offset[1]

    arrow_xml = f'''<mxCell id="{arrow_id}" value="" style="endArrow=classic;html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;strokeColor={col};strokeWidth=1.5;" edge="1" parent="1">
      <mxGeometry relative="1" as="geometry">
        <mxPoint x="{p_start[0]}" y="{p_start[1]}" as="sourcePoint"/>
        <mxPoint x="{p_end[0]}" y="{p_end[1]}" as="targetPoint"/>
        {mid_points}
      </mxGeometry>
    </mxCell>
    <mxCell id="{arrow_id}_lbl" value="{esc(label)}" style="text;html=1;align={align};verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;fontFamily=Arial;fontColor={font_col};" vertex="1" parent="1">
      <mxGeometry x="{lx}" y="{ly}" width="160" height="20" as="geometry"/>
    </mxCell>'''
    return arrow_xml

def build_page_as_is_a_minus_0():
    """Страница 1: AS-IS А-0 (Контекстная)"""
    header = ramus_header("p1", author="Шахсинов М. В.", project="Мониторинг веб-ресурсов (AS-IS)",
                          date="22.09.2026", context="ВЕРХ", is_draft=False)
    footer = ramus_footer("p1", node="А-0", title="Мониторинг доступности веб-ресурсов предприятия (AS-IS)", page_num=1)
    
    box = ramus_block("p1_b_a0", "Мониторинг доступности веб-ресурсов предприятия вручную", "А0", 410, 340, 340, 150, is_decomposed=True)
    
    arr_i1 = ramus_arrow("p1_i1", "Заявки на мониторинг узлов", [(100, 380), (410, 380)], label_offset=(10, -18), align="left")
    arr_i2 = ramus_arrow("p1_i2", "Сведения о целевых веб-ресурсах", [(100, 440), (410, 440)], label_offset=(10, -18), align="left")

    arr_c1 = ramus_arrow("p1_c1", "Регламент контроля доступности", [(480, 150), (480, 340)], label_offset=(-140, 40), align="right")
    arr_c2 = ramus_arrow("p1_c2", "Нормативы SLA и задержки", [(660, 150), (660, 340)], label_offset=(10, 40), align="left")

    arr_m1 = ramus_arrow("p1_m1", "Дежурный инженер мониторинга", [(480, 680), (480, 490)], label_offset=(-140, -40), align="right")
    arr_m2 = ramus_arrow("p1_m2", "ПК с утилитами cURL и ping", [(660, 680), (660, 490)], label_offset=(10, -40), align="left")

    arr_o1 = ramus_arrow("p1_o1", "Журнал инцидентов и отказов (Excel)", [(750, 380), (1060, 380)], label_offset=(20, -18), align="left")
    arr_o2 = ramus_arrow("p1_o2", "Извещения по почте и телефону", [(750, 440), (1060, 440)], label_offset=(20, -18), align="left")

    content = f"""<root>
      <mxCell id="0"/>
      <mxCell id="1" parent="0"/>
      {header}
      {footer}
      {box}
      {arr_i1}
      {arr_i2}
      {arr_c1}
      {arr_c2}
      {arr_m1}
      {arr_m2}
      {arr_o1}
      {arr_o2}
    </root>"""
    return content

def build_page_as_is_a0():
    """Страница 2: AS-IS А0 (Декомпозиция 2 уровня, 4 блока)"""
    header = ramus_header("p2", author="Шахсинов М. В.", project="Мониторинг веб-ресурсов (AS-IS)",
                          date="22.09.2026", context="А-0", is_draft=False)
    footer = ramus_footer("p2", node="А0", title="Мониторинг доступности веб-ресурсов предприятия (AS-IS)", page_num=2)

    b1 = ramus_block("p2_b1", "Прием и регистрация заявок на мониторинг", "А1", 130, 160, 180, 95, is_decomposed=False)
    b2 = ramus_block("p2_b2", "Ручной опрос и тестирование узлов", "А2", 370, 295, 180, 95, is_decomposed=True)
    b3 = ramus_block("p2_b3", "Анализ телеметрии и фиксация отказов", "А3", 610, 430, 180, 95, is_decomposed=False)
    b4 = ramus_block("p2_b4", "Ручное оповещение и отчетность", "А4", 850, 565, 180, 95, is_decomposed=False)

    arr_i1 = ramus_arrow("p2_i1", "Заявки на мониторинг", [(40, 190), (130, 190)], label_offset=(10, -18), align="left")
    arr_i2 = ramus_arrow("p2_i2", "Сведения о веб-ресурсах", [(40, 225), (130, 225)], label_offset=(10, -18), align="left")

    arr_12 = ramus_arrow("p2_12", "Реестр целевых адресов", [(310, 205), (340, 205), (340, 335), (370, 335)], label_offset=(5, -20), align="left")
    arr_23 = ramus_arrow("p2_23", "Протокол сетевых ответов", [(550, 340), (580, 340), (580, 470), (610, 470)], label_offset=(5, -20), align="left")
    arr_34 = ramus_arrow("p2_34", "Записи об инцидентах", [(790, 475), (820, 475), (820, 605), (850, 605)], label_offset=(5, -20), align="left")

    arr_o1 = ramus_arrow("p2_o1", "Журнал отказов (Excel)", [(1030, 595), (1110, 595)], label_offset=(10, -18), align="left")
    arr_o2 = ramus_arrow("p2_o2", "Извещения по почте", [(1030, 630), (1110, 630)], label_offset=(10, -18), align="left")

    arr_c1 = ramus_arrow("p2_c1", "Регламент контроля", [(220, 100), (220, 160)], label_offset=(-120, 15), align="right")
    arr_c2 = ramus_arrow("p2_c2", "Нормативы SLA", [(460, 100), (460, 295)], label_offset=(-120, 30), align="right")
    arr_c3 = ramus_arrow("p2_c3", "Нормативы SLA", [(700, 100), (700, 430)], label_offset=(-120, 30), align="right")
    arr_c4 = ramus_arrow("p2_c4", "Регламент оповещения", [(940, 100), (940, 565)], label_offset=(-140, 30), align="right")

    arr_m1 = ramus_arrow("p2_m1", "Дежурный инженер", [(220, 720), (220, 255)], label_offset=(-120, -30), align="right")
    arr_m2 = ramus_arrow("p2_m2", "Утилиты cURL и ping", [(460, 720), (460, 390)], label_offset=(-130, -30), align="right")
    arr_m3 = ramus_arrow("p2_m3", "Таблицы Excel", [(700, 720), (700, 525)], label_offset=(-120, -30), align="right")
    arr_m4 = ramus_arrow("p2_m4", "Корпоративная почта", [(940, 720), (940, 660)], label_offset=(-130, -30), align="right")

    content = f"""<root>
      <mxCell id="0"/>
      <mxCell id="1" parent="0"/>
      {header}
      {footer}
      {b1}
      {b2}
      {b3}
      {b4}
      {arr_i1}
      {arr_i2}
      {arr_12}
      {arr_23}
      {arr_34}
      {arr_o1}
      {arr_o2}
      {arr_c1}
      {arr_c2}
      {arr_c3}
      {arr_c4}
      {arr_m1}
      {arr_m2}
      {arr_m3}
      {arr_m4}
    </root>"""
    return content

def build_page_as_is_a2():
    """Страница 3: AS-IS А2 (Декомпозиция 3 уровня блока А2, 4 процесса)"""
    header = ramus_header("p3", author="Шахсинов М. В.", project="Мониторинг веб-ресурсов (AS-IS)",
                          date="22.09.2026", context="А2", is_draft=False)
    footer = ramus_footer("p3", node="А2", title="Ручной опрос и тестирование веб-узлов (AS-IS)", page_num=3)

    b1 = ramus_block("p3_b1", "Формирование разового списка адресов", "А21", 130, 160, 180, 95, is_decomposed=False)
    b2 = ramus_block("p3_b2", "Последовательный запуск HTTP/ICMP утилит", "А22", 370, 295, 180, 95, is_decomposed=False)
    b3 = ramus_block("p3_b3", "Ручной замер сетевых задержек и кодов", "А23", 610, 430, 180, 95, is_decomposed=False)
    b4 = ramus_block("p3_b4", "Формирование итогового протокола опроса", "А24", 850, 565, 180, 95, is_decomposed=False)

    arr_in = ramus_arrow("p3_in", "Реестр целевых адресов", [(40, 205), (130, 205)], label_offset=(10, -18), align="left")
    arr_12 = ramus_arrow("p3_12", "Список адресов для терминала", [(310, 205), (340, 205), (340, 335), (370, 335)], label_offset=(5, -20), align="left")
    arr_23 = ramus_arrow("p3_23", "Консольный вывод утилит", [(550, 340), (580, 340), (580, 470), (610, 470)], label_offset=(5, -20), align="left")
    arr_34 = ramus_arrow("p3_34", "Сводка сетевых задержек", [(790, 475), (820, 475), (820, 605), (850, 605)], label_offset=(5, -20), align="left")
    arr_out = ramus_arrow("p3_out", "Протокол сетевых ответов", [(1030, 610), (1110, 610)], label_offset=(10, -18), align="left")

    arr_c1 = ramus_arrow("p3_c1", "График ручных обходов", [(220, 100), (220, 160)], label_offset=(-140, 20), align="right")
    arr_c2 = ramus_arrow("p3_c2", "Инструкция по вызову cURL", [(460, 100), (460, 295)], label_offset=(-150, 20), align="right")
    arr_c3 = ramus_arrow("p3_c3", "Нормативы задержки SLA", [(700, 100), (700, 430)], label_offset=(-140, 20), align="right")
    arr_c4 = ramus_arrow("p3_c4", "Шаблон протокола опроса", [(940, 100), (940, 565)], label_offset=(-150, 20), align="right")

    arr_m1 = ramus_arrow("p3_m1", "Дежурный инженер", [(220, 720), (220, 255)], label_offset=(-120, -30), align="right")
    arr_m2 = ramus_arrow("p3_m2", "Утилиты cURL и ping", [(460, 720), (460, 390)], label_offset=(-130, -30), align="right")
    arr_m3 = ramus_arrow("p3_m3", "Дежурный инженер", [(700, 720), (700, 525)], label_offset=(-120, -30), align="right")
    arr_m4 = ramus_arrow("p3_m4", "Дежурный инженер", [(940, 720), (940, 660)], label_offset=(-120, -30), align="right")

    content = f"""<root>
      <mxCell id="0"/>
      <mxCell id="1" parent="0"/>
      {header}
      {footer}
      {b1}
      {b2}
      {b3}
      {b4}
      {arr_in}
      {arr_12}
      {arr_23}
      {arr_34}
      {arr_out}
      {arr_c1}
      {arr_c2}
      {arr_c3}
      {arr_c4}
      {arr_m1}
      {arr_m2}
      {arr_m3}
      {arr_m4}
    </root>"""
    return content

def build_page_to_be_a_minus_0():
    """Страница 4: TO-BE А-0 (Контекстная с фиолетовыми элементами автоматизации)"""
    header = ramus_header("p4", author="Шахсинов М. В.", project="ИС мониторинга веб-ресурсов Upward (TO-BE)",
                          date="22.09.2026", context="ВЕРХ", is_draft=False)
    footer = ramus_footer("p4", node="А-0", title="Автоматизированный мониторинг веб-ресурсов системой Upward (TO-BE)", page_num=4)

    box = ramus_block("p4_b_a0", "Автоматизированный мониторинг веб-ресурсов информационной системой «Upward»", "А0", 400, 340, 360, 150, is_decomposed=True, is_purple=True)

    arr_i1 = ramus_arrow("p4_i1", "Конфигурации целевых ресурсов", [(80, 370), (400, 370)], label_offset=(10, -18), align="left")
    arr_i2 = ramus_arrow("p4_i2", "Запросы на добавление сайтов через REST API", [(80, 430), (400, 430)], is_purple=True, label_offset=(10, -18), align="left")

    arr_c1 = ramus_arrow("p4_c1", "Политики безопасности и правила SSRF", [(470, 140), (470, 340)], is_purple=True, label_offset=(-180, 40), align="right")
    arr_c2 = ramus_arrow("p4_c2", "Нормативы SLA и интервалы опроса", [(670, 140), (670, 340)], label_offset=(10, 40), align="left")

    arr_m1 = ramus_arrow("p4_m1", "Системный администратор и инженеры", [(470, 680), (470, 490)], label_offset=(-180, -40), align="right")
    arr_m2 = ramus_arrow("p4_m2", "ИС Upward (Rust worker, TimescaleDB, Redis, Nginx, BFF)", [(670, 680), (670, 490)], is_purple=True, label_offset=(10, -40), align="left")

    arr_o1 = ramus_arrow("p4_o1", "Метрики (DNS, TLS, TTFB) в гипертаблице TimescaleDB", [(760, 370), (1080, 370)], is_purple=True, label_offset=(15, -18), align="left")
    arr_o2 = ramus_arrow("p4_o2", "Мгновенные вебхук-уведомления об авариях", [(760, 420), (1080, 420)], is_purple=True, label_offset=(15, -18), align="left")
    arr_o3 = ramus_arrow("p4_o3", "Аналитические отчеты об аптайме", [(760, 465), (1080, 465)], label_offset=(15, -18), align="left")

    content = f"""<root>
      <mxCell id="0"/>
      <mxCell id="1" parent="0"/>
      {header}
      {footer}
      {box}
      {arr_i1}
      {arr_i2}
      {arr_c1}
      {arr_c2}
      {arr_m1}
      {arr_m2}
      {arr_o1}
      {arr_o2}
      {arr_o3}
    </root>"""
    return content

def build_page_to_be_a0():
    """Страница 5: TO-BE А0 (Декомпозиция 2 уровня, 4 блока, фиолетовые новые элементы)"""
    header = ramus_header("p5", author="Шахсинов М. В.", project="ИС мониторинга веб-ресурсов Upward (TO-BE)",
                          date="22.09.2026", context="А-0", is_draft=False)
    footer = ramus_footer("p5", node="А0", title="Автоматизированный мониторинг веб-ресурсов системой Upward (TO-BE)", page_num=5)

    b1 = ramus_block("p5_b1", "Регистрация, валидация SSRF и верификация ресурсов", "А1", 120, 160, 190, 95, is_decomposed=True, is_purple=True)
    b2 = ramus_block("p5_b2", "Атомарный захват батчей и параллельный опрос узлов", "А2", 370, 295, 190, 95, is_decomposed=True, is_purple=True)
    b3 = ramus_block("p5_b3", "Анализ ответов, запись в гипертаблицу и детекция сбоев", "А3", 620, 430, 190, 95, is_decomposed=False, is_purple=True)
    b4 = ramus_block("p5_b4", "Агрегация метрик, отображение в Swagger/BFF и алертинг", "А4", 870, 565, 190, 95, is_decomposed=False, is_purple=True)

    arr_i1 = ramus_arrow("p5_i1", "Запросы через REST API", [(30, 190), (120, 190)], is_purple=True, label_offset=(5, -18), align="left")
    arr_i2 = ramus_arrow("p5_i2", "Конфигурации ресурсов", [(30, 225), (120, 225)], label_offset=(5, -18), align="left")

    arr_12 = ramus_arrow("p5_12", "Верифицированные сайты в БД", [(310, 205), (340, 205), (340, 335), (370, 335)], is_purple=True, label_offset=(5, -20), align="left")
    arr_23 = ramus_arrow("p5_23", "Сырые замеры сетевых зондов", [(560, 340), (590, 340), (590, 470), (620, 470)], is_purple=True, label_offset=(5, -20), align="left")
    arr_34 = ramus_arrow("p5_34", "Метрики и активные инциденты", [(810, 475), (840, 475), (840, 605), (870, 605)], is_purple=True, label_offset=(5, -20), align="left")

    arr_fb = ramus_arrow("p5_fb", "Фиксация last_check и сброс status=idle", [(940, 660), (940, 700), (440, 700), (440, 390)], is_purple=True, label_offset=(-40, 10), align="center")

    arr_o1 = ramus_arrow("p5_o1", "Временные ряды TimescaleDB", [(1060, 595), (1120, 595)], is_purple=True, label_offset=(5, -18), align="left")
    arr_o2 = ramus_arrow("p5_o2", "Вебхук-алерты об авариях", [(1060, 630), (1120, 630)], is_purple=True, label_offset=(5, -18), align="left")

    arr_c1 = ramus_arrow("p5_c1", "Политики безопасности SSRF", [(215, 100), (215, 160)], is_purple=True, label_offset=(-160, 20), align="right")
    arr_c2 = ramus_arrow("p5_c2", "SKIP LOCKED и buffer_unordered", [(465, 100), (465, 295)], is_purple=True, label_offset=(-160, 20), align="right")
    arr_c3 = ramus_arrow("p5_c3", "Пороги SLA и критерии аварий", [(715, 100), (715, 430)], label_offset=(-160, 20), align="right")
    arr_c4 = ramus_arrow("p5_c4", "Спецификация OpenAPI/Swagger", [(965, 100), (965, 565)], is_purple=True, label_offset=(-160, 20), align="right")

    arr_m1 = ramus_arrow("p5_m1", "ИС Upward: контроллер sites и SSRF-фильтр", [(215, 740), (215, 255)], is_purple=True, label_offset=(-170, -25), align="right")
    arr_m2 = ramus_arrow("p5_m2", "ИС Upward: асинхронный воркер Tokio и SQLx", [(465, 740), (465, 390)], is_purple=True, label_offset=(-170, -25), align="right")
    arr_m3 = ramus_arrow("p5_m3", "СУБД TimescaleDB (гипертаблица site_checks)", [(715, 740), (715, 525)], is_purple=True, label_offset=(-170, -25), align="right")
    arr_m4 = ramus_arrow("p5_m4", "Шлюз BFF (NestJS), Nginx и Swagger UI", [(965, 740), (965, 660)], is_purple=True, label_offset=(-170, -25), align="right")

    content = f"""<root>
      <mxCell id="0"/>
      <mxCell id="1" parent="0"/>
      {header}
      {footer}
      {b1}
      {b2}
      {b3}
      {b4}
      {arr_i1}
      {arr_i2}
      {arr_12}
      {arr_23}
      {arr_34}
      {arr_fb}
      {arr_o1}
      {arr_o2}
      {arr_c1}
      {arr_c2}
      {arr_c3}
      {arr_c4}
      {arr_m1}
      {arr_m2}
      {arr_m3}
      {arr_m4}
    </root>"""
    return content

def build_page_to_be_a1():
    """Страница 6: TO-BE А1 (Декомпозиция 3 уровня блока А1, 4 процесса)"""
    header = ramus_header("p6", author="Шахсинов М. В.", project="ИС мониторинга веб-ресурсов Upward (TO-BE)",
                          date="22.09.2026", context="А1", is_draft=False)
    footer = ramus_footer("p6", node="А1", title="Регистрация, валидация SSRF и верификация ресурсов (TO-BE)", page_num=6)

    b1 = ramus_block("p6_b1", "Прием параметров узла через REST API / Swagger", "А11", 120, 160, 190, 95, is_decomposed=False, is_purple=True)
    b2 = ramus_block("p6_b2", "Инспекция IP-адресов на SSRF и приватные сети", "А12", 370, 295, 190, 95, is_decomposed=False, is_purple=True)
    b3 = ramus_block("p6_b3", "Верификация владения доменом (DNS/Meta)", "А13", 620, 430, 190, 95, is_decomposed=False, is_purple=True)
    b4 = ramus_block("p6_b4", "Фиксация конфигурации ресурса в таблице sites", "А14", 870, 565, 190, 95, is_decomposed=False, is_purple=True)

    arr_in = ramus_arrow("p6_in", "Запросы на добавление сайтов", [(30, 205), (120, 205)], is_purple=True, label_offset=(5, -18), align="left")
    arr_12 = ramus_arrow("p6_12", "Непроверенная модель данных", [(310, 205), (340, 205), (340, 335), (370, 335)], is_purple=True, label_offset=(5, -20), align="left")
    arr_23 = ramus_arrow("p6_23", "Безопасный публичный URL", [(560, 340), (590, 340), (590, 470), (620, 470)], is_purple=True, label_offset=(5, -20), align="left")
    arr_34 = ramus_arrow("p6_34", "Подтвержденный статус домена", [(810, 475), (840, 475), (840, 605), (870, 605)], is_purple=True, label_offset=(5, -20), align="left")
    arr_out = ramus_arrow("p6_out", "Верифицированные записи сайтов", [(1060, 610), (1120, 610)], is_purple=True, label_offset=(5, -18), align="left")

    arr_c1 = ramus_arrow("p6_c1", "Схема DTO CreateSiteDto", [(215, 100), (215, 160)], is_purple=True, label_offset=(-150, 20), align="right")
    arr_c2 = ramus_arrow("p6_c2", "Список RFC 1918 и loopback", [(465, 100), (465, 295)], is_purple=True, label_offset=(-150, 20), align="right")
    arr_c3 = ramus_arrow("p6_c3", "Протокол DNS TXT / Meta", [(715, 100), (715, 430)], is_purple=True, label_offset=(-150, 20), align="right")
    arr_c4 = ramus_arrow("p6_c4", "Реляционная схема PostgreSQL", [(965, 100), (965, 565)], label_offset=(-150, 20), align="right")

    arr_m1 = ramus_arrow("p6_m1", "Маршрутизатор Axum", [(215, 740), (215, 255)], is_purple=True, label_offset=(-140, -25), align="right")
    arr_m2 = ramus_arrow("p6_m2", "Модуль dns_guard (Rust)", [(465, 740), (465, 390)], is_purple=True, label_offset=(-150, -25), align="right")
    arr_m3 = ramus_arrow("p6_m3", "Верификатор challenge_verifier", [(715, 740), (715, 525)], is_purple=True, label_offset=(-160, -25), align="right")
    arr_m4 = ramus_arrow("p6_m4", "SiteRepository (SQLx)", [(965, 740), (965, 660)], is_purple=True, label_offset=(-140, -25), align="right")

    content = f"""<root>
      <mxCell id="0"/>
      <mxCell id="1" parent="0"/>
      {header}
      {footer}
      {b1}
      {b2}
      {b3}
      {b4}
      {arr_in}
      {arr_12}
      {arr_23}
      {arr_34}
      {arr_out}
      {arr_c1}
      {arr_c2}
      {arr_c3}
      {arr_c4}
      {arr_m1}
      {arr_m2}
      {arr_m3}
      {arr_m4}
    </root>"""
    return content

def build_page_to_be_a2():
    """Страница 7: TO-BE А2 (Декомпозиция 3 уровня блока А2, 4 процесса)"""
    header = ramus_header("p7", author="Шахсинов М. В.", project="ИС мониторинга веб-ресурсов Upward (TO-BE)",
                          date="22.09.2026", context="А2", is_draft=False)
    footer = ramus_footer("p7", node="А2", title="Атомарный захват батчей и параллельный опрос узлов (TO-BE)", page_num=7)

    b1 = ramus_block("p7_b1", "Атомарный захват батча без гонок реплик", "А21", 120, 160, 190, 95, is_decomposed=False, is_purple=True)
    b2 = ramus_block("p7_b2", "Мультиплексирование асинхронных зондов", "А22", 370, 295, 190, 95, is_decomposed=False, is_purple=True)
    b3 = ramus_block("p7_b3", "Прецизионный замер фаз сетевого соединения", "А23", 620, 430, 190, 95, is_decomposed=False, is_purple=True)
    b4 = ramus_block("p7_b4", "Сборка результатов и сериализация телеметрии", "А24", 870, 565, 190, 95, is_decomposed=False, is_purple=True)

    arr_in = ramus_arrow("p7_in", "Верифицированные сайты в БД", [(30, 205), (120, 205)], is_purple=True, label_offset=(5, -18), align="left")
    arr_12 = ramus_arrow("p7_12", "Изолированный батч сайтов", [(310, 205), (340, 205), (340, 335), (370, 335)], is_purple=True, label_offset=(5, -20), align="left")
    arr_23 = ramus_arrow("p7_23", "Потоки сетевых HTTP-запросов", [(560, 340), (590, 340), (590, 470), (620, 470)], is_purple=True, label_offset=(5, -20), align="left")
    arr_34 = ramus_arrow("p7_34", "Сводка таймингов (DNS, TLS, TTFB)", [(810, 475), (840, 475), (840, 605), (870, 605)], is_purple=True, label_offset=(5, -20), align="left")
    arr_out = ramus_arrow("p7_out", "Сырые замеры сетевых зондов", [(1060, 610), (1120, 610)], is_purple=True, label_offset=(5, -18), align="left")

    arr_c1 = ramus_arrow("p7_c1", "FOR UPDATE SKIP LOCKED", [(215, 100), (215, 160)], is_purple=True, label_offset=(-160, 20), align="right")
    arr_c2 = ramus_arrow("p7_c2", "Параметр buffer_unordered", [(465, 100), (465, 295)], is_purple=True, label_offset=(-160, 20), align="right")
    arr_c3 = ramus_arrow("p7_c3", "Тайм-ауты сетевых сокетов", [(715, 100), (715, 430)], label_offset=(-160, 20), align="right")
    arr_c4 = ramus_arrow("p7_c4", "Схема DTO PingRecord", [(965, 100), (965, 565)], is_purple=True, label_offset=(-160, 20), align="right")

    arr_m1 = ramus_arrow("p7_m1", "Пул соединений SQLx", [(215, 740), (215, 255)], is_purple=True, label_offset=(-140, -25), align="right")
    arr_m2 = ramus_arrow("p7_m2", "Среда исполнения Tokio", [(465, 740), (465, 390)], is_purple=True, label_offset=(-140, -25), align="right")
    arr_m3 = ramus_arrow("p7_m3", "Клиент Reqwest и Instant", [(715, 740), (715, 525)], is_purple=True, label_offset=(-150, -25), align="right")
    arr_m4 = ramus_arrow("p7_m4", "Библиотека Serde JSON", [(965, 740), (965, 660)], is_purple=True, label_offset=(-140, -25), align="right")

    content = f"""<root>
      <mxCell id="0"/>
      <mxCell id="1" parent="0"/>
      {header}
      {footer}
      {b1}
      {b2}
      {b3}
      {b4}
      {arr_in}
      {arr_12}
      {arr_23}
      {arr_34}
      {arr_out}
      {arr_c1}
      {arr_c2}
      {arr_c3}
      {arr_c4}
      {arr_m1}
      {arr_m2}
      {arr_m3}
      {arr_m4}
    </root>"""
    return content

def build_full_drawio_xml():
    pages = [
        ("p_as_is_a0_ctx", "AS-IS: А-0 Контекст", build_page_as_is_a_minus_0()),
        ("p_as_is_a0_decomp", "AS-IS: А0 Декомпозиция 2 ур.", build_page_as_is_a0()),
        ("p_as_is_a2_decomp", "AS-IS: А2 Декомпозиция 3 ур.", build_page_as_is_a2()),
        ("p_to_be_a0_ctx", "TO-BE: А-0 Контекст", build_page_to_be_a_minus_0()),
        ("p_to_be_a0_decomp", "TO-BE: А0 Декомпозиция 2 ур.", build_page_to_be_a0()),
        ("p_to_be_a1_decomp", "TO-BE: А1 Декомпозиция 3 ур.", build_page_to_be_a1()),
        ("p_to_be_a2_decomp", "TO-BE: А2 Декомпозиция 3 ур.", build_page_to_be_a2()),
    ]

    xml = ['<mxfile host="app.diagrams.net" modified="2026-09-22T12:00:00.000Z" agent="Ramus IDEF0 Multi-Page Generator" version="21.6.8" type="device">']
    for pid, pname, pcontent in pages:
        xml.append(f'  <diagram id="{pid}" name="{esc(pname)}">')
        xml.append('    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" background="#FFFEEB" math="0" shadow="0">')
        xml.append(pcontent)
        xml.append('    </mxGraphModel>')
        xml.append('  </diagram>')
    xml.append('</mxfile>')
    return "\n".join(xml)

def main():
    output_path = "/home/zerok/projects/upward/idef0_monitoring_upward.drawio"
    xml_content = build_full_drawio_xml()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print(f"Full 7-page Ramus IDEF0 diagram successfully saved -> {output_path} ({len(xml_content)} bytes)")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GoodNotes iPad Pro 11" 프로젝트 플래너 (2026 - 2027)
미니멀 다크 · 주 시작 일요일 · 한글 · 10 프로젝트 슬롯
연간 → 월간 → 주간, 프로젝트 상세, 회의록 전부 하이퍼링크로 연결
"""
from datetime import date, timedelta
import calendar
import sys
import os

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# ========== CLI 옵션 ==========
SINGLE_YEAR = None
if '--year' in sys.argv:
    SINGLE_YEAR = int(sys.argv[sys.argv.index('--year') + 1])
LANDSCAPE = '--landscape' in sys.argv

# ========== 페이지 (iPad Pro 11" 네이티브) ==========
if LANDSCAPE:
    PAGE_W, PAGE_H = 2388, 1668
else:
    PAGE_W, PAGE_H = 1668, 2388
MX = 100
MT = 140
MB = 130

# ========== 색상 ==========
BG       = HexColor('#1c2030')
PANEL    = HexColor('#262b3c')
FG       = HexColor('#ffffff')
DIM      = HexColor('#b8bfd0')
FAINT    = HexColor('#565c72')
GRID     = HexColor('#3a4058')
ACCENT   = HexColor('#64b5ff')
HILITE   = HexColor('#ffd666')
SUN      = HexColor('#ff8a8a')
SAT      = HexColor('#89b4ff')
HOLIDAY  = HexColor('#ffb2ba')
HOLI_SUB = HexColor('#ffd6a8')   # 대체공휴일 (오렌지 톤)

# ========== 폰트 ==========
FONT_DIR = os.path.join(os.path.dirname(__file__), 'fonts')
FONT   = 'NotoSansKR'
FONT_B = 'NotoSansKRBold'
FONT_M = 'NotoSansKRMedium'
FONT_L = 'NotoSansKRLight'
pdfmetrics.registerFont(TTFont(FONT,   os.path.join(FONT_DIR, 'NotoSansKR-Regular.ttf')))
pdfmetrics.registerFont(TTFont(FONT_B, os.path.join(FONT_DIR, 'NotoSansKR-Bold.ttf')))
pdfmetrics.registerFont(TTFont(FONT_M, os.path.join(FONT_DIR, 'NotoSansKR-Medium.ttf')))
pdfmetrics.registerFont(TTFont(FONT_L, os.path.join(FONT_DIR, 'NotoSansKR-Light.ttf')))

_orient = '_landscape' if LANDSCAPE else ''
if SINGLE_YEAR is not None:
    YEARS = [SINGLE_YEAR]
    OUTPUT = f'Project_Planner_{SINGLE_YEAR}{_orient}.pdf'
else:
    YEARS = [2026, 2027]
    OUTPUT = f'Project_Planner_2026-2027{_orient}.pdf'
PROJECT_SLOTS = 10
MEETING_SLOTS = 30

WEEKDAYS_KR = ['일', '월', '화', '수', '목', '금', '토']

# ========== 공휴일 (이름, 대체공휴일 여부) ==========
HOLIDAYS = {
    # 2026
    date(2026, 1, 1):   ('신정', False),
    date(2026, 2, 16):  ('설날', False),
    date(2026, 2, 17):  ('설날', False),
    date(2026, 2, 18):  ('설날', False),
    date(2026, 3, 1):   ('삼일절', False),
    date(2026, 3, 2):   ('대체공휴일', True),
    date(2026, 5, 5):   ('어린이날', False),
    date(2026, 5, 24):  ('부처님오신날', False),
    date(2026, 5, 25):  ('대체공휴일', True),
    date(2026, 6, 6):   ('현충일', False),
    date(2026, 8, 15):  ('광복절', False),
    date(2026, 8, 17):  ('대체공휴일', True),
    date(2026, 9, 24):  ('추석', False),
    date(2026, 9, 25):  ('추석', False),
    date(2026, 9, 26):  ('추석', False),
    date(2026, 10, 3):  ('개천절', False),
    date(2026, 10, 5):  ('대체공휴일', True),
    date(2026, 10, 9):  ('한글날', False),
    date(2026, 12, 25): ('성탄절', False),
    # 2027
    date(2027, 1, 1):   ('신정', False),
    date(2027, 2, 6):   ('설날', False),
    date(2027, 2, 7):   ('설날', False),
    date(2027, 2, 8):   ('설날', False),
    date(2027, 2, 9):   ('대체공휴일', True),
    date(2027, 3, 1):   ('삼일절', False),
    date(2027, 5, 5):   ('어린이날', False),
    date(2027, 5, 13):  ('부처님오신날', False),
    date(2027, 6, 6):   ('현충일', False),
    date(2027, 6, 7):   ('대체공휴일', True),
    date(2027, 8, 15):  ('광복절', False),
    date(2027, 8, 16):  ('대체공휴일', True),
    date(2027, 9, 14):  ('추석', False),
    date(2027, 9, 15):  ('추석', False),
    date(2027, 9, 16):  ('추석', False),
    date(2027, 10, 3):  ('개천절', False),
    date(2027, 10, 4):  ('대체공휴일', True),
    date(2027, 10, 9):  ('한글날', False),
    date(2027, 10, 11): ('대체공휴일', True),
    date(2027, 12, 25): ('성탄절', False),
}


def is_holiday(d):
    return d in HOLIDAYS


def holiday_color(d):
    if d not in HOLIDAYS:
        return None
    return HOLI_SUB if HOLIDAYS[d][1] else HOLIDAY


def holiday_name(d):
    if d not in HOLIDAYS:
        return ''
    return HOLIDAYS[d][0]


# ========== 날짜 유틸 ==========
def sunday_of(d):
    return d - timedelta(days=(d.weekday() + 1) % 7)


def thursday_of(sunday):
    return sunday + timedelta(days=4)


def week_label(sunday):
    """Thursday rule 로 연도/주차 결정"""
    thu = thursday_of(sunday)
    y = thu.year
    jan1 = date(y, 1, 1)
    offset = (3 - jan1.weekday()) % 7
    first_thu = jan1 + timedelta(days=offset)
    wk = (thu - first_thu).days // 7 + 1
    return y, wk


def all_weeks():
    start = sunday_of(date(YEARS[0], 1, 1))
    end = sunday_of(date(YEARS[-1], 12, 31))
    cur = start
    out = []
    while cur <= end:
        out.append(cur)
        cur += timedelta(days=7)
    return out


# ========== 책갈피 키 ==========
def bm_cover():       return 'cover'
def bm_index():       return 'idx'
def bm_annual(y):     return f'ann_{y}'
def bm_month(y, m):   return f'mon_{y}_{m:02d}'
def bm_week(sun):     return f'wk_{sun.strftime("%Y%m%d")}'
def bm_projects():    return 'projects'
def bm_project(i):    return f'prj_{i:02d}'
def bm_meetings():    return 'meetings'
def bm_meeting(i):    return f'mtg_{i:02d}'


# ========== 저수준 그리기 헬퍼 ==========
def fill_bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)


def text(c, s, x, y, size, color=FG, font=FONT, anchor='left'):
    c.setFillColor(color)
    c.setFont(font, size)
    if anchor == 'left':
        c.drawString(x, y, s)
    elif anchor == 'center':
        c.drawCentredString(x, y, s)
    elif anchor == 'right':
        c.drawRightString(x, y, s)


def hline(c, x1, y, x2, color=GRID, width=1):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)


def vline(c, x, y1, y2, color=GRID, width=1):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x, y1, x, y2)


def box(c, x, y, w, h, stroke=GRID, fill=None, width=1, radius=0):
    c.setStrokeColor(stroke)
    c.setLineWidth(width)
    if fill is not None:
        c.setFillColor(fill)
    if radius > 0:
        c.roundRect(x, y, w, h, radius, stroke=1, fill=1 if fill is not None else 0)
    else:
        c.rect(x, y, w, h, stroke=1, fill=1 if fill is not None else 0)


def link(c, dest, x, y, w, h):
    """투명 클릭 영역으로 내부 하이퍼링크 생성. Border 는 PDF 배열 문자열로 전달 (콤마 들어가면 invalid)."""
    c.linkAbsolute('', dest, Rect=(x, y, x + w, y + h), Border='[0 0 0]')


def page_frame(c, title_main, title_sub='', crumb=''):
    # crumb 인자는 호환을 위해 유지하되 표시하지 않음 (배경 작은 글씨 제거 요청)
    text(c, title_main, MX, PAGE_H - 130, 64, FG, FONT_B)
    if title_sub:
        text(c, title_sub, MX + c.stringWidth(title_main, FONT_B, 64) + 32,
             PAGE_H - 130, 30, DIM, FONT_L)
    hline(c, MX, PAGE_H - 168, PAGE_W - MX, FAINT, 1)


def nav_bar(c, items):
    """하단 네비. items: [(label, dest), ...] / dest=None이거나 label=''인 항목은 건너뜀."""
    items = [(lbl, dest) for lbl, dest in items if lbl]
    y = 60
    gap = 30
    widths = [c.stringWidth(lbl, FONT, 24) + 70 for lbl, _ in items]
    total = sum(widths) + gap * (len(items) - 1)
    x = (PAGE_W - total) / 2
    for (lbl, dest), w in zip(items, widths):
        active = dest is not None
        stroke = ACCENT if active else FAINT
        fg = FG if active else DIM
        box(c, x, y, w, 64, stroke=stroke, width=1.2, radius=12)
        text(c, lbl, x + w / 2, y + 22, 24, fg, FONT, 'center')
        if active:
            link(c, dest, x, y, w, 64)
        x += w + gap


# ========== 표지 ==========
def page_cover(c):
    fill_bg(c)
    c.bookmarkPage(bm_cover())

    text(c, 'PROJECT  PLANNER', PAGE_W / 2, PAGE_H - 320, 50, DIM, FONT_L, 'center')

    cx = PAGE_W / 2
    if len(YEARS) == 1:
        cy = PAGE_H / 2 + 100
        text(c, f'{YEARS[0]}', cx, cy, 320, FG, FONT_B, 'center')
        hline(c, cx - 240, cy - 280, cx - 80, ACCENT, 2)
        hline(c, cx + 80, cy - 280, cx + 240, ACCENT, 2)
        text(c, '프로젝트 · 주간 · 회의록 통합 플래너',
             cx, cy - 360, 32, DIM, FONT_L, 'center')
    else:
        cy = PAGE_H / 2 + 240
        text(c, f'{YEARS[0]}', cx, cy,        260, FG,  FONT_B, 'center')
        text(c, f'{YEARS[-1]}', cx, cy - 380,  260, FG,  FONT_B, 'center')
        hline(c, cx - 240, cy - 200, cx - 80, ACCENT, 2)
        hline(c, cx + 80, cy - 200, cx + 240, ACCENT, 2)
        text(c, f'{len(YEARS)}개년 프로젝트 · 주간 · 회의록 통합 플래너',
             cx, cy - 540, 32, DIM, FONT_L, 'center')

    text(c, 'NAME', MX, 380, 22, DIM, FONT_L)
    hline(c, MX + 110, 386, MX + 700, FAINT, 1)
    text(c, 'TEAM', MX, 310, 22, DIM, FONT_L)
    hline(c, MX + 110, 316, MX + 700, FAINT, 1)

    btn_y = 470
    btn_h = 100
    btns = [('목차', bm_index())]
    for y in YEARS:
        btns.append((f'{y} 연간', bm_annual(y)))
    btns.append(('프로젝트', bm_projects()))
    btns.append(('회의록', bm_meetings()))
    bw = (PAGE_W - 2 * MX - 14 * (len(btns) - 1)) / len(btns)
    for i, (lbl, d) in enumerate(btns):
        x = MX + i * (bw + 14)
        box(c, x, btn_y, bw, btn_h, stroke=ACCENT, width=1.4, radius=14)
        text(c, lbl, x + bw / 2, btn_y + 38, 30, FG, FONT, 'center')
        link(c, d, x, btn_y, bw, btn_h)

    c.showPage()


# ========== 목차 (포트레이트: 3컬럼 / 가로: 4컬럼) ==========
def page_index(c):
    fill_bg(c)
    c.bookmarkPage(bm_index())
    page_frame(c, '목차', 'Contents', '표지')
    link(c, bm_cover(), MX, PAGE_H - 110, 220, 38)

    cols = 4 if LANDSCAPE else 3
    gap = 40
    col_w = (PAGE_W - 2 * MX - gap * (cols - 1)) / cols
    top_y = PAGE_H - 250

    def section(x, y, title, entries, row_spacing=50):
        text(c, title, x, y, 30, ACCENT, FONT_B)
        hline(c, x, y - 18, x + col_w, FAINT, 1)
        ey = y - 64
        for label, dest in entries:
            text(c, label, x + 14, ey, 24, FG, FONT)
            if dest:
                link(c, dest, x, ey - 14, col_w, row_spacing - 4)
            ey -= row_spacing
        return ey

    if LANDSCAPE:
        # 4 컬럼: 연간+월간 / 월간(또 한해) or 프로젝트 / 회의록 분할
        x1 = MX
        y1 = section(x1, top_y, '연간 달력', [(f'{y}', bm_annual(y)) for y in YEARS])
        y1 -= 36
        entries = [(f'{YEARS[0]}  {m:02d}월', bm_month(YEARS[0], m)) for m in range(1, 13)]
        y1 = section(x1, y1, f'{YEARS[0]} 월간', entries)

        x2 = MX + (col_w + gap)
        if len(YEARS) > 1:
            entries2 = [(f'{YEARS[1]}  {m:02d}월', bm_month(YEARS[1], m)) for m in range(1, 13)]
            section(x2, top_y, f'{YEARS[1]} 월간', entries2)
        else:
            section(x2, top_y, '프로젝트',
                    [('프로젝트 목록', bm_projects())] +
                    [(f'P{i:02d}', bm_project(i)) for i in range(1, PROJECT_SLOTS + 1)])

        x3 = MX + 2 * (col_w + gap)
        if len(YEARS) > 1:
            section(x3, top_y, '프로젝트',
                    [('프로젝트 목록', bm_projects())] +
                    [(f'P{i:02d}', bm_project(i)) for i in range(1, PROJECT_SLOTS + 1)])
            x4 = MX + 3 * (col_w + gap)
            section(x4, top_y, '회의록',
                    [('회의록 목록', bm_meetings())] +
                    [(f'M{i:02d}', bm_meeting(i)) for i in range(1, MEETING_SLOTS + 1)],
                    row_spacing=38)
        else:
            section(x3, top_y, '회의록',
                    [('회의록 목록', bm_meetings())] +
                    [(f'M{i:02d}', bm_meeting(i)) for i in range(1, MEETING_SLOTS + 1)],
                    row_spacing=38)
    else:
        # 포트레이트: 3 컬럼
        x1 = MX
        y1 = top_y
        y1 = section(x1, y1, '연간 달력', [(f'{y}', bm_annual(y)) for y in YEARS])
        for y in YEARS:
            y1 -= 36
            entries = [(f'{y}  {m:02d}월', bm_month(y, m)) for m in range(1, 13)]
            y1 = section(x1, y1, f'{y} 월간', entries)

        x2 = MX + col_w + gap
        section(x2, top_y, '프로젝트',
                [('프로젝트 목록', bm_projects())] +
                [(f'P{i:02d}', bm_project(i)) for i in range(1, PROJECT_SLOTS + 1)])

        x3 = MX + 2 * (col_w + gap)
        section(x3, top_y, '회의록',
                [('회의록 목록', bm_meetings())] +
                [(f'M{i:02d}', bm_meeting(i)) for i in range(1, MEETING_SLOTS + 1)],
                row_spacing=46)

    nav_items = [('표지', bm_cover())]
    for y in YEARS:
        nav_items.append((f'{y} 연간', bm_annual(y)))
    nav_items.append(('프로젝트', bm_projects()))
    nav_items.append(('회의록', bm_meetings()))
    nav_bar(c, nav_items)
    c.showPage()


# ========== 연간 ==========
def page_annual(c, year):
    fill_bg(c)
    c.bookmarkPage(bm_annual(year))
    page_frame(c, f'{year}', '연간 달력', f'목차  ›  {year}')
    link(c, bm_index(), MX, PAGE_H - 110, 240, 38)

    # 분기 목표 패널
    top_y = PAGE_H - 240
    qh = 220
    qgap = 28
    qw = (PAGE_W - 2 * MX - 3 * qgap) / 4
    for i, q in enumerate(['Q1 목표', 'Q2 목표', 'Q3 목표', 'Q4 목표']):
        x = MX + i * (qw + qgap)
        box(c, x, top_y - qh, qw, qh, stroke=FAINT, width=1, radius=12)
        text(c, q, x + 24, top_y - 56, 26, ACCENT, FONT_B)
        for k in range(1, 4):
            hline(c, x + 24, top_y - 96 - k * 38, x + qw - 24, FAINT, 0.6)

    # 12개월 미니 달력 (포트레이트: 4×3 / 가로: 6×2)
    grid_top = top_y - qh - 80
    grid_bottom = MB + 130
    grid_h = grid_top - grid_bottom
    if LANDSCAPE:
        ncols, nrows = 6, 2
    else:
        ncols, nrows = 4, 3
    cell_w = (PAGE_W - 2 * MX - (ncols - 1) * qgap) / ncols
    cell_h = (grid_h - (nrows - 1) * qgap) / nrows

    for m in range(1, 13):
        row = (m - 1) // ncols
        col = (m - 1) % ncols
        x = MX + col * (cell_w + qgap)
        y = grid_top - (row + 1) * cell_h - row * qgap

        box(c, x, y, cell_w, cell_h, stroke=FAINT, width=1, radius=12)
        text(c, f'{m}월', x + 24, y + cell_h - 50, 32, FG, FONT_B)
        link(c, bm_month(year, m), x, y, cell_w, cell_h)

        # 미니 달력
        cal = calendar.Calendar(firstweekday=6)
        weeks = cal.monthdayscalendar(year, m)
        head_y = y + cell_h - 100
        cw = (cell_w - 48) / 7
        for wi, wd in enumerate(WEEKDAYS_KR):
            color = SUN if wi == 0 else (SAT if wi == 6 else DIM)
            text(c, wd, x + 24 + cw * wi + cw / 2, head_y, 16, color, FONT, 'center')
        hline(c, x + 24, head_y - 10, x + cell_w - 24, FAINT, 0.5)

        for ri, wk_row in enumerate(weeks):
            for di, d in enumerate(wk_row):
                if d == 0:
                    continue
                dx = x + 24 + cw * di + cw / 2
                dy = head_y - 32 - ri * 28
                dt = date(year, m, d)
                if is_holiday(dt):
                    color = holiday_color(dt)
                elif di == 0:
                    color = SUN
                elif di == 6:
                    color = SAT
                else:
                    color = FG
                text(c, str(d), dx, dy, 16, color, FONT, 'center')

    others = [y for y in YEARS if y != year]
    nav_items = [('표지', bm_cover()), ('목차', bm_index())]
    if others:
        nav_items.append((f'{others[0]} 연간', bm_annual(others[0])))
    nav_items.append((f'{year}.1월', bm_month(year, 1)))
    nav_items.append(('프로젝트', bm_projects()))
    nav_bar(c, nav_items)
    c.showPage()


# ========== 월간 ==========
def page_month(c, year, month):
    fill_bg(c)
    c.bookmarkPage(bm_month(year, month))
    page_frame(c, f'{year}년 {month}월', f'{calendar.month_name[month]}',
               f'{year} 연간  ›  {month}월')
    link(c, bm_annual(year), MX, PAGE_H - 110, 280, 38)

    cal_x = MX
    cal_w = PAGE_W - 2 * MX - 560
    panel_x = cal_x + cal_w + 50
    panel_w = PAGE_W - MX - panel_x

    top_y = PAGE_H - 230
    bottom_y = MB + 110

    header_h = 70
    wcol_w = cal_w / 7
    for wi, wd in enumerate(WEEKDAYS_KR):
        color = SUN if wi == 0 else (SAT if wi == 6 else DIM)
        text(c, wd, cal_x + wcol_w * wi + wcol_w / 2,
             top_y - 46, 28, color, FONT_B, 'center')
    hline(c, cal_x, top_y - header_h, cal_x + cal_w, FAINT, 1)

    cal = calendar.Calendar(firstweekday=6)
    weeks = cal.monthdatescalendar(year, month)
    while len(weeks) < 6:
        last = weeks[-1][-1]
        weeks.append([last + timedelta(days=i + 1) for i in range(7)])
    rows = len(weeks)
    grid_top = top_y - header_h
    grid_h = grid_top - bottom_y
    row_h = grid_h / rows

    for i in range(8):
        x = cal_x + wcol_w * i
        vline(c, x, grid_top, bottom_y, GRID, 0.6)
    for i in range(rows + 1):
        y = grid_top - row_h * i
        hline(c, cal_x, y, cal_x + cal_w, GRID, 0.6)

    for ri, wk in enumerate(weeks):
        sun = wk[0]
        has_week_page = sun in ALL_WEEKS_SET
        if has_week_page:
            _, wk_num = week_label(sun)
            tag = f'W{wk_num:02d}'
            text(c, tag, cal_x - 56, grid_top - row_h * ri - 38, 16, DIM, FONT_L)
            link(c, bm_week(sun), cal_x - 64, grid_top - row_h * (ri + 1),
                 64, row_h)
        for di, d in enumerate(wk):
            cx = cal_x + wcol_w * di
            cy = grid_top - row_h * (ri + 1)
            is_this_month = d.month == month
            holi = is_holiday(d) and is_this_month

            if holi:
                color = holiday_color(d)
            elif di == 0:
                color = SUN
            elif di == 6:
                color = SAT
            else:
                color = FG
            if not is_this_month:
                color = FAINT

            # 날짜 (셀 좌상단)
            text(c, f'{d.day}', cx + 18, cy + row_h - 42, 26,
                 color, FONT_B if is_this_month else FONT_L)
            # 공휴일명 (날짜 아래에 별행)
            if holi:
                text(c, holiday_name(d), cx + 18, cy + row_h - 70, 13,
                     holiday_color(d), FONT_L)

            if has_week_page:
                link(c, bm_week(sun), cx, cy, wcol_w, row_h)

    # 우측 패널 - 가로 모드는 섹션 높이 압축
    y = top_y
    if LANDSCAPE:
        # 목표 4줄 / 핵심 3줄 / 리뷰 4줄, 행 간격 50pt
        text(c, '이달의 목표', panel_x, y - 50, 26, ACCENT, FONT_B)
        box(c, panel_x, y - 290, panel_w, 220, stroke=FAINT, width=1, radius=12)
        for i in range(4):
            ly = y - 110 - i * 50
            text(c, '□', panel_x + 22, ly, 22, DIM, FONT)
            hline(c, panel_x + 60, ly - 10, panel_x + panel_w - 24, FAINT, 0.6)

        text(c, '핵심 지표', panel_x, y - 330, 26, ACCENT, FONT_B)
        box(c, panel_x, y - 530, panel_w, 180, stroke=FAINT, width=1, radius=12)
        for i in range(3):
            ly = y - 390 - i * 54
            text(c, '·', panel_x + 26, ly, 24, DIM, FONT)
            hline(c, panel_x + 54, ly - 10, panel_x + panel_w - 24, FAINT, 0.6)

        text(c, '이달의 리뷰', panel_x, y - 570, 26, ACCENT, FONT_B)
        box(c, panel_x, y - 810, panel_w, 220, stroke=FAINT, width=1, radius=12)
        for i in range(4):
            ly = y - 630 - i * 50
            hline(c, panel_x + 26, ly, panel_x + panel_w - 24, FAINT, 0.6)
    else:
        text(c, '이달의 목표', panel_x, y - 50, 26, ACCENT, FONT_B)
        box(c, panel_x, y - 380, panel_w, 310, stroke=FAINT, width=1, radius=12)
        for i in range(5):
            ly = y - 110 - i * 56
            text(c, '□', panel_x + 22, ly, 22, DIM, FONT)
            hline(c, panel_x + 60, ly - 10, panel_x + panel_w - 24, FAINT, 0.6)

        text(c, '핵심 지표', panel_x, y - 420, 26, ACCENT, FONT_B)
        box(c, panel_x, y - 700, panel_w, 260, stroke=FAINT, width=1, radius=12)
        for i in range(4):
            ly = y - 480 - i * 60
            text(c, '·', panel_x + 26, ly, 24, DIM, FONT)
            hline(c, panel_x + 54, ly - 10, panel_x + panel_w - 24, FAINT, 0.6)

        text(c, '이달의 리뷰', panel_x, y - 750, 26, ACCENT, FONT_B)
        box(c, panel_x, y - 1100, panel_w, 330, stroke=FAINT, width=1, radius=12)
        for i in range(5):
            ly = y - 810 - i * 56
            hline(c, panel_x + 26, ly, panel_x + panel_w - 24, FAINT, 0.6)

    prev_y, prev_m = (year - 1, 12) if month == 1 else (year, month - 1)
    next_y, next_m = (year + 1, 1) if month == 12 else (year, month + 1)
    prev_dest = bm_month(prev_y, prev_m) if prev_y in YEARS else None
    next_dest = bm_month(next_y, next_m) if next_y in YEARS else None
    nav_bar(c, [('표지', bm_cover()),
                ('목차', bm_index()),
                (f'{year} 연간', bm_annual(year)),
                (f'◀ {prev_m}월' if prev_dest else '', prev_dest),
                (f'{next_m}월 ▶' if next_dest else '', next_dest)])
    c.showPage()


# ========== 주간 (가로 사이드바 레이아웃) ==========
def _page_week_landscape(c, sunday, mon_y, mon_m):
    # 좌 사이드바 (priority+focus+memo+review), 우 7일 그리드
    top_y = PAGE_H - 200
    side_w = 720
    side_x = MX
    grid_x = MX + side_w + 60
    grid_w = PAGE_W - MX - grid_x

    # === 사이드바 ===
    # 우선순위
    pri_h = 480
    box(c, side_x, top_y - pri_h, side_w, pri_h, stroke=FAINT, width=1, radius=14)
    text(c, '우선순위', side_x + 32, top_y - 56, 30, ACCENT, FONT_B)
    text(c, 'A · B · C', side_x + 220, top_y - 56, 16, DIM, FONT_L)
    rows = [('A', 3), ('B', 3), ('C', 3)]
    ry = top_y - 130
    for tier, count in rows:
        for i in range(1, count + 1):
            text(c, f'{tier}{i}', side_x + 36, ry, 22, ACCENT if tier == 'A' else DIM, FONT_B)
            text(c, '□', side_x + 96, ry, 24, DIM, FONT)
            hline(c, side_x + 138, ry - 14, side_x + side_w - 36, FAINT, 0.6)
            ry -= 38
        ry -= 12

    # 이번 주 집중
    foc_y = top_y - pri_h - 30
    foc_h = 240
    box(c, side_x, foc_y - foc_h, side_w, foc_h, stroke=FAINT, width=1, radius=14)
    text(c, '이번 주 집중', side_x + 32, foc_y - 50, 28, ACCENT, FONT_B)
    for i in range(3):
        ly = foc_y - 110 - i * 56
        text(c, '◆', side_x + 36, ly, 22, HILITE, FONT)
        hline(c, side_x + 80, ly - 14, side_x + side_w - 36, FAINT, 0.6)

    # 메모
    mem_y = foc_y - foc_h - 30
    mem_h = 320
    box(c, side_x, mem_y - mem_h, side_w, mem_h, stroke=FAINT, width=1, radius=14)
    text(c, '메모', side_x + 32, mem_y - 50, 28, ACCENT, FONT_B)
    for i in range(5):
        ly = mem_y - 110 - i * 50
        hline(c, side_x + 36, ly, side_x + side_w - 36, FAINT, 0.6)

    # 잘한 것 / 개선할 것 (가로 2분할)
    rev_y = mem_y - mem_h - 30
    rev_h = 200
    rev_w = (side_w - 20) / 2
    for i, lbl in enumerate(['잘한 것', '개선할 것']):
        rx = side_x + i * (rev_w + 20)
        box(c, rx, rev_y - rev_h, rev_w, rev_h, stroke=FAINT, width=1, radius=14)
        text(c, lbl, rx + 24, rev_y - 44, 22, ACCENT, FONT_B)
        for k in range(3):
            ly = rev_y - 90 - k * 38
            hline(c, rx + 24, ly, rx + rev_w - 24, FAINT, 0.5)

    # === 우: 7일 그리드 ===
    grid_top = top_y
    grid_bottom = rev_y - rev_h
    grid_h = grid_top - grid_bottom
    day_w = grid_w / 7

    for i in range(7):
        d = sunday + timedelta(days=i)
        x = grid_x + day_w * i
        is_h = is_holiday(d)
        if is_h:
            color_num = holiday_color(d)
        elif i == 0:
            color_num = SUN
        elif i == 6:
            color_num = SAT
        else:
            color_num = FG
        text(c, WEEKDAYS_KR[i], x + day_w / 2, grid_top - 38, 22,
             SUN if i == 0 else (SAT if i == 6 else DIM),
             FONT_B, 'center')
        text(c, f'{d.month}.{d.day}', x + day_w / 2, grid_top - 78, 28,
             color_num, FONT_B, 'center')
        if is_h:
            text(c, holiday_name(d), x + day_w / 2, grid_top - 104, 13,
                 holiday_color(d), FONT_L, 'center')
    hline(c, grid_x, grid_top - 120, grid_x + grid_w, FAINT, 1)
    for i in range(8):
        vline(c, grid_x + day_w * i, grid_top - 120, grid_bottom, GRID, 0.6)

    cell_top = grid_top - 138
    cell_bot = grid_bottom
    cell_h = cell_top - cell_bot
    todo_rows = 6
    row_h = cell_h / (todo_rows + 3)

    for i in range(7):
        x = grid_x + day_w * i
        for r in range(todo_rows):
            ly = cell_top - (r + 1) * row_h + 8
            text(c, '□', x + 18, ly, 16, DIM, FONT)
            hline(c, x + 50, ly - 8, x + day_w - 18, FAINT, 0.5)
        sep_y = cell_top - todo_rows * row_h - 14
        hline(c, x + 14, sep_y, x + day_w - 14, FAINT, 0.8)
        text(c, '주요 일정', x + 18, sep_y - 28, 12, DIM, FONT_L)
        for r in range(3):
            ly = sep_y - 56 - r * 30
            hline(c, x + 18, ly, x + day_w - 14, FAINT, 0.5)

    # 네비
    prev_sun = sunday - timedelta(days=7)
    next_sun = sunday + timedelta(days=7)
    prev_dest = bm_week(prev_sun) if prev_sun in ALL_WEEKS_SET else None
    next_dest = bm_week(next_sun) if next_sun in ALL_WEEKS_SET else None
    nav_bar(c, [('표지', bm_cover()),
                ('목차', bm_index()),
                (f'{mon_y} {mon_m}월', bm_month(mon_y, mon_m) if mon_y in YEARS else None),
                ('◀ 이전 주' if prev_dest else '', prev_dest),
                ('다음 주 ▶' if next_dest else '', next_dest)])
    c.showPage()


# ========== 주간 ==========
def page_week(c, sunday):
    fill_bg(c)
    c.bookmarkPage(bm_week(sunday))
    wy, wn = week_label(sunday)
    sat = sunday + timedelta(days=6)
    title = f'{wy} W{wn:02d}'
    sub = f'{sunday.month}.{sunday.day} – {sat.month}.{sat.day}'
    thu = thursday_of(sunday)
    mon_y, mon_m = thu.year, thu.month
    page_frame(c, title, sub)
    if mon_y in YEARS:
        link(c, bm_month(mon_y, mon_m), MX, PAGE_H - 110, 280, 38)

    if LANDSCAPE:
        _page_week_landscape(c, sunday, mon_y, mon_m)
        return

    # 상단: 우선순위 + 집중/메모  (큼지막한 쓰기 공간)
    top_y = PAGE_H - 210
    pri_h = 760
    pri_w = (PAGE_W - 2 * MX - 60) * 0.42
    focus_w = (PAGE_W - 2 * MX - 60) - pri_w

    # 우선순위 (A:3 / B:3 / C:3 = 9개, 큰 행 간격)
    box(c, MX, top_y - pri_h, pri_w, pri_h, stroke=FAINT, width=1, radius=14)
    text(c, '우선순위', MX + 32, top_y - 60, 32, ACCENT, FONT_B)
    text(c, 'A 반드시  ·  B 가능하면  ·  C 여유되면',
         MX + 230, top_y - 60, 18, DIM, FONT_L)

    rows = [('A', 3), ('B', 3), ('C', 3)]
    ry = top_y - 150
    for tier, count in rows:
        for i in range(1, count + 1):
            text(c, f'{tier}{i}', MX + 36, ry, 26, ACCENT if tier == 'A' else DIM, FONT_B)
            text(c, '□', MX + 110, ry, 28, DIM, FONT)
            hline(c, MX + 158, ry - 16, MX + pri_w - 36, FAINT, 0.7)
            ry -= 64
        ry -= 18

    # 이번 주 집중 + 메모
    fx = MX + pri_w + 60
    box(c, fx, top_y - pri_h, focus_w, pri_h, stroke=FAINT, width=1, radius=14)
    text(c, '이번 주 집중', fx + 32, top_y - 60, 32, ACCENT, FONT_B)
    for i in range(3):
        ly = top_y - 150 - i * 78
        text(c, '◆', fx + 36, ly, 26, HILITE, FONT)
        hline(c, fx + 88, ly - 16, fx + focus_w - 36, FAINT, 0.7)
    text(c, '메모', fx + 32, top_y - 410, 30, ACCENT, FONT_B)
    for i in range(4):
        ly = top_y - 480 - i * 64
        hline(c, fx + 36, ly, fx + focus_w - 36, FAINT, 0.7)

    # 하단 7일 그리드
    grid_top = top_y - pri_h - 70
    grid_bottom = MB + 290
    grid_h = grid_top - grid_bottom
    day_w = (PAGE_W - 2 * MX) / 7

    # 요일 헤더
    for i in range(7):
        d = sunday + timedelta(days=i)
        x = MX + day_w * i
        is_h = is_holiday(d)
        if is_h:
            color_num = holiday_color(d)
        elif i == 0:
            color_num = SUN
        elif i == 6:
            color_num = SAT
        else:
            color_num = FG
        text(c, WEEKDAYS_KR[i], x + day_w / 2, grid_top - 40, 24,
             SUN if i == 0 else (SAT if i == 6 else DIM),
             FONT_B, 'center')
        text(c, f'{d.month}.{d.day}', x + day_w / 2, grid_top - 84, 30,
             color_num, FONT_B, 'center')
        if is_h:
            text(c, holiday_name(d), x + day_w / 2, grid_top - 114, 14,
                 holiday_color(d), FONT_L, 'center')
    hline(c, MX, grid_top - 130, PAGE_W - MX, FAINT, 1)

    for i in range(8):
        vline(c, MX + day_w * i, grid_top - 130, grid_bottom, GRID, 0.6)

    cell_top = grid_top - 150
    cell_bot = grid_bottom
    cell_h = cell_top - cell_bot
    todo_rows = 5
    row_h = cell_h / (todo_rows + 3)

    for i in range(7):
        x = MX + day_w * i
        for r in range(todo_rows):
            ly = cell_top - (r + 1) * row_h + 10
            text(c, '□', x + 24, ly, 18, DIM, FONT)
            hline(c, x + 60, ly - 10, x + day_w - 24, FAINT, 0.5)
        sep_y = cell_top - todo_rows * row_h - 18
        hline(c, x + 20, sep_y, x + day_w - 20, FAINT, 0.8)
        text(c, '주요 일정', x + 24, sep_y - 34, 14, DIM, FONT_L)
        for r in range(3):
            ly = sep_y - 70 - r * 40
            hline(c, x + 24, ly, x + day_w - 20, FAINT, 0.5)

    # 주간 리뷰 (다음 주로 제거, 2개 칸으로 넓게)
    rev_y = grid_bottom - 30
    rev_h = 240
    rev_w = (PAGE_W - 2 * MX - 50) / 2
    for i, lbl in enumerate(['잘한 것', '개선할 것']):
        x = MX + i * (rev_w + 50)
        box(c, x, rev_y - rev_h, rev_w, rev_h, stroke=FAINT, width=1, radius=14)
        text(c, lbl, x + 32, rev_y - 56, 28, ACCENT, FONT_B)
        for k in range(3):
            ly = rev_y - 120 - k * 54
            hline(c, x + 32, ly, x + rev_w - 32, FAINT, 0.6)

    prev_sun = sunday - timedelta(days=7)
    next_sun = sunday + timedelta(days=7)
    prev_dest = bm_week(prev_sun) if prev_sun in ALL_WEEKS_SET else None
    next_dest = bm_week(next_sun) if next_sun in ALL_WEEKS_SET else None
    nav_bar(c, [('표지', bm_cover()),
                ('목차', bm_index()),
                (f'{mon_y} {mon_m}월', bm_month(mon_y, mon_m) if mon_y in YEARS else None),
                ('◀ 이전 주' if prev_dest else '', prev_dest),
                ('다음 주 ▶' if next_dest else '', next_dest)])
    c.showPage()


# ========== 프로젝트 인덱스 ==========
def page_projects_index(c):
    fill_bg(c)
    c.bookmarkPage(bm_projects())
    page_frame(c, '프로젝트', 'Projects', '목차  ›  프로젝트')
    link(c, bm_index(), MX, PAGE_H - 110, 240, 38)

    if LANDSCAPE:
        cols = 5
        rows = 2
    else:
        cols = 2
        rows = 5
    gap_x = 50
    gap_y = 40
    top_y = PAGE_H - 250
    bottom_y = MB + 130
    grid_h = top_y - bottom_y
    card_w = (PAGE_W - 2 * MX - gap_x) / cols
    card_h = (grid_h - gap_y * (rows - 1)) / rows

    for i in range(PROJECT_SLOTS):
        r = i // cols
        col = i % cols
        x = MX + col * (card_w + gap_x)
        y = top_y - (r + 1) * card_h - r * gap_y
        box(c, x, y, card_w, card_h, stroke=FAINT, width=1, radius=14)
        # 번호
        text(c, f'P{i + 1:02d}', x + 32, y + card_h - 70, 50, ACCENT, FONT_B)
        # 프로젝트명
        text(c, '프로젝트명', x + 200, y + card_h - 56, 18, DIM, FONT_L)
        hline(c, x + 200, y + card_h - 80, x + card_w - 32, FAINT, 0.8)
        # 기간 / 상태
        text(c, '기간', x + 32, y + card_h - 138, 18, DIM, FONT_L)
        hline(c, x + 32, y + card_h - 162, x + card_w / 2 - 24, FAINT, 0.6)
        text(c, '상태', x + card_w / 2 + 24, y + card_h - 138, 18, DIM, FONT_L)
        hline(c, x + card_w / 2 + 24, y + card_h - 162, x + card_w - 32, FAINT, 0.6)
        # 한 줄 요약
        text(c, '한 줄 요약', x + 32, y + card_h - 204, 18, DIM, FONT_L)
        hline(c, x + 32, y + card_h - 228, x + card_w - 32, FAINT, 0.6)
        # 진척
        bar_y = y + 56
        text(c, '진척', x + 32, bar_y - 4, 16, DIM, FONT_L)
        box(c, x + 92, bar_y, card_w - 132, 18, stroke=FAINT, width=0.8, radius=9)
        link(c, bm_project(i + 1), x, y, card_w, card_h)

    nav_bar(c, [('표지', bm_cover()),
                ('목차', bm_index()),
                ('P01', bm_project(1)),
                (f'P{PROJECT_SLOTS:02d}', bm_project(PROJECT_SLOTS)),
                ('회의록', bm_meetings())])
    c.showPage()


# ========== 프로젝트 상세 ==========
def page_project(c, i):
    fill_bg(c)
    c.bookmarkPage(bm_project(i))
    page_frame(c, f'P{i:02d}', '프로젝트 상세', f'프로젝트  ›  P{i:02d}')
    link(c, bm_projects(), MX, PAGE_H - 110, 280, 38)

    # 상단 헤더
    top_y = PAGE_H - 230
    header_h = 170 if LANDSCAPE else 210
    box(c, MX, top_y - header_h, PAGE_W - 2 * MX, header_h, stroke=FAINT, width=1, radius=14)

    text(c, '프로젝트명', MX + 28, top_y - 50, 18, DIM, FONT_L)
    hline(c, MX + 28, top_y - 80, MX + 1000, FAINT, 0.8)
    text(c, '기간', MX + 1040, top_y - 50, 18, DIM, FONT_L)
    hline(c, MX + 1040, top_y - 80, PAGE_W - MX - 28, FAINT, 0.8)
    text(c, '목표', MX + 28, top_y - 118, 18, DIM, FONT_L)
    hline(c, MX + 28, top_y - 148, PAGE_W - MX - 28, FAINT, 0.8)
    text(c, '오너', MX + 28, top_y - 184, 18, DIM, FONT_L)
    hline(c, MX + 90, top_y - 196, MX + 500, FAINT, 0.6)
    text(c, '상태', MX + 540, top_y - 184, 18, DIM, FONT_L)
    hline(c, MX + 600, top_y - 196, MX + 900, FAINT, 0.6)
    text(c, '우선순위', MX + 940, top_y - 184, 18, DIM, FONT_L)
    hline(c, MX + 1040, top_y - 196, PAGE_W - MX - 28, FAINT, 0.6)

    # 행 수/높이 - 가로 모드는 압축
    if LANDSCAPE:
        mil_h_v = 220
        mil_rows = 5
        mil_row_sp = 32
        mid_h_v = 380
        mid_rows = 7
        mid_row_sp = 42
        todo_rows = 6
    else:
        mil_h_v = 320
        mil_rows = 5
        mil_row_sp = 48
        mid_h_v = 600
        mid_rows = 10
        mid_row_sp = 50
        todo_rows = 8

    # 마일스톤
    mil_y = top_y - header_h - 50
    mil_h = mil_h_v
    text(c, '마일스톤', MX, mil_y, 28, ACCENT, FONT_B)
    box(c, MX, mil_y - mil_h - 12, PAGE_W - 2 * MX, mil_h, stroke=FAINT, width=1, radius=12)
    ths = ['#', '마일스톤', '목표일', '완료일', '비고']
    widths = [90, 720, 200, 200, (PAGE_W - 2 * MX) - 90 - 720 - 200 - 200]
    hx = MX
    hy = mil_y - 50
    for w, label in zip(widths, ths):
        text(c, label, hx + 16, hy, 18, DIM, FONT_L)
        hx += w
    hline(c, MX, hy - 16, PAGE_W - MX, FAINT, 0.8)
    for r in range(mil_rows):
        ry = hy - 56 - r * mil_row_sp
        text(c, f'M{r + 1}', MX + 16, ry, 20, DIM, FONT_B)
        hline(c, MX + 90, ry - 10, PAGE_W - MX - 16, FAINT, 0.5)

    # 좌: 주간 체크 / 우: 시간 로그
    mid_y = mil_y - mil_h - 80
    mid_h = mid_h_v
    col_w = (PAGE_W - 2 * MX - 50) / 2
    text(c, '주간 체크', MX, mid_y, 28, ACCENT, FONT_B)
    box(c, MX, mid_y - mid_h, col_w, mid_h, stroke=FAINT, width=1, radius=12)
    col_labels = ['주', '계획', '실행', '리뷰']
    sub_w = [80, (col_w - 80) / 3, (col_w - 80) / 3, (col_w - 80) / 3]
    sx = MX
    sy = mid_y - 44
    for w, label in zip(sub_w, col_labels):
        text(c, label, sx + 16, sy, 18, DIM, FONT_L)
        sx += w
    hline(c, MX, sy - 16, MX + col_w, FAINT, 0.8)
    for r in range(mid_rows):
        ry = sy - 50 - r * mid_row_sp
        text(c, f'W{r + 1}', MX + 22, ry, 18, DIM, FONT_B)
        cx = MX + 80
        for w in sub_w[1:]:
            vline(c, cx, ry - 18, ry + 28, FAINT, 0.4)
            cx += w
        hline(c, MX, ry - 18, MX + col_w, FAINT, 0.4)

    rx = MX + col_w + 50
    text(c, '소요시간 로그', rx, mid_y, 28, ACCENT, FONT_B)
    box(c, rx, mid_y - mid_h, col_w, mid_h, stroke=FAINT, width=1, radius=12)
    log_cols = ['날짜', '작업', '시간', '비고']
    lw = [130, (col_w - 130 - 120 - 140), 120, 140]
    lsx = rx
    lsy = mid_y - 44
    for w, label in zip(lw, log_cols):
        text(c, label, lsx + 16, lsy, 18, DIM, FONT_L)
        lsx += w
    hline(c, rx, lsy - 16, rx + col_w, FAINT, 0.8)
    for r in range(mid_rows):
        ry = lsy - 50 - r * mid_row_sp
        hline(c, rx, ry - 14, rx + col_w, FAINT, 0.4)
        cx = rx
        for w in lw[:-1]:
            cx += w
            vline(c, cx, ry - 18, ry + 28, FAINT, 0.4)

    # 할일 목록
    todo_y = mid_y - mid_h - 70
    todo_h = todo_y - MB - 150
    text(c, '할일 목록', MX, todo_y, 28, ACCENT, FONT_B)
    box(c, MX, todo_y - todo_h, PAGE_W - 2 * MX, todo_h, stroke=FAINT, width=1, radius=12)
    col_count = 2
    col_gap = 50
    tc_w = (PAGE_W - 2 * MX - 50 - col_gap) / col_count
    inner_h = todo_h - 90
    for col in range(col_count):
        for r in range(todo_rows):
            tx = MX + 30 + col * (tc_w + col_gap)
            ty = todo_y - 60 - r * inner_h / todo_rows
            text(c, '□', tx, ty, 20, DIM, FONT)
            hline(c, tx + 42, ty - 10, tx + tc_w, FAINT, 0.5)

    prev_dest = bm_project(i - 1) if i > 1 else None
    next_dest = bm_project(i + 1) if i < PROJECT_SLOTS else None
    nav_bar(c, [('목차', bm_index()),
                ('프로젝트 목록', bm_projects()),
                (f'◀ P{i - 1:02d}' if prev_dest else '', prev_dest),
                (f'P{i + 1:02d} ▶' if next_dest else '', next_dest),
                ('회의록', bm_meetings())])
    c.showPage()


# ========== 회의록 인덱스 ==========
def page_meetings_index(c):
    fill_bg(c)
    c.bookmarkPage(bm_meetings())
    page_frame(c, '회의록', 'Meeting Notes', '목차  ›  회의록')
    link(c, bm_index(), MX, PAGE_H - 110, 240, 38)

    if LANDSCAPE:
        cols = 6
        rows = 5
    else:
        cols = 5
        rows = 6
    gap = 26
    top_y = PAGE_H - 250
    bottom_y = MB + 140
    gh = top_y - bottom_y
    cw = (PAGE_W - 2 * MX - gap * (cols - 1)) / cols
    ch = (gh - gap * (rows - 1)) / rows

    for i in range(MEETING_SLOTS):
        r = i // cols
        col = i % cols
        x = MX + col * (cw + gap)
        y = top_y - (r + 1) * ch - r * gap
        box(c, x, y, cw, ch, stroke=FAINT, width=1, radius=12)
        text(c, f'M{i + 1:02d}', x + cw / 2, y + ch - 76, 40, ACCENT, FONT_B, 'center')
        text(c, '날짜', x + 22, y + ch - 138, 16, DIM, FONT_L)
        hline(c, x + 22, y + ch - 158, x + cw - 22, FAINT, 0.5)
        text(c, '제목', x + 22, y + ch - 196, 16, DIM, FONT_L)
        hline(c, x + 22, y + ch - 216, x + cw - 22, FAINT, 0.5)
        hline(c, x + 22, y + ch - 256, x + cw - 22, FAINT, 0.5)
        link(c, bm_meeting(i + 1), x, y, cw, ch)

    nav_bar(c, [('표지', bm_cover()),
                ('목차', bm_index()),
                ('M01', bm_meeting(1)),
                (f'M{MEETING_SLOTS:02d}', bm_meeting(MEETING_SLOTS)),
                ('프로젝트', bm_projects())])
    c.showPage()


# ========== 회의록 상세 ==========
def page_meeting(c, i):
    fill_bg(c)
    c.bookmarkPage(bm_meeting(i))
    page_frame(c, f'M{i:02d}', 'Meeting Note', f'회의록  ›  M{i:02d}')
    link(c, bm_meetings(), MX, PAGE_H - 110, 280, 38)

    top_y = PAGE_H - 230
    head_h = 220
    box(c, MX, top_y - head_h, PAGE_W - 2 * MX, head_h, stroke=FAINT, width=1, radius=14)
    text(c, '제목', MX + 28, top_y - 56, 18, DIM, FONT_L)
    hline(c, MX + 90, top_y - 70, PAGE_W - MX - 28, FAINT, 0.8)
    text(c, '날짜', MX + 28, top_y - 122, 18, DIM, FONT_L)
    hline(c, MX + 90, top_y - 134, MX + 500, FAINT, 0.6)
    text(c, '시간', MX + 540, top_y - 122, 18, DIM, FONT_L)
    hline(c, MX + 600, top_y - 134, MX + 900, FAINT, 0.6)
    text(c, '장소', MX + 940, top_y - 122, 18, DIM, FONT_L)
    hline(c, MX + 1000, top_y - 134, PAGE_W - MX - 28, FAINT, 0.6)
    text(c, '참석자', MX + 28, top_y - 184, 18, DIM, FONT_L)
    hline(c, MX + 110, top_y - 196, PAGE_W - MX - 28, FAINT, 0.6)

    # 가로 모드 압축
    if LANDSCAPE:
        ag_h_v = 220
        ag_rows = 4
        ag_row_sp = 42
        dis_h_v = 460
        dis_rows = 8
        dis_row_sp = 50
        dec_h_v = 280
        dec_rows = 4
        dec_row_sp = 50
    else:
        ag_h_v = 320
        ag_rows = 5
        ag_row_sp = 56
        dis_h_v = 700
        dis_rows = 11
        dis_row_sp = 60
        dec_h_v = 380
        dec_rows = 5
        dec_row_sp = 60

    # 안건
    ag_y = top_y - head_h - 50
    ag_h = ag_h_v
    text(c, '안건', MX, ag_y, 28, ACCENT, FONT_B)
    box(c, MX, ag_y - ag_h - 12, PAGE_W - 2 * MX, ag_h, stroke=FAINT, width=1, radius=12)
    for r in range(ag_rows):
        ly = ag_y - 60 - r * ag_row_sp
        text(c, f'{r + 1}.', MX + 28, ly, 20, DIM, FONT_B)
        hline(c, MX + 80, ly - 10, PAGE_W - MX - 28, FAINT, 0.5)

    # 논의 내용
    dis_y = ag_y - ag_h - 80
    dis_h = dis_h_v
    text(c, '논의 내용', MX, dis_y, 28, ACCENT, FONT_B)
    box(c, MX, dis_y - dis_h - 12, PAGE_W - 2 * MX, dis_h, stroke=FAINT, width=1, radius=12)
    for r in range(dis_rows):
        ly = dis_y - 54 - r * dis_row_sp
        hline(c, MX + 28, ly - 8, PAGE_W - MX - 28, FAINT, 0.4)

    # 결정 / 액션
    dec_y = dis_y - dis_h - 80
    dec_h = dec_h_v
    col_w = (PAGE_W - 2 * MX - 50) / 2
    text(c, '결정사항', MX, dec_y, 28, ACCENT, FONT_B)
    box(c, MX, dec_y - dec_h - 12, col_w, dec_h, stroke=FAINT, width=1, radius=12)
    for r in range(dec_rows):
        ly = dec_y - 60 - r * dec_row_sp
        text(c, '✓', MX + 28, ly, 20, HILITE, FONT_B)
        hline(c, MX + 70, ly - 10, MX + col_w - 28, FAINT, 0.5)

    ax = MX + col_w + 50
    text(c, '액션 아이템', ax, dec_y, 28, ACCENT, FONT_B)
    box(c, ax, dec_y - dec_h - 12, col_w, dec_h, stroke=FAINT, width=1, radius=12)
    text(c, '담당', ax + 28, dec_y - 56, 16, DIM, FONT_L)
    text(c, '내용', ax + 180, dec_y - 56, 16, DIM, FONT_L)
    text(c, '기한', ax + col_w - 170, dec_y - 56, 16, DIM, FONT_L)
    hline(c, ax, dec_y - 70, ax + col_w, FAINT, 0.8)
    for r in range(dec_rows):
        ly = dec_y - 110 - r * dec_row_sp
        hline(c, ax + 28, ly - 10, ax + col_w - 28, FAINT, 0.5)
        vline(c, ax + 170, ly - 20, ly + 32, FAINT, 0.4)
        vline(c, ax + col_w - 180, ly - 20, ly + 32, FAINT, 0.4)

    prev_dest = bm_meeting(i - 1) if i > 1 else None
    next_dest = bm_meeting(i + 1) if i < MEETING_SLOTS else None
    nav_bar(c, [('목차', bm_index()),
                ('회의록 목록', bm_meetings()),
                (f'◀ M{i - 1:02d}' if prev_dest else '', prev_dest),
                (f'M{i + 1:02d} ▶' if next_dest else '', next_dest),
                ('프로젝트', bm_projects())])
    c.showPage()


# ========== 조립 ==========
ALL_WEEKS = all_weeks()
ALL_WEEKS_SET = set(ALL_WEEKS)


def build():
    c = canvas.Canvas(OUTPUT, pagesize=(PAGE_W, PAGE_H))
    c.setTitle(f'Project Planner {YEARS[0]}' + (f'-{YEARS[-1]}' if len(YEARS) > 1 else ''))
    c.setAuthor('GoodNotes Planner Generator')

    # 1) 표지 / 목차
    page_cover(c)
    page_index(c)

    # 2) 연간 + 해당 연도 월간
    for y in YEARS:
        page_annual(c, y)
        for m in range(1, 13):
            page_month(c, y, m)

    # 3) 주간
    for sun in ALL_WEEKS:
        page_week(c, sun)

    # 4) 프로젝트
    page_projects_index(c)
    for i in range(1, PROJECT_SLOTS + 1):
        page_project(c, i)

    # 5) 회의록
    page_meetings_index(c)
    for i in range(1, MEETING_SLOTS + 1):
        page_meeting(c, i)

    c.save()


if __name__ == '__main__':
    build()
    print(f'생성 완료: {OUTPUT}')
    print(f'주 페이지 수: {len(ALL_WEEKS)}')

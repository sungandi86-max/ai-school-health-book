#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
『보건교사를 위한 AI 업무 자동화』 전체 조판 (Book Design v2, 출판사 QA 폴리시 적용판)
- design-v2/design_v2.py 에서 승인된 디자인 시스템(화이트+딥네이비+연블루, 소프트 카드, 4분할 페이지 리듬,
  v2.1 타이포그래피)을 book-source-final.md 전체(PART1~8·Chapter01~22·에필로그)에 일관되게 적용한다.
- 새 디자인을 만들지 않는다. 기존 build_pdf.py(v1 조판)는 참고하지 않는다.
- 원고/Chapter·PART 순서/실습 내용/QR/이미지는 절대 수정하지 않는다.
"""
import os, re
from reportlab.lib.pagesizes import A5
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, PageBreak, NextPageTemplate, Image as RLImage, Flowable
)
from reportlab.lib.styles import ParagraphStyle
from PIL import Image as PILImage

from parser import parse, classify_blockquote

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
FONTS = os.path.join(BASE, "fonts")
QR = os.path.join(BASE, "qr")
OUT = os.path.join(BASE, "book-v2-final.pdf")

pdfmetrics.registerFont(TTFont("NotoKR", os.path.join(FONTS, "NotoKR-Regular.ttf")))
pdfmetrics.registerFont(TTFont("NotoKR-Bold", os.path.join(FONTS, "NotoKR-Bold.ttf")))

# ---------------- design system (v2.1, design-v2/design_v2.py 승인본과 동일) ----------------
NAVY = colors.HexColor("#16233F")
NAVY_SOFT = colors.HexColor("#4A5A7A")
# Round 5 — Workflow 화살표 칩 전용, NAVY_SOFT를 흰색 쪽으로 25% 블렌드한 옅은 톤.
# 새 색상 체계 추가가 아니라 기존 NAVY_SOFT를 살짝 연하게 낮춘 파생색.
NAVY_SOFT_LIGHT = colors.HexColor("#77839B")
SKY = colors.HexColor("#EAF2FB")
SKY_LINE = colors.HexColor("#D3E4F5")
INK = colors.HexColor("#232323")
GRAY = colors.HexColor("#8A8F99")
WHITE = colors.white
GOLD_TEXT = colors.HexColor("#8A6D1D")  # 주의 라벨 전용 (색상 시스템 내 강조, 새 색 추가 아님: 텍스트만)

# 컴포넌트별 시각적 톤 분리를 위한 보조 포인트 색(기본 딥네이비+연블루 체계는 유지,
# CASE/주의/한마디만 아주 옅은 보조 포인트를 추가해 서로 다른 성격의 박스로 구분되게 함)
CASE_BG = colors.HexColor("#E7F0FA")      # 연블루보다 살짝 더 또렷한 톤(기록 카드 느낌)
CASE_LINE = colors.HexColor("#8FB3DC")    # CASE 왼쪽 세로선
WARN_BG = colors.HexColor("#FBF1EC")      # 아주 옅은 웜/코랄 포인트(경고색 과용 금지)
WARN_LINE = colors.HexColor("#E3B7A0")
WARN_TEXT = colors.HexColor("#9C5B3C")
NOTE_LINE = colors.HexColor("#C9AE6B")    # 쑤캥의 한마디 — 저자 서명처럼 보이는 손글씨톤 포인트
NOTE_BG = colors.HexColor("#FBF8EF")      # 쑤캥의 한마디 전용 아주 옅은 웜톤 배경(연블루와 확실히 구분)
FRAME_BG = colors.HexColor("#F5F6F8")      # 실제 프로젝트 화면 전용 — 사진을 마운트에 얹은 듯한 아주 옅은 회색 매트(브랜드 색상 아님, 중립 프레임 전용)
FRAME_LINE = colors.HexColor("#E5E8ED")    # 위 매트의 아주 연한 테두리

PAGE_W, PAGE_H = A5
MARGIN_X = 52
MARGIN_TOP = 50
MARGIN_BOTTOM = 44
CONTENT_W = PAGE_W - 2 * MARGIN_X

BOOK_TITLE = "『보건교사를 위한 AI 업무 자동화』"
BOOK_TITLE_PLAIN = "보건교사를 위한 AI 업무 자동화"
AUTHOR = "쑤캥"
TAGLINE = "반복되는 업무 하나를 구조로 바꾸는 프로젝트북"

ASSETS_DERIVED = os.path.join(BASE, "assets_derived")
OTTER = os.path.join(ASSETS_DERIVED, "otter_signature.png")  # assets/07_ai_workflow.png에서
# 잘라낸 기존 그림 그대로(새 캐릭터 생성 아님) — 쑤캥 브랜드 시그니처로 제한된 위치에만 사용

# PART 표지 보조 키워드 — 원고 제목은 그대로 두고, 표지에서만 보조적으로 병기한다
PART_KEYWORDS = {
    1: "발견하다", 2: "경계를 그리다", 3: "실패를 기록하다", 4: "구조를 만들다",
    5: "흐름을 연결하다", 6: "운영으로 확장하다", 7: "반복을 맡기다", 8: "시스템으로 남기다",
}

# Chapter 오프닝 3변형 — 같은 디자인 시스템 안에서 성격만 다르게
# A: 이야기형(감성 에세이 오프닝) / B: 구조·판단형(핵심 질문 중심) / C: AI·운영형(Workflow 스트립)
CHAPTER_STYLE = {}
for _n in (1, 2, 5, 6, 7):
    CHAPTER_STYLE[_n] = "A"
for _n in (3, 4, *range(8, 17)):
    CHAPTER_STYLE[_n] = "B"
for _n in range(17, 23):
    CHAPTER_STYLE[_n] = "C"

# ---------------- styles (design-v2 v2.1과 동일 수치) ----------------
S = {}
S["running"] = ParagraphStyle("running", fontName="NotoKR-Bold", fontSize=8.5, leading=11.5, textColor=GRAY)
S["h1"] = ParagraphStyle("h1", fontName="NotoKR-Bold", fontSize=20, leading=26, textColor=NAVY)
S["h2"] = ParagraphStyle("h2", fontName="NotoKR-Bold", fontSize=14, leading=19, textColor=NAVY, spaceBefore=10, spaceAfter=6)
S["lead"] = ParagraphStyle("lead", fontName="NotoKR", fontSize=9.4, leading=17.4, textColor=NAVY_SOFT)
S["body"] = ParagraphStyle("body", fontName="NotoKR", fontSize=9.6, leading=18.8, textColor=INK, spaceAfter=11.5)
S["story"] = ParagraphStyle("story", fontName="NotoKR", fontSize=10, leading=19, textColor=INK, spaceAfter=13,
                             leftIndent=11, rightIndent=11)
S["dialogue"] = ParagraphStyle("dialogue", parent=S["story"], leftIndent=22, textColor=NAVY, fontName="NotoKR-Bold")
# Final Book Polish — 본문 리듬: 행간(leading)은 그대로 두고 문단 간격(spaceAfter)만
# 다르게 써서 "중요한 문장 뒤 / 설명 전환 / 사례 전환"에서 숨을 쉬게 한다. 새 문장은
# 추가하지 않고, 같은 문장을 다른 간격으로 배치할 뿐이다.
S["story_pause"] = ParagraphStyle("story_pause", parent=S["story"], spaceAfter=24)
S["dialogue_pause"] = ParagraphStyle("dialogue_pause", parent=S["dialogue"], spaceAfter=24)
S["beat"] = ParagraphStyle("beat", fontName="NotoKR-Bold", fontSize=11.5, leading=18, textColor=NAVY, alignment=TA_CENTER, spaceBefore=10, spaceAfter=10)
S["cardlabel"] = ParagraphStyle("cardlabel", fontName="NotoKR-Bold", fontSize=9.2, leading=13, textColor=NAVY)
S["cardbody"] = ParagraphStyle("cardbody", fontName="NotoKR", fontSize=8.8, leading=14.5, textColor=INK)
# Final Book Polish — 이미지 -> 캡션 -> 본문 위계: 캡션은 본문(9.6~10pt, INK)보다
# 한 단계 더 조용해야 하므로, 브랜드 색(NAVY_SOFT)이 아니라 중립 GRAY로 낮췄다.
S["caption"] = ParagraphStyle("caption", fontName="NotoKR", fontSize=8.1, leading=13, textColor=GRAY, spaceBefore=6, spaceAfter=11, alignment=TA_CENTER)
S["takeaway"] = ParagraphStyle("takeaway", fontName="NotoKR-Bold", fontSize=11.8, leading=17.5, textColor=NAVY, alignment=TA_CENTER, spaceBefore=10)
S["step_title"] = ParagraphStyle("step_title", fontName="NotoKR-Bold", fontSize=10.1, leading=14, textColor=NAVY)
S["step_body"] = ParagraphStyle("step_body", fontName="NotoKR", fontSize=9.0, leading=14.5, textColor=INK)
S["prompt"] = ParagraphStyle("prompt", fontName="NotoKR", fontSize=8.8, leading=14.5, textColor=NAVY, leftIndent=4)
S["check"] = ParagraphStyle("check", fontName="NotoKR", fontSize=9.0, leading=14.5, textColor=INK)
S["badge"] = ParagraphStyle("badge", fontName="NotoKR-Bold", fontSize=9.7, leading=12.5, textColor=NAVY, alignment=TA_CENTER)
S["eyebrow"] = ParagraphStyle("eyebrow", fontName="NotoKR-Bold", fontSize=8, leading=11, textColor=GRAY)
S["table_head"] = ParagraphStyle("tablehead", fontName="NotoKR-Bold", fontSize=8.4, leading=12, textColor=WHITE)
S["table_cell"] = ParagraphStyle("tablecell", fontName="NotoKR", fontSize=8.4, leading=12.5, textColor=INK)
S["toc_part"] = ParagraphStyle("tocpart", fontName="NotoKR-Bold", fontSize=10.6, leading=16, textColor=NAVY, spaceBefore=9)
S["toc_chap"] = ParagraphStyle("tocchap", fontName="NotoKR", fontSize=9.2, leading=14, textColor=INK, leftIndent=12, spaceAfter=4)
S["cover_label"] = ParagraphStyle("coverlabel", fontName="NotoKR-Bold", fontSize=9, leading=12, textColor=GRAY)
S["subhead"] = ParagraphStyle("subhead", fontName="NotoKR-Bold", fontSize=12.6, leading=18, textColor=NAVY, spaceBefore=12, spaceAfter=6)


def tracked(text, gap_pt=6.5):
    """짧은 영문/숫자 라벨에 살짝 자간을 줘 Apple Books/Vercel류의 절제된
    편집 타이포 느낌을 낸다(한글 본문에는 쓰지 않음 — 가독성 기준 유지 대상 아님).
    참고: Noto Sans CJK KR에는 얇은 공백(U+2009 등) 글리프 자체가 없어
    유니코드 thin-space를 쓰면 조용히 사라져 자간이 전혀 적용되지 않는
    버그가 있었다. 대신 일반 스페이스를 작은 인라인 폰트 크기로 감싸
    시각적으로 좁은 간격을 만든다 — 모든 폰트에 항상 존재하는 글리프라 안전하다."""
    gap = f'<font size="{gap_pt}"> </font>'
    return gap.join(list(text))


def esc(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'`([^`]+)`', r'<font face="NotoKR">\1</font>', t)
    t = t.replace("  \n", "<br/>").replace("\\n", "<br/>")
    return t


def is_dialogue(text):
    return bool(re.match(r'^["“”]', text.strip())) or text.strip().startswith('"')


def running_header_flowable(left_text, right_text):
    left = Paragraph(esc(left_text), S["running"])
    right = Paragraph(esc(right_text), ParagraphStyle("runningR", parent=S["running"], alignment=TA_LEFT))
    t = Table([[left, right]], colWidths=[CONTENT_W * 0.62, CONTENT_W * 0.38])
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.6, SKY_LINE),
    ]))
    return t


def soft_card(rows_flowables, pad=11, bg=SKY, radius=10, box=False, box_color=SKY_LINE):
    """Final Book Polish (Round 4~5) — 카드가 'UI 컴포넌트'처럼 보이지 않도록
    모서리를 한 단계 덜 둥글게(radius 12->10) 하고, 배경색은 그대로 두되 아주
    연한 테두리 한 줄만 그린다. Round 5에서 기본 패딩을 12->11로 살짝 줄이고
    테두리를 0.4/0.5->0.3/0.35pt로 한 번 더 낮춰 종이 위 옅은 상자에 더
    가깝게 했다(그림자·입체효과·새 색상은 추가하지 않음 — 애초에 그림자 자체가
    없었으므로 이번에도 없음)."""
    data = [[rows_flowables]]
    t = Table(data, colWidths=[CONTENT_W])
    style = [
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROUNDEDCORNERS", [radius, radius, radius, radius]),
        ("BOX", (0, 0), (-1, -1), 0.35 if box else 0.3, box_color),
    ]
    t.setStyle(TableStyle(style))
    return t


def stamp(text, bold_prefix="완료 확인", with_otter=False):
    p = Paragraph(f"&#10003;&nbsp;&nbsp;{esc(bold_prefix)} — {esc(text)}",
                  ParagraphStyle("stamp", parent=S["cardlabel"], fontSize=9.4, textColor=NAVY))
    if with_otter and os.path.exists(OTTER):
        otter_cell = RLImage(OTTER, width=20, height=17)
        row = Table([[p, otter_cell]], colWidths=[CONTENT_W - 40, 40])
        row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (1, 0), (1, 0), "RIGHT")]))
        content_cell = row
    else:
        content_cell = p
    t = Table([[content_cell]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SKY),
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("ROUNDEDCORNERS", [7, 7, 7, 7]),
    ]))
    return t


# ---------------- blockquote body rendering ----------------
def body_lines(body):
    """빈 줄 제거"""
    return [l for l in body if l.strip()]


def render_lines(lines, label_style=S["cardlabel"], body_style=S["cardbody"], skip_first_if_label=True):
    out = []
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith("**") and s.endswith("**") and s.count("**") == 2:
            out.append(Paragraph(esc(s), label_style))
        else:
            out.append(Paragraph(esc(s), body_style))
    return out


def _workflow_step_chip():
    """Workflow 전용 화살표 칩 — 단순 '↓' 문자 대신 작은 원형 칩 안에 화살표를 넣어
    '흐름 카드'라는 성격이 CASE/핵심 메시지 등과 뚜렷이 구분되게 한다. (텍스트 내용
    변경 아님 — 원고의 ↓ 기호를 시각적으로만 강화)
    Final Polish: 화살표를 카드 전체 폭 기준 가운데가 아니라 번호 배지 칸(26pt)
    바로 아래로 옮겨, 번호-화살표-번호가 하나의 세로 축으로 이어지는 '경로'처럼
    보이게 한다 — 읽는 카드가 아니라 따라가는 다이어그램에 가깝게.
    Round 5: Workflow에서 가장 먼저 읽혀야 하는 것은 문장(번호가 붙은 단계
    설명)이지 화살표가 아니므로, 칩을 20pt->15pt(25% 축소)로 줄이고 배경색도
    NAVY_SOFT의 옅은 톤(NAVY_SOFT_LIGHT)으로 낮춰 화살표는 '흐름을 보조'하는
    역할로 물러나게 한다. Workflow의 구조(번호·단계·화살표 자체) 는 그대로."""
    chip = Table([[Paragraph("↓", ParagraphStyle("wfchip", fontName="NotoKR-Bold", fontSize=7.6,
                                                  textColor=WHITE, alignment=TA_CENTER))]],
                 colWidths=[15], rowHeights=[15])
    chip.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY_SOFT_LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROUNDEDCORNERS", [7, 7, 7, 7]),
    ]))
    # 번호 배지(26pt 칸)의 중심에 화살표 중심이 오도록 같은 26pt 칸에 배치하고
    # 본문 칸은 비워 둔다 — 번호 칼럼과 화살표 칼럼이 시각적으로 같은 세로선 위에 놓인다.
    avail_w = CONTENT_W - 2 * 16  # box_workflow의 soft_card pad=16 안에서 실제로 쓸 수 있는 폭
    row = Table([[chip, ""]], colWidths=[26, avail_w - 26])
    row.setStyle(TableStyle([
        ("ALIGN", (0, 0), (0, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return row


def _workflow_step_label(n, text, is_label):
    """단계 번호를 붙인 Workflow 단계 줄 — 화살표와 함께 '단계 관계'가 보이도록 한다."""
    if is_label:
        return Paragraph(esc(text), S["cardlabel"])
    num_style = ParagraphStyle("wfnum", fontName="NotoKR-Bold", fontSize=8.6, textColor=NAVY_SOFT, alignment=TA_CENTER)
    badge = Paragraph(f"{n:02d}", num_style)
    # Final Book Polish: 덜어내기 — 번호 배지가 이미 순서를 알려주므로 단계 설명
    # 문장까지 볼드로 만들 필요는 없다. 굵기를 빼고 색만 NAVY로 유지해 조용히
    # 구분되게 한다.
    body = Paragraph(esc(text), ParagraphStyle("wfstep", parent=S["cardbody"], textColor=NAVY))
    avail_w = CONTENT_W - 2 * 16  # box_workflow의 soft_card pad=16 안에서 실제로 쓸 수 있는 폭
    row = Table([[badge, body]], colWidths=[26, avail_w - 26])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return row


def workflow_arrow_lines(lines):
    """Workflow 전용 렌더링 — 단계마다 번호를 붙이고 ↓는 원형 칩으로 강화해
    '흐름이 먼저 보이는' 카드가 되게 한다. 원고 텍스트는 그대로 사용한다."""
    out = []
    step_n = 0
    for l in lines:
        s = l.strip()
        if not s:
            continue
        if s == "↓":
            out.append(_workflow_step_chip())
        elif s.startswith("**") and s.endswith("**") and s.count("**") == 2:
            out.append(Paragraph(esc(s), S["cardlabel"]))
        else:
            step_n += 1
            out.append(_workflow_step_label(step_n, s, is_label=False))
    return out


def box_progress_card(body):
    lines = body_lines(body)[1:]  # 첫줄 "**프로젝트 진행 카드**" 라벨은 제외
    fields = {}
    order = []
    for l in lines:
        m = re.match(r'^\*\*(.+?)\*\*\s*(.*)$', l.strip())
        if m:
            k, v = m.group(1), m.group(2)
            fields[k] = v
            order.append(k)
    day_chapter = fields.get("DAY", "") or next((fields[k] for k in order if k.startswith("DAY")), "")
    make = fields.get("오늘 만드는 것", "")
    time_ = fields.get("걸리는 시간", "")
    diff = fields.get("난이도", "")
    part_prog = fields.get("PART 진행", "")
    day_key = next((k for k in order if k.startswith("DAY")), None)
    day_val = fields.get(day_key, "") if day_key else ""

    rows = [Paragraph("오늘 만드는 것", S["cardlabel"]), Spacer(1, 3),
            Paragraph(esc(make) if make else "", ParagraphStyle("bigmake", fontName="NotoKR-Bold", fontSize=12, textColor=NAVY))]
    stat = Table([[
        Paragraph(esc(day_key + " " + day_val) if day_key else "", ParagraphStyle("st1", fontName="NotoKR-Bold", fontSize=9.6, textColor=NAVY)),
        Paragraph(f"걸리는 시간<br/><b>{esc(time_)}</b>", ParagraphStyle("st2", fontName="NotoKR", fontSize=8.6, textColor=NAVY_SOFT, leading=12.2)),
        Paragraph(f"난이도<br/><b>{esc(diff)}</b>", ParagraphStyle("st3", fontName="NotoKR", fontSize=8.6, textColor=NAVY_SOFT, leading=12.2)),
    ]], colWidths=[CONTENT_W * 0.30, CONTENT_W * 0.35, CONTENT_W * 0.35])
    stat.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                               ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    rows += [Spacer(1, 10), stat]
    card = soft_card(rows, pad=15)
    extra = []
    if part_prog:
        extra.append(Paragraph(esc(part_prog), ParagraphStyle("pprog", fontName="NotoKR", fontSize=8.3, textColor=GRAY, alignment=TA_CENTER, spaceBefore=6)))
    return [card] + extra


def box_case(body):
    """CASE — 실제 사례라는 성격이 드러나도록 번호형 기록 카드로 렌더링.
    (텍스트 내용은 그대로, 굵은 라벨 줄에만 순번을 붙이고 왼쪽 세로선 + 살짝 더
    또렷한 배경으로 Workflow/핵심 메시지 카드와 확실히 구분되게 한다.)"""
    lines = body_lines(body)
    out = []
    n = 0
    first_label_seen = False
    for l in lines:
        s = l.strip()
        if s.startswith("**") and s.endswith("**") and s.count("**") == 2:
            label = s.strip("*")
            if not first_label_seen:
                # 첫 굵은 줄은 "CASE · 제목" 자체(카드 라벨) — 사례 항목이 아니므로 번호를 매기지 않는다
                first_label_seen = True
                out.append(Paragraph(esc(label), S["cardlabel"]))
            else:
                n += 1
                out.append(Paragraph(f'<font color="#8FB3DC"><b>{n:02d}</b></font>&nbsp;&nbsp;<b>{esc(label)}</b>', S["cardlabel"]))
        else:
            out.append(Paragraph(esc(s), S["cardbody"]))
    card = soft_card(out, pad=12, bg=CASE_BG)
    wrap = Table([[card]], colWidths=[CONTENT_W])
    wrap.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LINEBEFORE", (0, 0), (0, 0), 2.5, CASE_LINE),  # Final Book Polish: 덜어내기 — 3->2.5pt
    ]))
    return [wrap]


def box_workflow(body):
    """Workflow 카드 — 흐름이 먼저 보이도록 다른 카드보다 내부 여백을 넓히고
    (다이어그램 느낌), 왼쪽에 얇은 NAVY_SOFT 세로선을 둬 CASE(파란 계열 세로선)와도
    구분되는 '전용 스타일'로 통일한다."""
    lines = body_lines(body)
    card = soft_card(workflow_arrow_lines(lines), pad=16)
    wrap = Table([[card]], colWidths=[CONTENT_W])
    wrap.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LINEBEFORE", (0, 0), (0, 0), 2.5, NAVY),  # Final Book Polish: 덜어내기 — 3->2.5pt
    ]))
    return [wrap]


def box_caution(body):
    """주의 — 경고색을 과하게 쓰지 않는 선에서, 연블루 카드와 즉시 구분되도록
    아주 옅은 웜/코랄 톤만 사용한다(새 색상 체계 추가가 아니라 보조 포인트)."""
    lines = body_lines(body)
    label_style = ParagraphStyle("warnlabel", parent=S["cardlabel"], textColor=WARN_TEXT)
    return [soft_card(render_lines(lines, label_style=label_style), pad=12, bg=WARN_BG, radius=10, box=True, box_color=WARN_LINE)]


def box_core_message(body):
    """핵심 메시지 — 문장 하나가 중심이 되도록 카드 높이를 줄이고(패딩 축소),
    굵은 문장은 한 단계 더 크게 키워 시선이 바로 꽂히게 한다."""
    lines = body_lines(body)
    out = [Paragraph(esc(lines[0]), S["eyebrow"]), Spacer(1, 3)]
    big_style = ParagraphStyle("coremsgbig", fontName="NotoKR-Bold", fontSize=11.2, leading=16.5, textColor=NAVY)
    for l in lines[1:]:
        s = l.strip()
        style = big_style if s.startswith("**") and s.endswith("**") else S["cardbody"]
        out.append(Paragraph(esc(s), style))
    return [soft_card(out, pad=11)]


def box_celebration(body):
    """작은 축하 — 쑤캥 브랜드 시그니처(수달)를 제한적으로 함께 배치한다."""
    lines = body_lines(body)
    text = " ".join(l.strip("* ") for l in lines[1:]) if len(lines) > 1 else lines[0].strip("* ")
    return [stamp(text, bold_prefix="작은 축하", with_otter=True)]


def box_today_made(body):
    """오늘 만든 프로젝트 — 카드 벽을 줄이기 위해 채워진 배경 대신 얇은 상단 선 +
    라벨 + 체크 리스트만 남긴다(QR·완료 표시와 나란히 있어도 카드가 반복되지
    않도록 다음 Chapter Preview와 같은 '가벼운' 톤으로 통일)."""
    lines = body_lines(body)[1:]
    rule = Table([[""]], colWidths=[CONTENT_W], rowHeights=[1])
    rule.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), SKY_LINE)]))
    out = [rule, Spacer(1, 8), Paragraph("오늘 만든 프로젝트", S["eyebrow"]), Spacer(1, 5)]
    for l in lines:
        s = l.strip()
        if s.startswith("✓"):
            out.append(Paragraph(esc(s), ParagraphStyle("tmbody", parent=S["cardbody"], textColor=INK)))
        else:
            out.append(Paragraph(f"<b>{esc(s)}</b>", ParagraphStyle("tm", parent=S["cardlabel"], textColor=NAVY)))
    return out


def box_done_marker(body):
    """완료 · DAY N — 카드로 감싸지 않고 얇은 라벨 + 짧은 문장으로만 표시해
    QR/오늘 만든 프로젝트와 나란히 있어도 '카드 벽'이 되지 않게 한다."""
    lines = body_lines(body)
    label = lines[0].strip("* ")
    rest = lines[1:]
    out = [Paragraph(f'<font color="#4A5A7A">✓</font>&nbsp;&nbsp;{esc(label)}',
                      ParagraphStyle("donelabel", fontName="NotoKR-Bold", fontSize=8.6, textColor=NAVY_SOFT))]
    if rest:
        out.append(Spacer(1, 3))
        out += [Paragraph(esc(l), ParagraphStyle("donebody", parent=S["cardbody"], fontName="NotoKR-Bold", textColor=NAVY)) for l in rest]
    return out


def box_author_note(body):
    """쑤캥의 한마디 — "저자가 직접 말을 거는 공간"이라는 인상을 주기 위해
    (1) 다른 카드와 다른 아주 옅은 웜톤 배경, (2) 영문 트래킹 eyebrow +
    큰 장식 인용부호로 대화체를 강조, (3) 수달 시그니처를 오른쪽 위 서명
    자리에 배치한다. 수달은 책 전체에서 제한적으로만 사용(과용 금지)."""
    lines = body_lines(body)[1:]
    eyebrow = Paragraph(tracked("AUTHOR'S NOTE"), ParagraphStyle(
        "authoreyebrow", fontName="NotoKR-Bold", fontSize=7.4, textColor=NOTE_LINE))
    label = Paragraph("쑤캥의 한마디", ParagraphStyle("authorlabel", parent=S["cardlabel"], fontSize=10.4))
    if os.path.exists(OTTER):
        otter_cell = RLImage(OTTER, width=30, height=25)
        head = Table([[[eyebrow, Spacer(1, 2), label], otter_cell]],
                     colWidths=[CONTENT_W - 2 * 12 - 36, 36])
        head.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        out = [head, Spacer(1, 8)]
    else:
        out = [eyebrow, Spacer(1, 2), label, Spacer(1, 6)]
    quote_mark = Paragraph('&ldquo;', ParagraphStyle("authorquote", fontName="NotoKR-Bold",
                                                      fontSize=26, leading=18, textColor=NOTE_LINE))
    out.append(quote_mark)
    out += [Paragraph(esc(l), ParagraphStyle("author", parent=S["cardbody"], fontSize=9.2, leading=15.6)) for l in lines]
    card = soft_card(out, pad=13, bg=NOTE_BG)
    wrap = Table([[card]], colWidths=[CONTENT_W])
    wrap.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LINEBEFORE", (0, 0), (0, 0), 2.5, NOTE_LINE),  # Final Book Polish: 덜어내기 — 3->2.5pt
    ]))
    return [wrap]


def box_preview(body):
    """다음 Chapter/PART Preview — Round 5: 남아 있던 '디자인 요소' 느낌을 한
    번 더 덜어낸다. 전체 폭 굵은 선 대신 짧은 선(40pt)만 남기고, 라벨은 더
    작고 볼드를 빼 속삭이듯 표시하며, 본문 문장은 카드 전용 색(NAVY_SOFT) 대신
    일반 본문과 같은 색(INK)·스타일(S["story"])로 렌더링해 "다음 이야기를
    살짝 들려주는 문장"처럼 본문에 자연스럽게 이어지게 한다."""
    lines = body_lines(body)
    label = lines[0].strip("* ")
    rule = Table([[""]], colWidths=[40], rowHeights=[0.75])
    rule.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), SKY_LINE)]))
    out = [rule, Spacer(1, 7),
           Paragraph(esc(label), ParagraphStyle("previewlabel", fontName="NotoKR", fontSize=7.6, textColor=GRAY)),
           Spacer(1, 4)]
    out += [Paragraph(esc(l), ParagraphStyle("previewbody", parent=S["story"], leftIndent=0, rightIndent=0)) for l in lines[1:]]
    return out


def box_qr(body, qr_path):
    lines = body_lines(body)
    title = lines[0].strip("* ")
    desc, info = [], []
    in_info = False
    for l in lines[1:]:
        s = l.strip()
        if s.startswith("**안내**"):
            in_info = True
            continue
        (info if in_info else desc).append(s)
    left = [Paragraph(esc(title), S["cardlabel"]), Spacer(1, 3)]
    left += [Paragraph(esc(d), S["cardbody"]) for d in desc]
    if info:
        left.append(Spacer(1, 4))
        left.append(Paragraph("<b>안내</b>", S["cardbody"]))
        left += [Paragraph(esc(d), S["cardbody"]) for d in info]
    qr_img = RLImage(qr_path, width=62, height=62)
    t = Table([[left, qr_img]], colWidths=[CONTENT_W - 86, 86])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("BOX", (0, 0), (-1, -1), 0.5, SKY_LINE),
        ("ROUNDEDCORNERS", [8, 8, 8, 8]),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return [t]


def box_prompt(body):
    lines = body_lines(body)
    out = [Paragraph(tracked("PROMPT"), ParagraphStyle("promptlabel", fontName="NotoKR-Bold", fontSize=8.2, textColor=NAVY_SOFT)),
           Spacer(1, 4)]
    out += [Paragraph(esc(l), S["prompt"]) for l in lines]
    return [soft_card(out, pad=11, bg=WHITE, radius=8, box=True)]


def box_generic(body):
    lines = body_lines(body)
    return [soft_card(render_lines(lines), pad=12, bg=colors.HexColor("#F5F7FA"))]


def box_checklist(items):
    out = [Paragraph("체크리스트", S["cardlabel"]), Spacer(1, 4)]
    for it in items:
        txt = it.lstrip("-").strip()
        out.append(Paragraph(f"{esc(txt)}", S["check"]))
    return [soft_card(out, pad=11)]


# ---------------- tables ----------------
def parse_table_rows(rows):
    cells = []
    for r in rows:
        parts = [p.strip() for p in r.strip("|").split("|")]
        cells.append(parts)
    return cells


def is_before_after(cells):
    header = [c.strip() for c in cells[0]]
    return len(header) == 3 and "Before" in header[0] and "After" in header[-1]


def table_before_after(cells):
    """오늘 바뀐 것 — Before는 작고 흐리게, After는 크고 굵은 딥네이비로 세로
    배치해 대비를 극대화한다(한눈에 변화가 느껴지도록). 카드 자체 색상 체계는
    그대로 두고 대비는 글자 크기·굵기·색 차이로만 만든다."""
    body_rows = [r for i, r in enumerate(cells) if i >= 2]
    avail_w = CONTENT_W - 2 * 13 - 4  # soft_card pad(13*2) + 안전 여유
    before_style = ParagraphStyle("baBefore", fontName="NotoKR", fontSize=8.4, leading=12.5, textColor=GRAY)
    after_style = ParagraphStyle("baAfter", fontName="NotoKR-Bold", fontSize=12.4, leading=17.5, textColor=NAVY)
    out = []
    for r in body_rows:
        if len(r) < 3 or not (r[0].strip() or r[2].strip()):
            continue
        before, after = r[0], r[2]
        before_p = Paragraph(f'{tracked("BEFORE")}&nbsp;&nbsp;{esc(before)}', ParagraphStyle(
            "baBeforeLine", parent=before_style))
        arrow_p = Paragraph('↓', ParagraphStyle("baArrowV", fontName="NotoKR-Bold", fontSize=11,
                                                 textColor=SKY_LINE, alignment=TA_LEFT, spaceBefore=2, spaceAfter=2))
        after_p = Paragraph(esc(after), after_style)
        after_box = Table([[after_p]], colWidths=[avail_w])
        after_box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), WHITE),
            ("BOX", (0, 0), (-1, -1), 0.4, SKY_LINE),
            ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("ROUNDEDCORNERS", [7, 7, 7, 7]),
        ]))
        out += [before_p, arrow_p, after_box, Spacer(1, 6)]
    # 원고 자체에 "#### 오늘 바뀐 것" 제목이 이미 별도로 렌더링되므로,
    # 카드 안에서 같은 라벨을 다시 넣으면 중복 표현이 된다(정리 대상).
    # 카드는 내용만 담고, 제목 역할은 원고 헤딩에게 맡긴다.
    return [soft_card(out[:-1] if out and isinstance(out[-1], Spacer) else out, pad=12)]


def is_blank_form(cells):
    """헤더만 있고 본문 칸이 모두 비어 있는 표 — 독자가 직접 채우는 '실습 입력표'.
    표 내용(헤더 문구)은 원고 그대로, 렌더링 스타일만 워크북처럼 다르게 한다."""
    body_rows = [r for i, r in enumerate(cells) if i >= 2]
    if not body_rows:
        return False
    return all(all(not c.strip() for c in r) for r in body_rows)


def table_generic(cells):
    header = cells[0]
    body_rows = [r for i, r in enumerate(cells) if i >= 2]
    ncols = len(header)
    is_form = is_blank_form(cells)
    data = [[Paragraph(esc(h), S["table_head"]) for h in header]]
    row_count = max(len(body_rows), 1)
    for r in body_rows:
        r = (r + [""] * ncols)[:ncols]
        data.append([Paragraph(esc(c), S["table_cell"]) for c in r])
    colw = CONTENT_W / ncols
    row_heights = None
    if is_form:
        # Round 5: Workbook 느낌 강화 — 실제 실습장처럼 "쓰는 줄"이 우선 보이게
        # 한다. 칸 높이를 조금 더 키우고(30→34) 안쪽 여백을 넉넉히 주어 손으로
        # 적을 자리처럼 보이게 하되, 세로 칸 구분선은 더 옅게 줄여 Canva식
        # 촘촘한 표 느낌을 덜어내고, 실제로 "쓰는 줄"인 가로선만 살짝 또렷하게
        # 남긴다. 새 색·아이콘·장식은 추가하지 않는다.
        row_heights = [None] + [34] * row_count
    t = Table(data, colWidths=[colw] * ncols, rowHeights=row_heights, repeatRows=1)
    if is_form:
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F7FAFD")),
            ("LINEBELOW", (0, 0), (-1, -2), 0.9, SKY_LINE),
            ("BOX", (0, 1), (-1, -1), 0.75, SKY_LINE),
            ("INNERGRID", (0, 1), (-1, -1), 0.4, SKY_LINE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        return [t, Spacer(1, 4),
                Paragraph(tracked("WRITE HERE") + "  ·  직접 적어보세요",
                          ParagraphStyle("formcue", fontName="NotoKR", fontSize=7.6, textColor=GRAY)),
                Spacer(1, 8)]
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.5, SKY_LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, colors.HexColor("#F7FAFD")]),
    ]))
    return [t, Spacer(1, 8)]


def render_table(rows):
    cells = parse_table_rows(rows)
    if is_before_after(cells):
        return table_before_after(cells)
    return table_generic(cells)


# ---------------- image block (프로젝트 화면: 이미지가 페이지의 주인공) ----------------
def render_image_block(block):
    """실제 프로젝트 화면 — 이미지가 페이지의 주인공이 되도록 캡션 위에 옅은
    '실제 화면' eyebrow로 위계를 분명히 하고, 캡션-이미지 간격을 좁혀 하나의
    장면처럼 붙어 보이게 한다.
    Final Polish: 이미지 자체·캡션 문장은 그대로 두고, 화면을 사진 마운트에
    얹은 듯한 아주 옅은 회색 매트 + 아주 연한 테두리로 감싸 '스크린샷을 그냥
    붙여넣은 느낌'이 아니라 '지면에 신중하게 배치한 실제 화면'처럼 보이게 한다.
    매트의 아래·오른쪽 여백을 위·왼쪽보다 살짝 더 주어 아주 얇은 그림자처럼
    읽히게 하되, 새 장식이나 브랜드 색은 추가하지 않는다(중립 회색 한 톤)."""
    fname = os.path.basename(block["src"])
    path = os.path.join(ASSETS, fname)
    flows = [Paragraph("실제 화면", S["eyebrow"]), Spacer(1, 6)]
    if os.path.exists(path):
        with PILImage.open(path) as im:
            iw, ih = im.size
        disp_w = CONTENT_W * 0.96
        disp_h = ih * (disp_w / iw)
        max_h = 405
        if disp_h > max_h:
            disp_h = max_h
            disp_w = iw * (max_h / ih)
        img = RLImage(path, width=disp_w, height=disp_h)
        # Round 5 ⑦: 이 페이지는 이미 가장 완성도가 높다고 판단되어 새로 꾸미지
        # 않는다. 다만 다른 카드들의 테두리를 이번 라운드에서 전반적으로 더
        # 연하게 줄인 것과 톤을 맞추기 위해, 매트 테두리만 아주 살짝 더
        # 얇게 낮춘다(불필요하게 이미지보다 튀는 강조를 덜어냄).
        mat = Table([[img]], colWidths=[disp_w + 8])
        mat.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), FRAME_BG),
            ("BOX", (0, 0), (-1, -1), 0.6, FRAME_LINE),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 3), ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ]))
        wrap = Table([[mat]], colWidths=[CONTENT_W])
        wrap.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        flows.append(wrap)
    cap = block.get("caption", "")
    if cap:
        # 내부 표기(IMG-00N ·) 제거, 독자용 문장만 남긴다
        cap_clean = re.sub(r'^IMG-\d+\s*[·\-]\s*', '', cap).strip()
        flows.append(Paragraph(esc(cap_clean), ParagraphStyle("imgcap", parent=S["caption"], spaceBefore=7)))
    return flows


# ---------------- covers (화이트 기반, 여백 중심 — v2 승인 디자인 언어 확장) ----------------
def cover_book():
    story = [Spacer(1, 130)]
    story.append(Paragraph(BOOK_TITLE_PLAIN.replace(" ", "<br/>", 0), S["cover_label"]))
    story.append(Spacer(1, 8))
    title_style = ParagraphStyle("bookTitle", fontName="NotoKR-Bold", fontSize=26, leading=33, textColor=NAVY)
    story.append(Paragraph("보건교사를 위한<br/>AI 업무 자동화", title_style))
    story.append(Spacer(1, 14))
    story.append(Paragraph(TAGLINE, S["lead"]))
    story.append(Spacer(1, 200))
    story.append(Paragraph(AUTHOR, ParagraphStyle("authorc", fontName="NotoKR-Bold", fontSize=12, textColor=NAVY)))
    return story


def cover_part(num, title, chapters):
    """PART 표지 — 새 막이 열리는 느낌을 위해 PART 번호를 페이지의 지배적인
    그래픽 요소로 키우고(캡션이 아니라 디자인 요소), 키워드는 짧게 트래킹된
    라벨로 보조 역할만 하게 한다. 제목·색상 체계·프레임 여백 구조는 그대로다."""
    # Round 5: 우선순위를 제목 -> PART 번호 -> 키워드 순으로 다시 정리한다.
    # 번호는 크기(132pt)는 유지하되 색을 한 단계 더 옅은 SKY(카드 배경에도 쓰는
    # 기존 색)로 낮춰 "배경 그래픽"처럼 물러나게 하고, 키워드는 크기를 줄여
    # 제목과 경쟁하지 않는 보조 라벨로 만든다. 제목(S["h1"]) 자체는 손대지 않는다.
    keyword = PART_KEYWORDS.get(num, "")
    big_num_style = ParagraphStyle("bigpartnum", fontName="NotoKR-Bold", fontSize=132, leading=118, textColor=SKY)
    story = [Spacer(1, 34)]
    story.append(Paragraph(f"{num:02d}", big_num_style))
    rule = Table([[""]], colWidths=[36], rowHeights=[3])
    rule.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY)]))
    story.append(Spacer(1, 4))
    story.append(rule)
    story.append(Spacer(1, 10))
    story.append(Paragraph(tracked(f"PART {num:02d}"), ParagraphStyle(
        "partno", fontName="NotoKR-Bold", fontSize=9.4, leading=12, textColor=NAVY_SOFT)))
    if keyword:
        story.append(Spacer(1, 3))
        story.append(Paragraph(esc(keyword), ParagraphStyle("partkeyword", fontName="NotoKR-Bold", fontSize=11, textColor=NAVY_SOFT)))
    story.append(Spacer(1, 18))
    story.append(Paragraph(esc(title), S["h1"]))
    story.append(Spacer(1, 16))
    ch_range = f"Chapter {chapters[0]:02d}–{chapters[-1]:02d}" if len(chapters) > 1 else f"Chapter {chapters[0]:02d}"
    story.append(Paragraph(ch_range, ParagraphStyle("partrange", fontName="NotoKR", fontSize=9.6, textColor=NAVY_SOFT)))
    story.append(Spacer(1, 120))
    if os.path.exists(OTTER):
        story.append(RLImage(OTTER, width=38, height=32, hAlign="CENTER"))
        story.append(Spacer(1, 6))
    story.append(Paragraph(TAGLINE, ParagraphStyle("parttag", fontName="NotoKR", fontSize=8.6, textColor=GRAY, alignment=TA_CENTER)))
    return story


def _chip_row(labels):
    """C형(AI·운영형) 오프닝의 작은 구조 스트립 — 사람/AI/데이터/시스템 같은
    책 전체에서 이미 반복적으로 쓰이는 일반 개념어만 배치(원고 내용 추가 아님)."""
    chip_style = ParagraphStyle("chip", fontName="NotoKR-Bold", fontSize=8.2, textColor=NAVY, alignment=TA_CENTER)
    cells = []
    for i, lab in enumerate(labels):
        cells.append(Paragraph(esc(lab), chip_style))
    row = [cells[0]]
    for c in cells[1:]:
        row.append(Paragraph("→", ParagraphStyle("chiparrow", fontName="NotoKR", fontSize=8.2, textColor=NAVY_SOFT, alignment=TA_CENTER)))
        row.append(c)
    n = len(row)
    w = CONTENT_W / n
    t = Table([row], colWidths=[w] * n)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SKY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [8, 8, 8, 8]),
    ]))
    return t


def cover_chapter(num, title):
    """Chapter 오프닝 3변형(A 이야기형 / B 구조·판단형 / C AI·운영형).
    큰 제목·진행 카드(별도 블록)는 그대로 유지하고, 성격에 따라 상단 여백·장식
    요소·하단 여백만 다르게 해 22개 Chapter가 전부 같은 템플릿으로 보이지 않게 한다."""
    style = CHAPTER_STYLE.get(num, "B")
    running_label = f"PART {BUILD_STATE['part_num']} · CHAPTER {num:02d}"

    if style == "A":
        # 이야기형: 여백을 충분히 주되, 제목 위 얇은 선 하나로 "에세이 오프닝" 느낌.
        # Final Polish: 제목 뒤 여백을 하나의 거대한 빈 칸(90pt)으로 두지 않고
        # 절반 가까이로 줄여, 제목 → 태그라인 → 진행 카드로 시선이 자연스럽게
        # 이어지는 리듬을 만든다(장식 추가 없이 간격만 조정).
        story = [Spacer(1, 86)]
        rule = Table([[""]], colWidths=[28], rowHeights=[2])
        rule.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), SKY_LINE)]))
        story.append(rule)
        story.append(Spacer(1, 14))
        story.append(Paragraph(running_label, S["running"]))
        story.append(Spacer(1, 10))
        story.append(Paragraph(esc(title), S["h1"]))
        story.append(Spacer(1, 54))
        story.append(Paragraph(BOOK_TITLE_PLAIN, ParagraphStyle("chaptagA", fontName="NotoKR", fontSize=8.3, textColor=GRAY, alignment=TA_CENTER)))
    elif style == "C":
        # AI·운영형: 제목 아래 작은 Workflow 스트립(구조 강조)
        story = [Spacer(1, 56)]
        story.append(Paragraph(running_label, S["running"]))
        story.append(Spacer(1, 10))
        story.append(Paragraph(esc(title), S["h1"]))
        story.append(Spacer(1, 22))
        story.append(_chip_row(["사람", "AI", "데이터", "시스템"]))
        story.append(Spacer(1, 38))
        story.append(Paragraph(BOOK_TITLE_PLAIN, ParagraphStyle("chaptagC", fontName="NotoKR", fontSize=8.3, textColor=GRAY, alignment=TA_CENTER)))
    else:
        # B, 구조·판단형: 제목 왼쪽에 작은 정사각 포인트 + 좁은 여백(핵심 질문을 정리하듯 담백하게)
        mark = Table([[""]], colWidths=[9], rowHeights=[9])
        mark.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY), ("ROUNDEDCORNERS", [2, 2, 2, 2])]))
        story = [Spacer(1, 62)]
        story.append(mark)
        story.append(Spacer(1, 8))
        story.append(Paragraph(running_label, S["running"]))
        story.append(Spacer(1, 10))
        story.append(Paragraph(esc(title), S["h1"]))
        story.append(Spacer(1, 42))
        story.append(Paragraph(BOOK_TITLE_PLAIN, ParagraphStyle("chaptagB", fontName="NotoKR", fontSize=8.3, textColor=GRAY, alignment=TA_CENTER)))
    return story


def cover_epilogue():
    story = [Spacer(1, 110)]
    story.append(Paragraph(tracked("EPILOGUE"), S["running"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("에필로그", S["h1"]))
    story.append(Spacer(1, 160))
    if os.path.exists(OTTER):
        story.append(RLImage(OTTER, width=44, height=38, hAlign="CENTER"))
        story.append(Spacer(1, 8))
    story.append(Paragraph(BOOK_TITLE_PLAIN, ParagraphStyle("epitag", fontName="NotoKR", fontSize=8.3, textColor=GRAY, alignment=TA_CENTER)))
    return story


# ---------------- TOC ----------------
def build_toc(blocks):
    story = [Spacer(1, 20)]
    story.append(Paragraph("차례", S["h1"]))
    story.append(Spacer(1, 14))
    cur_part_title = None
    for b in blocks:
        if b["type"] == "part":
            cur_part_title = f'PART {b["num"]}. {b["title"]}'
            story.append(Paragraph(esc(cur_part_title), S["toc_part"]))
        elif b["type"] == "chapter":
            story.append(Paragraph(f'Chapter {b["num"]:02d}. {esc(b["title"])}', S["toc_chap"]))
        elif b["type"] == "epilogue_head":
            story.append(Paragraph("에필로그", S["toc_part"]))
    return story


# ---------------- page callbacks ----------------
CURRENT = {"part_num": None, "part_title": "", "chapter_num": None, "chapter_title": ""}
# BUILD_STATE: 문서 조립(story 리스트 생성) 단계에서만 쓰는 동기 상태.
# CURRENT는 오직 _RunningHeaderMarker.draw()에서만 갱신되어야 실제 렌더링 순서와
# 어긋나지 않는다(2~4페이지에 "에필로그" 러닝 헤더가 잘못 표시되던 버그의 원인이
# CURRENT를 조립 단계에서 동기적으로도 같이 바꾸던 것이었음). cover_chapter()처럼
# 조립 시점에 "지금 PART 번호가 뭔지" 알아야 하는 곳은 BUILD_STATE만 참조한다.
BUILD_STATE = {"part_num": None}


class _RunningHeaderMarker(Flowable):
    """실제 문서 흐름(진짜 렌더링 시점) 중에 CURRENT를 갱신하기 위한 크기 0 마커.
    story 리스트를 미리 다 만든 뒤 한 번에 doc.build()를 호출하는 구조상,
    CURRENT를 파이썬 루프에서 바로 바꾸면 onPage 콜백이 항상 '루프가 끝난 뒤의
    최종 값'만 보게 되는 버그가 있어(러닝 헤더가 전부 비거나 마지막 챕터로 고정됨),
    실제 draw() 호출 시점(문서가 그 지점을 실제로 그릴 때)에 갱신하도록 분리."""

    def __init__(self, part_num=None, chapter_num=None, chapter_title=""):
        Flowable.__init__(self)
        self.width = 0
        self.height = 0
        self._part_num = part_num
        self._chapter_num = chapter_num
        self._chapter_title = chapter_title

    def wrap(self, availWidth, availHeight):
        return (0, 0)

    def draw(self):
        CURRENT["part_num"] = self._part_num
        CURRENT["chapter_num"] = self._chapter_num
        CURRENT["chapter_title"] = self._chapter_title


def make_body_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(WHITE)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    left = None
    if CURRENT["chapter_num"] is not None:
        left = f'PART {CURRENT["part_num"]} · CHAPTER {CURRENT["chapter_num"]:02d}'
    elif CURRENT["part_num"] == "에필로그":
        left = "에필로그"
    if left:
        canvas.setFont("NotoKR-Bold", 8.2)
        canvas.setFillColor(GRAY)
        canvas.drawString(MARGIN_X, PAGE_H - 34, left)
        canvas.setStrokeColor(SKY_LINE)
        canvas.setLineWidth(0.6)
        canvas.line(MARGIN_X, PAGE_H - 40, PAGE_W - MARGIN_X, PAGE_H - 40)
    canvas.setFont("NotoKR", 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(PAGE_W / 2, 24, str(canvas.getPageNumber()))
    canvas.restoreState()


def make_cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(WHITE)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFont("NotoKR", 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(PAGE_W / 2, 24, str(canvas.getPageNumber()))
    canvas.restoreState()


def step_badge(num_label, title):
    badge = Table([[Paragraph(str(num_label), ParagraphStyle("stepnum", fontName="NotoKR-Bold",
                                                              fontSize=11.5, textColor=WHITE,
                                                              alignment=TA_CENTER))]],
                  colWidths=[24], rowHeights=[24])
    badge.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ROUNDEDCORNERS", [12, 12, 12, 12]),
    ]))
    right = Paragraph(esc(title), S["step_title"])
    row = Table([[badge, right]], colWidths=[32, CONTENT_W - 32])
    row.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return row


def render_workflow_poster(block):
    """책 전체를 설명하는 대표 인포그래픽(IMG-002) — 삽화가 아니라 포스터처럼."""
    fname = os.path.basename(block["src"])
    path = os.path.join(ASSETS, fname)
    flows = [Spacer(1, 2)]
    flows.append(Paragraph("이 책의 Workflow", ParagraphStyle("wftitle", fontName="NotoKR-Bold",
                                                             fontSize=14.5, textColor=NAVY, alignment=TA_CENTER)))
    flows.append(Spacer(1, 6))
    if os.path.exists(path):
        with PILImage.open(path) as im:
            iw, ih = im.size
        disp_w = CONTENT_W * 1.0
        disp_h = ih * (disp_w / iw)
        # Final Book Polish — 이 페이지는 "책의 얼굴"이므로 포스터 이미지만 약 5%
        # 확대해 임팩트를 더한다(383 -> 402, 5~8% 범위 하한). 본문 텍스트·다른
        # 이미지는 그대로 두고, 이 포스터만 본문 여백을 살짝 넘어서도록 허용한다.
        # 확대분을 같은 페이지 안에 담기 위해 제목·캡션 주변의 여백만 아주
        # 조금 줄였다(문장·크기 자체는 그대로).
        max_h = 402
        if disp_h > max_h:
            disp_h = max_h
            disp_w = iw * (max_h / ih)
        flows.append(RLImage(path, width=disp_w, height=disp_h, hAlign="CENTER"))
    cap = block.get("caption", "")
    if cap:
        cap_clean = re.sub(r'^IMG-\d+\s*[·\-]\s*', '', cap).strip()
        flows.append(Paragraph(esc(cap_clean), ParagraphStyle("wfcap", parent=S["caption"], spaceBefore=4)))
    flows.append(Paragraph("이 책은 이 Workflow를 하나씩 완성하는 과정입니다.",
                            ParagraphStyle("wftakeaway", parent=S["takeaway"], spaceBefore=6)))
    return flows


def render_para_run(run):
    """본문 리듬(Round 5 고도화 + Round 6 고아줄 방지) — 연속된 '문단'들을 받아
    문단 간격만으로 읽는 호흡을 만든다. 글자 크기·행간은 그대로 두고, 아래
    규칙만 적용한다(모두 spaceBefore/spaceAfter 조정, 문장·순서 변경 없음):
      1) 결론 문장(묶음의 마지막 문단, 문단이 2개 이상일 때만) — 앞 여백을
         키워 "이제 정리한다"는 느낌을 준다.
      2) 짧은 전환/중요 문장(30자 이하) — 앞뒤 모두 살짝 넓혀 혼자 숨 쉬게
         한다. 묶음의 처음·끝에 있어도 적용된다.
      3) 긴 문단(90자 이상) — 뒤 여백을 아주 조금 더 줘 읽고 난 뒤 잠깐
         쉬어가게 한다.
      4) (Round 6) 결론 문장 앞 여백을 키우다 보니, 바로 앞에 카드처럼 자리를
         많이 차지하는 요소가 있으면 이 마지막 문장 한 줄만 다음 페이지로
         밀려 "거의 빈 페이지에 한 줄"처럼 보이는 경우가 있었다. 짧은 마무리
         묶음(문단이 정확히 2개, 합쳐서 160자 이하)은 KeepTogether로 묶어
         마지막 문장이 혼자 떨어져 나가지 않게 한다.
    이 함수는 full_build()의 본문 조판과 brand_samples.py의 12페이지 샘플
    렌더러가 동일하게 사용해야, 샘플에서 본 리듬이 실제 전체 조판과 같아진다."""
    out = []
    n = len(run)
    for i, p in enumerate(run):
        text = p["text"]
        base = S["dialogue"] if is_dialogue(text) else S["story"]
        length = len(text)
        is_last = (i == n - 1 and n >= 2)
        is_short = length <= 30
        is_long = length >= 90

        extra_before = 0
        extra_after = 0
        if is_last:
            extra_before = max(extra_before, 12)   # 결론 문장 앞 여백 확대
            extra_after = max(extra_after, 11)     # 다음 카드/제목으로 넘어가기 전 숨쉬기(기존 유지)
        if is_short:
            extra_before = max(extra_before, 9)    # 짧은 전환/중요 문장 — 혼자 숨쉬게(양쪽)
            extra_after = max(extra_after, 10)
        if is_long and not is_short:
            extra_after = max(extra_after, 4)      # 긴 문단 뒤 아주 약간의 여유

        if extra_before or extra_after:
            style = ParagraphStyle(
                f"story_dyn_{i}_{id(p)}", parent=base,
                spaceBefore=(base.spaceBefore or 0) + extra_before,
                spaceAfter=base.spaceAfter + extra_after,
            )
        else:
            style = base
        out.append(Paragraph(esc(text), style))

    if n == 2 and sum(len(p["text"]) for p in run) <= 160:
        return [KeepTogether(out)]
    return out


def produce(b, in_practice=False):
    t = b["type"]
    if t == "para":
        style = S["dialogue"] if is_dialogue(b["text"]) else S["story"]
        return [Paragraph(esc(b["text"]), style)]
    if t == "checklist":
        return box_checklist(b["items"])
    if t == "table":
        return render_table(b["rows"])
    if t == "image":
        if b.get("anchor") == "IMG-002":
            return render_workflow_poster(b)
        return render_image_block(b)
    if t == "hr":
        return [Spacer(1, 4)]
    if t == "blockquote":
        return produce_blockquote(b)
    return []


# ---------------- blockquote kind (classify_blockquote + 보완 휴리스틱) ----------------
def my_classify(qlines):
    kind, body = classify_blockquote(qlines)
    if kind == "generic_quote":
        lines = body_lines(body)
        first = lines[0].strip() if lines else ""
        if re.match(r'^\*\*핵심\s*(정리|메시지)\*\*$', first):
            return "core_message", body
        if any("___" in l for l in lines):
            return "prompt", body
        if any(l.strip() == "↓" for l in lines):
            return "workflow", body
        if re.match(r'^\*\*완료\s*·', first):
            return "done_marker", body
    return kind, body


def produce_blockquote(b):
    kind, body = my_classify(b["lines"])
    if kind == "progress_card":
        return box_progress_card(body)
    if kind == "case":
        return box_case(body)
    if kind == "workflow":
        return box_workflow(body)
    if kind == "caution":
        return box_caution(body)
    if kind == "core_message":
        return box_core_message(body)
    if kind == "celebration":
        return box_celebration(body)
    if kind == "today_made":
        return box_today_made(body)
    if kind == "done_marker":
        return box_done_marker(body)
    if kind == "author_note":
        return box_author_note(body)
    if kind == "preview":
        return box_preview(body)
    if kind == "prompt":
        return box_prompt(body)
    if kind == "qr":
        global QR_COUNTER
        QR_COUNTER += 1
        qr_path = os.path.join(QR, f"qr_{QR_COUNTER:02d}.png")
        return box_qr(body, qr_path)
    return box_generic(body)


QR_COUNTER = 0


# ---------------- main build ----------------
def build():
    blocks = parse(os.path.join(BASE, "book-source-final.md"))
    N = len(blocks)

    # PART -> chapter 목록 미리 계산 (PART 표지의 Chapter 범위 표기용)
    part_chapters = {}
    cur_p = None
    for b in blocks:
        if b["type"] == "part":
            cur_p = b["num"]
            part_chapters[cur_p] = []
        elif b["type"] == "chapter":
            part_chapters[cur_p].append(b["num"])

    doc = BaseDocTemplate(OUT, pagesize=A5,
                           leftMargin=MARGIN_X, rightMargin=MARGIN_X,
                           topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM)
    body_frame = Frame(MARGIN_X, MARGIN_BOTTOM, CONTENT_W, PAGE_H - MARGIN_TOP - MARGIN_BOTTOM,
                        id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    cover_frame = Frame(MARGIN_X, MARGIN_BOTTOM, CONTENT_W, PAGE_H - MARGIN_TOP - MARGIN_BOTTOM,
                         id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=make_cover_page),
        PageTemplate(id="body", frames=[body_frame], onPage=make_body_page),
    ])

    story = []
    story.append(NextPageTemplate("cover"))
    story.extend(cover_book())
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())
    story.extend(build_toc(blocks))

    keep_buffer = None
    in_practice = False

    def emit(flowables):
        nonlocal keep_buffer
        if keep_buffer is not None:
            keep_buffer.extend(flowables)
        else:
            story.extend(flowables)

    idx = 0
    while idx < N:
        b = blocks[idx]
        t = b["type"]

        # 표지에 이미 사용된 원고 최상단 대표 제목(H1) 중복 노출 방지
        # (book-source-final.md 1행의 "# 『...』" 는 표지(cover_book)에서 이미 사용했으므로
        #  본문 흐름에 그대로 노출되지 않도록 건너뜀 — 원고 삭제가 아니라 렌더링 중복 제거)
        if t == "para" and b["text"].lstrip().startswith("#"):
            idx += 1
            continue

        if t == "part":
            story.append(NextPageTemplate("cover"))
            story.append(PageBreak())
            story.extend(cover_part(b["num"], b["title"], part_chapters.get(b["num"], [b["num"]])))
            story.append(NextPageTemplate("body"))
            # BUILD_STATE는 조립 단계 전용(다음 chapter cover가 자기 PART 번호를
            # 알기 위한 용도). 실제 페이지에 표시되는 러닝 헤더는 마커가 그려지는
            # 시점에만 CURRENT를 갱신하므로 여기서 CURRENT를 직접 건드리지 않는다.
            BUILD_STATE["part_num"] = b["num"]
            story.append(_RunningHeaderMarker(part_num=b["num"], chapter_num=None))
            idx += 1
            continue

        if t == "chapter":
            story.append(NextPageTemplate("cover"))
            story.append(PageBreak())
            story.extend(cover_chapter(b["num"], b["title"]))
            story.append(NextPageTemplate("body"))
            in_practice = False
            story.append(_RunningHeaderMarker(part_num=BUILD_STATE["part_num"], chapter_num=b["num"], chapter_title=b["title"]))
            idx += 1
            continue

        if t == "epilogue_head":
            story.append(NextPageTemplate("cover"))
            story.append(PageBreak())
            story.extend(cover_epilogue())
            story.append(NextPageTemplate("body"))
            BUILD_STATE["part_num"] = "에필로그"
            story.append(_RunningHeaderMarker(part_num="에필로그", chapter_num=None))
            idx += 1
            continue

        if t == "keep_start":
            keep_buffer = []
            idx += 1
            continue
        if t == "keep_end":
            if keep_buffer is not None:
                story.append(KeepTogether(keep_buffer))
            keep_buffer = None
            idx += 1
            continue

        if t == "h3":
            emit([Paragraph(esc(b["text"]), S["subhead"])])
            idx += 1
            continue

        if t == "h4":
            m = re.match(r'^(실습\s*\d+)\s*[—\-]\s*(.*)$', b["text"].strip())
            if m:
                in_practice = True
                flows = [Paragraph(m.group(1), S["running"]), Paragraph(esc(m.group(2)), S["h2"])]
            else:
                in_practice = False
                flows = [Paragraph(esc(b["text"]), S["h2"])]
            # 다음 블록과 함께 묶어 고아 제목 방지
            if idx + 1 < N and blocks[idx + 1]["type"] not in ("part", "chapter", "epilogue_head", "keep_start", "keep_end"):
                nxt = blocks[idx + 1]
                nxt_flows = produce(nxt, in_practice)
                if keep_buffer is None:
                    story.append(KeepTogether(flows + nxt_flows))
                else:
                    keep_buffer.extend(flows + nxt_flows)
                idx += 2
                continue
            emit(flows)
            idx += 1
            continue

        if t == "h5":
            text = b["text"].strip()
            m = re.match(r'^(\d+)\.\s*(.*)$', text)
            m2 = re.match(r'^([A-Z])\.\s*(.*)$', text)
            if in_practice and m:
                flows = [step_badge(m.group(1), m.group(2))]
            elif in_practice and m2:
                flows = [step_badge(m2.group(1), m2.group(2))]
            else:
                flows = [Paragraph(esc(text), ParagraphStyle("h5sub", fontName="NotoKR-Bold", fontSize=10, textColor=NAVY, spaceBefore=6, spaceAfter=4))]
            emit(flows)
            idx += 1
            continue

        if t == "image" and b.get("anchor") == "IMG-002":
            story.append(PageBreak())

        if t == "para":
            # 챕터/PART가 끝나기 직전의 마지막 짧은 문단(들) — 앞의 카드 묶음 뒤에
            # 혼자 남아 거의 빈 페이지("고아 문단")가 되는 것을 막기 위해, 이런
            # 위치의 문단만 의도된 클로징 문장(beat)으로 렌더링해 KeepTogether로 묶는다.
            # (원고 문장은 그대로, 다음 챕터/PART 시작 위치도 그대로 유지됨)
            j = idx
            run = []
            while j < N and blocks[j]["type"] == "para":
                run.append(blocks[j])
                j += 1
            is_closing = (j < N and blocks[j]["type"] == "hr" and
                          j + 1 < N and blocks[j + 1]["type"] in ("part", "chapter", "epilogue_head"))
            if is_closing and len(run) <= 2 and all(len(p["text"]) <= 40 for p in run):
                beat_flows = [Paragraph(esc(p["text"]), S["beat"]) for p in run]
                if keep_buffer is None:
                    story.append(KeepTogether(beat_flows))
                else:
                    keep_buffer.extend(beat_flows)
                idx = j
                continue

            # Round 5: 문단이 1개뿐이어도(짧은 독립 문장/긴 문단) 리듬 규칙이
            # 적용되도록 항상 render_para_run()을 거친다.
            emit(render_para_run(run))
            idx = j
            continue

        flows = produce(b, in_practice)
        if keep_buffer is None and t in ("table", "image", "blockquote", "checklist") and flows:
            story.append(KeepTogether(flows))
        else:
            emit(flows)
        idx += 1

    doc.build(story)
    print("DONE", OUT, "pages built")


if __name__ == "__main__":
    build()

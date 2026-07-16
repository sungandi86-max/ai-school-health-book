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
SKY = colors.HexColor("#EAF2FB")
SKY_LINE = colors.HexColor("#D3E4F5")
INK = colors.HexColor("#232323")
GRAY = colors.HexColor("#8A8F99")
WHITE = colors.white
GOLD_TEXT = colors.HexColor("#8A6D1D")  # 주의 라벨 전용 (색상 시스템 내 강조, 새 색 추가 아님: 텍스트만)

PAGE_W, PAGE_H = A5
MARGIN_X = 52
MARGIN_TOP = 50
MARGIN_BOTTOM = 44
CONTENT_W = PAGE_W - 2 * MARGIN_X

BOOK_TITLE = "『보건교사를 위한 AI 업무 자동화』"
BOOK_TITLE_PLAIN = "보건교사를 위한 AI 업무 자동화"
AUTHOR = "쑤캥"
TAGLINE = "반복되는 업무 하나를 구조로 바꾸는 프로젝트북"

# ---------------- styles (design-v2 v2.1과 동일 수치) ----------------
S = {}
S["running"] = ParagraphStyle("running", fontName="NotoKR-Bold", fontSize=8.5, leading=11.5, textColor=GRAY)
S["h1"] = ParagraphStyle("h1", fontName="NotoKR-Bold", fontSize=20, leading=26, textColor=NAVY)
S["h2"] = ParagraphStyle("h2", fontName="NotoKR-Bold", fontSize=14, leading=19, textColor=NAVY, spaceBefore=10, spaceAfter=6)
S["lead"] = ParagraphStyle("lead", fontName="NotoKR", fontSize=9.4, leading=17.4, textColor=NAVY_SOFT)
S["body"] = ParagraphStyle("body", fontName="NotoKR", fontSize=9.6, leading=18.8, textColor=INK, spaceAfter=10)
S["story"] = ParagraphStyle("story", fontName="NotoKR", fontSize=10, leading=19, textColor=INK, spaceAfter=13,
                             leftIndent=11, rightIndent=11)
S["dialogue"] = ParagraphStyle("dialogue", parent=S["story"], leftIndent=22, textColor=NAVY, fontName="NotoKR-Bold")
S["beat"] = ParagraphStyle("beat", fontName="NotoKR-Bold", fontSize=11.5, leading=18, textColor=NAVY, alignment=TA_CENTER, spaceBefore=10, spaceAfter=10)
S["cardlabel"] = ParagraphStyle("cardlabel", fontName="NotoKR-Bold", fontSize=9.2, leading=13, textColor=NAVY)
S["cardbody"] = ParagraphStyle("cardbody", fontName="NotoKR", fontSize=8.8, leading=14.5, textColor=INK)
S["caption"] = ParagraphStyle("caption", fontName="NotoKR", fontSize=8.3, leading=13.2, textColor=NAVY_SOFT, spaceBefore=6, spaceAfter=10, alignment=TA_CENTER)
S["takeaway"] = ParagraphStyle("takeaway", fontName="NotoKR-Bold", fontSize=10.6, leading=16.8, textColor=NAVY, alignment=TA_CENTER)
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


def soft_card(rows_flowables, pad=12, bg=SKY, radius=12, box=False, box_color=SKY_LINE):
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
    ]
    if box:
        style.append(("BOX", (0, 0), (-1, -1), 1, box_color))
    t.setStyle(TableStyle(style))
    return t


def stamp(text, bold_prefix="완료 확인"):
    p = Paragraph(f"&#10003;&nbsp;&nbsp;{esc(bold_prefix)} — {esc(text)}",
                  ParagraphStyle("stamp", parent=S["cardlabel"], fontSize=9.4, textColor=NAVY))
    t = Table([[p]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SKY),
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("ROUNDEDCORNERS", [8, 8, 8, 8]),
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


def workflow_arrow_lines(lines):
    """Workflow 화살표(↓) 구분줄만 압축된 전용 스타일로, 나머지는 카드 본문 스타일로."""
    arrow_style = ParagraphStyle("wfarrow", fontName="NotoKR", fontSize=9.2, leading=9,
                                  textColor=NAVY_SOFT, alignment=TA_CENTER, spaceBefore=2, spaceAfter=2)
    out = []
    for l in lines:
        s = l.strip()
        if not s:
            continue
        if s == "↓":
            out.append(Paragraph(s, arrow_style))
        elif s.startswith("**") and s.endswith("**") and s.count("**") == 2:
            out.append(Paragraph(esc(s), S["cardlabel"]))
        else:
            out.append(Paragraph(esc(s), S["cardbody"]))
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
    card = soft_card(rows, pad=16)
    extra = []
    if part_prog:
        extra.append(Paragraph(esc(part_prog), ParagraphStyle("pprog", fontName="NotoKR", fontSize=8.3, textColor=GRAY, alignment=TA_CENTER, spaceBefore=6)))
    return [card] + extra


def box_case(body):
    lines = body_lines(body)
    return [soft_card(render_lines(lines), pad=12)]


def box_workflow(body):
    lines = body_lines(body)
    return [soft_card(workflow_arrow_lines(lines), pad=12)]


def box_caution(body):
    lines = body_lines(body)
    return [soft_card(render_lines(lines), pad=12)]


def box_core_message(body):
    lines = body_lines(body)
    # 첫줄(**핵심 정리**/**핵심 메시지**) 라벨 + 나머지는 강조 takeaway 톤
    out = [Paragraph(esc(lines[0]), S["cardlabel"]), Spacer(1, 5)]
    for l in lines[1:]:
        s = l.strip()
        style = ParagraphStyle("coremsg", parent=S["cardbody"], fontName="NotoKR-Bold", textColor=NAVY) \
            if s.startswith("**") and s.endswith("**") else S["cardbody"]
        out.append(Paragraph(esc(s), style))
    return [soft_card(out, pad=13)]


def box_celebration(body):
    lines = body_lines(body)
    text = " ".join(l.strip("* ") for l in lines[1:]) if len(lines) > 1 else lines[0].strip("* ")
    return [stamp(text, bold_prefix="작은 축하")]


def box_today_made(body):
    lines = body_lines(body)[1:]
    out = []
    for l in lines:
        s = l.strip()
        if s.startswith("✓"):
            out.append(Paragraph(esc(s), S["cardbody"]))
        else:
            out.append(Paragraph(f"<b>{esc(s)}</b>", ParagraphStyle("tm", parent=S["cardlabel"])))
    return [soft_card([Paragraph("오늘 만든 프로젝트", S["cardlabel"]), Spacer(1, 4)] + out, pad=12)]


def box_author_note(body):
    lines = body_lines(body)[1:]
    out = [Paragraph("쑤캥의 한마디", S["cardlabel"]), Spacer(1, 4)]
    out += [Paragraph(esc(l), ParagraphStyle("author", parent=S["cardbody"])) for l in lines]
    return [soft_card(out, pad=12)]


def box_preview(body):
    lines = body_lines(body)
    label = lines[0].strip("* ")
    out = [Paragraph(esc(label), S["cardlabel"]), Spacer(1, 4)]
    out += [Paragraph(esc(l), S["cardbody"]) for l in lines[1:]]
    return [soft_card(out, pad=12, bg=colors.HexColor("#F5F7FA"))]


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
        ("BOX", (0, 0), (-1, -1), 1, SKY_LINE),
        ("ROUNDEDCORNERS", [10, 10, 10, 10]),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return [t]


def box_prompt(body):
    lines = body_lines(body)
    out = [Paragraph("PROMPT", ParagraphStyle("promptlabel", fontName="NotoKR-Bold", fontSize=8.2, textColor=NAVY_SOFT)),
           Spacer(1, 4)]
    out += [Paragraph(esc(l), S["prompt"]) for l in lines]
    return [soft_card(out, pad=11, bg=WHITE, radius=10, box=True)]


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
    body_rows = [r for i, r in enumerate(cells) if i >= 2]
    out = []
    for r in body_rows:
        if len(r) < 3 or not (r[0].strip() or r[2].strip()):
            continue
        before, arrow, after = r[0], r[1] or "→", r[2]
        row = Table([[
            Paragraph(esc(before), S["cardbody"]),
            Paragraph(f"<font color='#4A5A7A'>{esc(arrow)}</font>", ParagraphStyle("baArrow", parent=S["cardbody"], alignment=TA_CENTER)),
            Paragraph(esc(after), ParagraphStyle("baAfter", parent=S["cardbody"], fontName="NotoKR-Bold", textColor=NAVY)),
        ]], colWidths=[CONTENT_W * 0.42, CONTENT_W * 0.10, CONTENT_W * 0.48])
        row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
        out.append(row)
        out.append(Spacer(1, 4))
    return [soft_card([Paragraph("오늘 바뀐 것", S["cardlabel"]), Spacer(1, 6)] + out, pad=13)]


def table_generic(cells):
    header = cells[0]
    body_rows = [r for i, r in enumerate(cells) if i >= 2]
    ncols = len(header)
    data = [[Paragraph(esc(h), S["table_head"]) for h in header]]
    for r in body_rows:
        r = (r + [""] * ncols)[:ncols]
        data.append([Paragraph(esc(c), S["table_cell"]) for c in r])
    colw = CONTENT_W / ncols
    t = Table(data, colWidths=[colw] * ncols, repeatRows=1)
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
    fname = os.path.basename(block["src"])
    path = os.path.join(ASSETS, fname)
    flows = []
    if os.path.exists(path):
        with PILImage.open(path) as im:
            iw, ih = im.size
        disp_w = CONTENT_W * 0.94
        disp_h = ih * (disp_w / iw)
        max_h = 400
        if disp_h > max_h:
            disp_h = max_h
            disp_w = iw * (max_h / ih)
        flows.append(RLImage(path, width=disp_w, height=disp_h, hAlign="CENTER"))
    cap = block.get("caption", "")
    if cap:
        # 내부 표기(IMG-00N ·) 제거, 독자용 문장만 남긴다
        cap_clean = re.sub(r'^IMG-\d+\s*[·\-]\s*', '', cap).strip()
        flows.append(Paragraph(esc(cap_clean), S["caption"]))
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
    story = [Spacer(1, 96)]
    story.append(Paragraph(f"PART {num}", S["running"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(esc(title), S["h1"]))
    story.append(Spacer(1, 20))
    ch_range = f"Chapter {chapters[0]:02d}–{chapters[-1]:02d}" if len(chapters) > 1 else f"Chapter {chapters[0]:02d}"
    story.append(Paragraph(ch_range, ParagraphStyle("partrange", fontName="NotoKR", fontSize=9.6, textColor=NAVY_SOFT)))
    story.append(Spacer(1, 200))
    story.append(Paragraph(TAGLINE, ParagraphStyle("parttag", fontName="NotoKR", fontSize=8.6, textColor=GRAY, alignment=TA_CENTER)))
    return story


def cover_chapter(num, title):
    story = [Spacer(1, 70)]
    story.append(Paragraph(f"PART {CURRENT['part_num']} · CHAPTER {num:02d}", S["running"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(esc(title), S["h1"]))
    story.append(Spacer(1, 220))
    story.append(Paragraph(BOOK_TITLE_PLAIN, ParagraphStyle("chaptag", fontName="NotoKR", fontSize=8.3, textColor=GRAY, alignment=TA_CENTER)))
    return story


def cover_epilogue():
    story = [Spacer(1, 110)]
    story.append(Paragraph("EPILOGUE", S["running"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("에필로그", S["h1"]))
    story.append(Spacer(1, 220))
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
    flows = [Spacer(1, 4)]
    flows.append(Paragraph("이 책의 Workflow", ParagraphStyle("wftitle", fontName="NotoKR-Bold",
                                                             fontSize=14.5, textColor=NAVY, alignment=TA_CENTER)))
    flows.append(Spacer(1, 10))
    if os.path.exists(path):
        with PILImage.open(path) as im:
            iw, ih = im.size
        disp_w = CONTENT_W * 1.0
        disp_h = ih * (disp_w / iw)
        max_h = 383
        if disp_h > max_h:
            disp_h = max_h
            disp_w = iw * (max_h / ih)
        flows.append(RLImage(path, width=disp_w, height=disp_h, hAlign="CENTER"))
    cap = block.get("caption", "")
    if cap:
        cap_clean = re.sub(r'^IMG-\d+\s*[·\-]\s*', '', cap).strip()
        flows.append(Paragraph(esc(cap_clean), S["caption"]))
    flows.append(Paragraph("이 책은 이 Workflow를 하나씩 완성하는 과정입니다.", S["takeaway"]))
    return flows


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
            CURRENT["part_num"] = b["num"]
            CURRENT["part_title"] = b["title"]
            CURRENT["chapter_num"] = None
            # 러닝 헤더는 onPage 콜백이 실제 렌더링 시점에 읽으므로,
            # 파이썬 루프 시점의 CURRENT 값이 아니라 이 마커가 실제로 그려지는
            # 시점에 CURRENT를 갱신해야 각 페이지에 올바른 PART/CHAPTER가 표시됨
            story.append(_RunningHeaderMarker(part_num=b["num"], chapter_num=None))
            idx += 1
            continue

        if t == "chapter":
            story.append(NextPageTemplate("cover"))
            story.append(PageBreak())
            story.extend(cover_chapter(b["num"], b["title"]))
            story.append(NextPageTemplate("body"))
            CURRENT["chapter_num"] = b["num"]
            CURRENT["chapter_title"] = b["title"]
            in_practice = False
            story.append(_RunningHeaderMarker(part_num=CURRENT["part_num"], chapter_num=b["num"], chapter_title=b["title"]))
            idx += 1
            continue

        if t == "epilogue_head":
            story.append(NextPageTemplate("cover"))
            story.append(PageBreak())
            story.extend(cover_epilogue())
            story.append(NextPageTemplate("body"))
            CURRENT["chapter_num"] = None
            CURRENT["part_num"] = "에필로그"
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

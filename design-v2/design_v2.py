#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
『보건교사를 위한 AI 업무 자동화』 book v2 편집 디자인 시안
- 기존 pdf/book-final-pass2.pdf 및 그 조판 코드(build_pdf.py)를 전혀 참고하지 않고 새로 작성.
- book-source/book-source-final.md 의 실제 원고만 사용 (더미 텍스트 없음).
- 레퍼런스(『보건실은 운영된다』, Canva 전자책)의 "레이아웃 철학"만 분석해 반영:
  여백 중심, 소프트 카드형 정보 단위, 절제된 포인트 컬러, 짧은 문단, 굵은 한 줄 요약.
  색상/폰트/이미지 등 실제 자산은 복제하지 않고 본 도서의 브랜드(딥네이비+연블루)로 새로 설계.
"""
import os
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, PageBreak, Image as RLImage, Flowable
)
from reportlab.lib.styles import ParagraphStyle
from PIL import Image as PILImage

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
FONTS = os.path.join(BASE, "fonts")
OUT = os.path.join(BASE, "book-v2-samples.pdf")

pdfmetrics.registerFont(TTFont("NotoKR", os.path.join(FONTS, "NotoKR-Regular.ttf")))
pdfmetrics.registerFont(TTFont("NotoKR-Bold", os.path.join(FONTS, "NotoKR-Bold.ttf")))

# ---------------- design system (v2) ----------------
NAVY = colors.HexColor("#16233F")
NAVY_SOFT = colors.HexColor("#4A5A7A")
SKY = colors.HexColor("#EAF2FB")
SKY_LINE = colors.HexColor("#D3E4F5")
INK = colors.HexColor("#232323")
GRAY = colors.HexColor("#8A8F99")
WHITE = colors.white
PILL = colors.HexColor("#DCEAFB")

PAGE_W, PAGE_H = A5
MARGIN_X = 52
MARGIN_TOP = 58
MARGIN_BOTTOM = 46
CONTENT_W = PAGE_W - 2 * MARGIN_X

# ---- 타이포그래피 v2.1 (출판사 QA 폴리시): 장시간 가독성 재조정 ----
# 제목 -13%(h1) / -9.7%(h2), 본문류 -8~9%, 행간 비율 +10~12%, 카드/캡션/Prompt/체크리스트 비례 축소
S = {}
S["running"] = ParagraphStyle("running", fontName="NotoKR-Bold", fontSize=8.5, leading=11.5, textColor=GRAY)
S["h1"] = ParagraphStyle("h1", fontName="NotoKR-Bold", fontSize=20, leading=26, textColor=NAVY)
S["h2"] = ParagraphStyle("h2", fontName="NotoKR-Bold", fontSize=14, leading=19, textColor=NAVY)
S["lead"] = ParagraphStyle("lead", fontName="NotoKR", fontSize=9.4, leading=17.4, textColor=NAVY_SOFT)
S["body"] = ParagraphStyle("body", fontName="NotoKR", fontSize=9.6, leading=18.8, textColor=INK)
S["story"] = ParagraphStyle("story", fontName="NotoKR", fontSize=10, leading=19, textColor=INK, spaceAfter=13,
                             leftIndent=11, rightIndent=11)
S["dialogue"] = ParagraphStyle("dialogue", parent=S["story"], leftIndent=22, textColor=NAVY, fontName="NotoKR-Bold")
S["beat"] = ParagraphStyle("beat", fontName="NotoKR-Bold", fontSize=11.5, leading=18, textColor=NAVY, alignment=TA_CENTER, spaceBefore=10)
S["cardlabel"] = ParagraphStyle("cardlabel", fontName="NotoKR-Bold", fontSize=9.2, leading=13, textColor=NAVY)
S["cardbody"] = ParagraphStyle("cardbody", fontName="NotoKR", fontSize=8.8, leading=14.5, textColor=INK)
S["cardex"] = ParagraphStyle("cardex", fontName="NotoKR", fontSize=8.1, leading=12.2, textColor=NAVY_SOFT)
S["caption"] = ParagraphStyle("caption", fontName="NotoKR", fontSize=8.3, leading=13.2, textColor=NAVY_SOFT, spaceBefore=6)
S["takeaway"] = ParagraphStyle("takeaway", fontName="NotoKR-Bold", fontSize=10.6, leading=16.8, textColor=NAVY, alignment=TA_CENTER)
S["step_title"] = ParagraphStyle("step_title", fontName="NotoKR-Bold", fontSize=10.1, leading=14, textColor=NAVY)
S["step_body"] = ParagraphStyle("step_body", fontName="NotoKR", fontSize=9.0, leading=14.5, textColor=INK)
S["prompt"] = ParagraphStyle("prompt", fontName="NotoKR", fontSize=8.8, leading=14.5, textColor=NAVY, leftIndent=4)
S["check"] = ParagraphStyle("check", fontName="NotoKR", fontSize=9.0, leading=14.5, textColor=INK)
S["badge"] = ParagraphStyle("badge", fontName="NotoKR-Bold", fontSize=9.7, leading=12.5, textColor=NAVY, alignment=TA_CENTER)
S["eyebrow"] = ParagraphStyle("eyebrow", fontName="NotoKR-Bold", fontSize=8, leading=11, textColor=GRAY)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def running_header(part_label, chapter_label):
    left = Paragraph(esc(part_label), S["running"])
    right = Paragraph(esc(chapter_label), ParagraphStyle("runningR", parent=S["running"], alignment=TA_LEFT))
    t = Table([[left, right]], colWidths=[CONTENT_W * 0.6, CONTENT_W * 0.4])
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.6, SKY_LINE),
    ]))
    return t


def soft_card(rows_flowables, pad=16, bg=SKY, radius=12):
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
    t.setStyle(TableStyle(style))
    return t


def pill(text, w=None):
    """실습 완료 표시: 버튼처럼 보이지 않도록 낮은 채도(카드와 동일 톤)·낮은 라운드·
    좌측 정렬 체크마크로 '워크북 완료 확인' 느낌만 준다 (디자인 변경 아님, 표현 방식만 조정)."""
    p = Paragraph(f"&#10003;&nbsp;&nbsp;완료 확인 — {esc(text)}",
                  ParagraphStyle("stamp", parent=S["cardlabel"], fontSize=9.4, textColor=NAVY))
    data = [[p]]
    t = Table(data, colWidths=[w or (CONTENT_W * 0.7)])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SKY),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("ROUNDEDCORNERS", [8, 8, 8, 8]),
    ]))
    return t


def step_badge_row(num, title, body_flowables):
    badge = Table([[Paragraph(str(num), ParagraphStyle("stepnum", fontName="NotoKR-Bold",
                                                        fontSize=11.5, textColor=WHITE,
                                                        alignment=TA_CENTER))]],
                  colWidths=[24], rowHeights=[24])
    badge.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ROUNDEDCORNERS", [12, 12, 12, 12]),
    ]))
    right = [Paragraph(esc(title), S["step_title"]), Spacer(1, 2)] + body_flowables
    row = Table([[badge, right]], colWidths=[32, CONTENT_W - 32])
    row.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return row


class HR(Flowable):
    def __init__(self, width, color=SKY_LINE, thickness=0.7):
        Flowable.__init__(self)
        self.width = width
        self.thickness = thickness
        self.color = color

    def wrap(self, aw, ah):
        return (self.width, self.thickness + 2)

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)


def page_howto():
    story = []
    story.append(Spacer(1, 14))
    story.append(Paragraph("이 책 사용법", S["h1"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "이 책은 PART 1부터 PART 8까지, 22개 Chapter로 이어집니다. "
        "각 Chapter는 아래 요소를 같은 순서로 반복합니다.", S["lead"]))
    story.append(Spacer(1, 12))

    # 정보 위계: 카드 디자인/색상/크기는 그대로 두고, 작은 eyebrow 라벨로 핵심/보조 그룹만 구분
    core_items = [
        ("프로젝트 진행 카드", "이 Chapter에서 오늘 만드는 것과 걸리는 시간, 난이도를 먼저 보여줍니다."),
        ("핵심 정리 / 핵심 메시지", "본문에서 관찰한 내용을 한 문장으로 압축합니다."),
        ("CASE / Workflow", "다른 사례이거나, 지금까지의 결정을 순서로 정리한 실제 업무 흐름입니다."),
    ]
    sub_items = [
        ("실습", "설명을 읽는 데서 끝나지 않고, 그 자리에서 직접 써보는 자리입니다."),
        ("오늘 만든 프로젝트 / 오늘 바뀐 것", "이 Chapter에서 완성한 결과물과, 그 전후의 생각 변화를 확인합니다."),
        ("쑤캥의 한마디 / 자료실 QR", "저자의 개인적인 조언과, 실습 파일을 내려받는 연결 통로입니다."),
    ]
    story.append(Paragraph("핵심 구성", S["eyebrow"]))
    story.append(Spacer(1, 4))
    for label, desc in core_items:
        card = soft_card([
            Paragraph(esc(label), S["cardlabel"]),
            Spacer(1, 3),
            Paragraph(esc(desc), S["cardbody"]),
        ], pad=9)
        story.append(card)
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 4))
    story.append(Paragraph("보조 구성", S["eyebrow"]))
    story.append(Spacer(1, 4))
    for label, desc in sub_items:
        card = soft_card([
            Paragraph(esc(label), S["cardlabel"]),
            Spacer(1, 3),
            Paragraph(esc(desc), S["cardbody"]),
        ], pad=9)
        story.append(card)
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "이야기 · 설명 · 프로젝트 화면 · 실습, 네 가지 페이지는 펼치는 순간 바로 구분됩니다.",
        S["takeaway"]))
    return story


def page_chapter_opening():
    story = []
    story.append(Spacer(1, 70))
    story.append(Paragraph("PART 1 · CHAPTER 01", S["running"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("하루 종일 바빴는데,<br/>아침 파일은 그대로였습니다", S["h1"]))
    story.append(Spacer(1, 26))

    stat_row = Table([[
        Paragraph("DAY 1", ParagraphStyle("st1", fontName="NotoKR-Bold", fontSize=9.6, textColor=NAVY)),
        Paragraph("걸리는 시간<br/><b>약 20분</b>", ParagraphStyle("st2", fontName="NotoKR", fontSize=8.6, textColor=NAVY_SOFT, leading=12.2)),
        Paragraph("난이도<br/><b>★☆☆☆☆</b>", ParagraphStyle("st3", fontName="NotoKR", fontSize=8.6, textColor=NAVY_SOFT, leading=12.2)),
    ]], colWidths=[CONTENT_W * 0.28, CONTENT_W * 0.36, CONTENT_W * 0.36])
    stat_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))

    card = soft_card([
        Paragraph("오늘 만드는 것", S["cardlabel"]),
        Spacer(1, 3),
        Paragraph("하루 한 장면 해부표", ParagraphStyle("bigmake", fontName="NotoKR-Bold", fontSize=12, textColor=NAVY)),
        Spacer(1, 12),
        stat_row,
    ], pad=18)
    story.append(card)
    story.append(Spacer(1, 40))
    story.append(Paragraph("PART 1 진행 · 시작 · 0 / 2", ParagraphStyle("prog", fontName="NotoKR", fontSize=9, textColor=GRAY, alignment=TA_CENTER)))
    return story


def page_story():
    story = []
    story.append(running_header("PART 1 · CHAPTER 01", "이야기"))
    story.append(Spacer(1, 20))
    story.append(Paragraph("메신저 알림음이 울렸습니다.", S["story"]))
    story.append(Paragraph("“선생님, 어제 보내주신 검진 링크가 어디에 있나요?”", S["dialogue"]))
    story.append(Paragraph(
        "아침에 열어둔 검진 공문은 아직 첫 페이지였습니다. 답장을 먼저 보내려고 메신저 검색창에 "
        "'검진'을 입력했습니다. 전날 보낸 메시지가 바로 나오지 않았습니다. 비슷한 제목의 안내가 몇 개 "
        "보였습니다. 하나씩 열어 날짜를 확인한 뒤에야 링크를 찾았습니다.", S["story"]))
    story.append(Paragraph("링크를 복사하는 순간 보건실 문이 열렸습니다.", S["story"]))
    story.append(Paragraph("“선생님, 체육 시간에 넘어졌어요.”", S["dialogue"]))
    story.append(Paragraph(
        "의자를 당겨 학생을 앉혔습니다. 상처를 살피고 처치한 뒤 기록을 남겼습니다. 사용한 물품을 "
        "정리하고 다시 자리에 앉으려는데 책상 전화가 울렸습니다.", S["story"]))
    story.append(Paragraph("그제야 아침에 읽던 공문으로 돌아왔습니다.", S["story"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("그런데 아침에 하려던 일은 그대로 남아 있었습니다.", S["beat"]))
    return story


def page_project():
    story = []
    story.append(running_header("PART 3 · CHAPTER 05", "프로젝트 화면"))
    story.append(Spacer(1, 14))
    story.append(Paragraph("화면이 열렸다는 사실이<br/>완성처럼 느껴졌습니다", S["h2"]))
    story.append(Spacer(1, 14))

    path = os.path.join(ASSETS, "01_first_online_health_room.png")
    with PILImage.open(path) as im:
        iw, ih = im.size
    disp_w = CONTENT_W * 0.92
    disp_h = ih * (disp_w / iw)
    max_h = 330
    if disp_h > max_h:
        disp_h = max_h
        disp_w = iw * (max_h / ih)
    img = RLImage(path, width=disp_w, height=disp_h, hAlign="CENTER")
    story.append(img)
    story.append(Paragraph(
        "처음 만든 온라인 보건실 화면입니다. 보기에는 제법 완성된 것 같았지만, "
        "실제 업무가 어떻게 이어지는지는 아직 충분히 확인하지 못했습니다.",
        ParagraphStyle("projcap", parent=S["caption"], alignment=TA_CENTER, spaceBefore=7, spaceAfter=11)))
    story.append(Paragraph(
        "화면은 정돈되어 있었습니다. 색도 맞았고, 카드 간격도 반듯했습니다. "
        "버튼을 누르면 다른 화면으로 이동했습니다.", S["body"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("화면이 열렸으니 프로젝트도 거의 끝났다고 생각했습니다.", S["beat"]))
    return story


def page_workflow():
    story = []
    story.append(Spacer(1, 6))
    story.append(Paragraph("이 책의 Workflow", ParagraphStyle("wftitle", fontName="NotoKR-Bold", fontSize=14.5, textColor=NAVY, alignment=TA_CENTER)))
    story.append(Spacer(1, 10))

    path = os.path.join(ASSETS, "07_ai_workflow.png")
    with PILImage.open(path) as im:
        iw, ih = im.size
    disp_w = CONTENT_W * 1.0
    disp_h = ih * (disp_w / iw)
    max_h = 383  # 기존 355 대비 약 +8%
    if disp_h > max_h:
        disp_h = max_h
        disp_w = iw * (max_h / ih)
    img = RLImage(path, width=disp_w, height=disp_h, hAlign="CENTER")
    story.append(img)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "이 책 전체에서 반복되는 AI 업무 자동화 Workflow 구조입니다. "
        "PART 1부터 8까지 만든 결과물이 이 흐름 위에서 하나로 연결됩니다.",
        ParagraphStyle("wfcap", parent=S["caption"], alignment=TA_CENTER)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("이 책은 이 Workflow를 하나씩 완성하는 과정입니다.", S["takeaway"]))
    return story


def page_practice():
    story = []
    story.append(running_header("PART 7 · CHAPTER 17", "실습"))
    story.append(Spacer(1, 8))
    story.append(Paragraph("실습 17", ParagraphStyle("pnum", fontName="NotoKR-Bold", fontSize=9, textColor=NAVY_SOFT)))
    story.append(Paragraph("첫 AI 요청문 쓰기", S["h2"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "사람이 이미 판단을 끝낸 반복 하나를 골라, 결과를 원문과 쉽게 비교할 수 있는 "
        "작은 일부터 시작합니다.", S["lead"]))
    story.append(Spacer(1, 10))

    step1 = step_badge_row(1, "사람이 먼저 확정한 내용을 적습니다", [
        Paragraph("목적 · 대상 · 반드시 유지할 사실 · 제외할 정보 · 원하는 형식", S["step_body"]),
    ])
    step2 = step_badge_row(2, "맡길 반복을 한 줄로 적습니다", [
        Paragraph("&ldquo;내가 AI에게 맡길 반복은 ______________입니다.&rdquo;", S["step_body"]),
    ])
    prompt_box = soft_card([
        Paragraph("PROMPT", ParagraphStyle("promptlabel", fontName="NotoKR-Bold", fontSize=8.6, textColor=NAVY_SOFT)),
        Spacer(1, 3),
        Paragraph(
            "아래 내용은 제가 확인한 ______________입니다.<br/>"
            "새로운 사실을 추가하지 말고 ______________ 형식으로 정리해주세요.<br/>"
            "______________은 그대로 유지하고, ______________은 포함하지 마세요.",
            S["prompt"]),
    ], pad=10, bg=WHITE, radius=10)
    prompt_box.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, SKY_LINE),
        ("ROUNDEDCORNERS", [10, 10, 10, 10]),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    step3 = step_badge_row(3, "첫 요청문을 완성합니다", [Spacer(1, 2), prompt_box])

    story.append(step1)
    story.append(step2)
    story.append(step3)

    check_items = [
        "사람의 판단이 끝난 내용이다.",
        "맡길 일이 한 가지다.",
        "학생 이름이나 개인 건강정보가 없다.",
        "새로운 사실을 만들지 말라고 적었다.",
    ]
    check_flows = [Paragraph(f"☐ {esc(c)}", S["check"]) for c in check_items]
    check_card = soft_card([Paragraph("체크리스트", S["cardlabel"]), Spacer(1, 4)] + check_flows, pad=10)
    story.append(check_card)
    story.append(Spacer(1, 8))
    story.append(pill("처음으로 반복 한 줄을 안전하게 맡겼습니다", w=CONTENT_W))
    return story


def make_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(WHITE)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFont("NotoKR", 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(PAGE_W / 2, 24, str(canvas.getPageNumber()))
    canvas.restoreState()


def build():
    doc = BaseDocTemplate(OUT, pagesize=A5,
                           leftMargin=MARGIN_X, rightMargin=MARGIN_X,
                           topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM)
    frame = Frame(MARGIN_X, MARGIN_BOTTOM, CONTENT_W, PAGE_H - MARGIN_TOP - MARGIN_BOTTOM,
                  id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="body", frames=[frame], onPage=make_page)])

    story = []
    pages = [page_howto, page_chapter_opening, page_story, page_project, page_workflow, page_practice]
    for i, fn in enumerate(pages):
        if i > 0:
            story.append(PageBreak())
        story.extend(fn())
    doc.build(story)
    print("DONE", OUT)


if __name__ == "__main__":
    build()

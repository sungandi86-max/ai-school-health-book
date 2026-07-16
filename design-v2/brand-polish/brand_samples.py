#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Book v2 Brand Polish — 대표 12페이지 샘플 빌더.
brand_build.py(강화된 스타일 함수)를 그대로 재사용하고, book-source-final.md의
실제 블록만 골라 12개 대표 페이지를 만든다. 전체 250페이지 재조판이 아니다.
"""
import os
from reportlab.lib.pagesizes import A5
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, NextPageTemplate
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

import brand_build as bb
from parser import parse

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "book-v2-brand-samples.pdf")

blocks = parse(os.path.join(BASE, "book-source-final.md"))

part_chapters = {}
cur_p = None
for b in blocks:
    if b["type"] == "part":
        cur_p = b["num"]
        part_chapters[cur_p] = []
    elif b["type"] == "chapter":
        part_chapters[cur_p].append(b["num"])


def render_blocks(idxs, in_practice=False):
    # 본문 리듬(문단 간격 차등화)이 전체 조판(full_build)과 똑같이 보이도록,
    # 연속된 "para" 블록은 개별 produce() 대신 bb.render_para_run()으로 한 번에
    # 처리한다(짧은 pivot 문장·묶음 마지막 문단 뒤에 더 넓은 간격).
    flows = []
    i0 = 0
    n = len(idxs)
    while i0 < n:
        i = idxs[i0]
        b = blocks[i]
        t = b["type"]
        if t == "para":
            run = [b]
            j0 = i0 + 1
            while j0 < n and blocks[idxs[j0]]["type"] == "para":
                run.append(blocks[idxs[j0]])
                j0 += 1
            # Round 5: 문단 1개짜리도 리듬 규칙(짧은 문장/긴 문단)을 받도록
            # 항상 render_para_run()을 거친다.
            flows.extend(bb.render_para_run(run))
            i0 = j0
            continue
        if t == "h4":
            flows.append(Paragraph(bb.esc(b["text"]), bb.S["h2"]))
        elif t == "h5":
            flows.append(Paragraph(bb.esc(b["text"]), ParagraphStyle(
                "h5tag", fontName="NotoKR-Bold", fontSize=10, textColor=bb.NAVY,
                spaceBefore=6, spaceAfter=4)))
        elif t == "hr":
            pass
        elif t in ("keep_start", "keep_end"):
            pass
        else:
            flows.extend(bb.produce(b, in_practice))
        i0 += 1
    return flows


def sample_label(tag, old_page):
    return Paragraph(f"SAMPLE · 구(舊) {old_page}페이지 상당 — {tag}",
                      ParagraphStyle("samplelabel", fontName="NotoKR-Bold", fontSize=7.6,
                                     textColor=bb.GRAY, alignment=TA_LEFT))


def build_samples():
    doc = BaseDocTemplate(OUT, pagesize=A5,
                           leftMargin=bb.MARGIN_X, rightMargin=bb.MARGIN_X,
                           topMargin=bb.MARGIN_TOP, bottomMargin=bb.MARGIN_BOTTOM)
    frame = Frame(bb.MARGIN_X, bb.MARGIN_BOTTOM, bb.CONTENT_W,
                  bb.PAGE_H - bb.MARGIN_TOP - bb.MARGIN_BOTTOM,
                  id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    def on_page(canvas, doc_):
        canvas.saveState()
        canvas.setFillColor(bb.WHITE)
        canvas.rect(0, 0, bb.PAGE_W, bb.PAGE_H, fill=1, stroke=0)
        canvas.setFont("NotoKR", 8)
        canvas.setFillColor(bb.GRAY)
        canvas.drawCentredString(bb.PAGE_W / 2, 24, str(canvas.getPageNumber()))
        canvas.restoreState()

    doc.addPageTemplates([PageTemplate(id="f", frames=[frame], onPage=on_page)])

    story = []

    def add_sample(tag, old_page, flows):
        if story:
            story.append(PageBreak())
        story.append(sample_label(tag, old_page))
        story.append(Spacer(1, 10))
        story.extend(flows)

    add_sample("차례", 2, bb.build_toc(blocks))
    add_sample("전체 Workflow", 4, bb.render_workflow_poster(blocks[1]))
    add_sample("PART 1 표지(강화판)", 5, bb.cover_part(1, "왜 보건실은 늘 바쁠까", part_chapters.get(1, [1, 2])))

    bb.BUILD_STATE["part_num"] = 1
    ch_flows = bb.cover_chapter(1, "하루 종일 바빴는데, 아침 파일은 그대로였습니다")
    ch_flows += render_blocks([5])
    add_sample("Chapter 01 오프닝 · A형(이야기형)", 6, ch_flows)

    add_sample("핵심 정리", 10, render_blocks(list(range(37, 47))))
    add_sample("실습", 12, render_blocks(list(range(59, 70)) + [71], in_practice=True))

    idxs = [73] + list(range(75, 77)) + list(range(78, 83))
    add_sample("Chapter 마무리", 13, render_blocks(idxs))

    idxs = list(range(152, 157)) + [158, 160]
    add_sample("QR · 프로젝트 완료", 21, render_blocks(idxs))

    add_sample("CASE", 28, render_blocks(list(range(218, 227))))
    add_sample("Workflow(본문 카드)", 37, render_blocks(list(range(313, 321))))
    add_sample("실제 프로젝트 화면", 47, render_blocks(list(range(393, 402))))

    idxs = [656] + list(range(658, 660)) + list(range(661, 664))
    add_sample("PART 마무리", 72, render_blocks(idxs))

    doc.build(story)
    print("DONE", OUT)


if __name__ == "__main__":
    build_samples()

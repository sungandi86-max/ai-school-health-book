from __future__ import annotations

import re
from pathlib import Path
from typing import Required, TypedDict


class Block(TypedDict, total=False):
    type: Required[str]
    text: str
    title: str
    num: int
    lines: list[str]
    items: list[str]
    rows: list[str]
    src: str
    alt: str
    anchor: str
    caption: str


_PART = re.compile(r"^##\s+PART\s+(\d+)\.\s*(.+)$")
_CHAPTER = re.compile(r"^###\s+Chapter\s+(\d+)\.\s*(.+)$")
_IMAGE = re.compile(r"^!\[([^]]*)\]\(([^)]+)\)$")
_ANCHOR = re.compile(r'^<a\s+id="([^"]+)"\s*></a>$')


def _is_boundary(line: str) -> bool:
    stripped = line.strip()
    return (
        not stripped
        or stripped.startswith("#")
        or stripped.startswith(">")
        or stripped.startswith("|")
        or stripped.startswith("- ")
        or stripped.startswith("<!--")
        or stripped == "---"
        or _IMAGE.match(stripped) is not None
        or _ANCHOR.match(stripped) is not None
    )


def _caption(line: str) -> str | None:
    stripped = line.strip()
    if len(stripped) >= 2 and stripped.startswith("*") and stripped.endswith("*"):
        return stripped[1:-1].strip()
    return None


def parse(path: str | Path) -> list[Block]:
    source = Path(path).read_text(encoding="utf-8")
    lines = source.splitlines()
    blocks: list[Block] = []
    pending_anchor = ""
    index = 0

    while index < len(lines):
        raw = lines[index]
        line = raw.strip()

        if not line:
            index += 1
            continue

        anchor_match = _ANCHOR.match(line)
        if anchor_match is not None:
            pending_anchor = anchor_match.group(1)
            index += 1
            continue

        if line == "<!-- KEEP BLOCK TOGETHER -->":
            blocks.append({"type": "keep_start"})
            index += 1
            continue
        if line == "<!-- KEEP BLOCK TOGETHER END -->":
            blocks.append({"type": "keep_end"})
            index += 1
            continue
        if line.startswith("<!--"):
            index += 1
            continue

        part_match = _PART.match(line)
        if part_match is not None:
            blocks.append(
                {"type": "part", "num": int(part_match.group(1)), "title": part_match.group(2)}
            )
            index += 1
            continue

        chapter_match = _CHAPTER.match(line)
        if chapter_match is not None:
            blocks.append(
                {
                    "type": "chapter",
                    "num": int(chapter_match.group(1)),
                    "title": chapter_match.group(2),
                }
            )
            index += 1
            continue

        if line == "## 에필로그":
            blocks.append({"type": "epilogue_head"})
            index += 1
            continue
        if line.startswith("### "):
            blocks.append({"type": "h3", "text": line[4:].strip()})
            index += 1
            continue
        if line.startswith("#### "):
            blocks.append({"type": "h4", "text": line[5:].strip()})
            index += 1
            continue
        if line.startswith("##### "):
            blocks.append({"type": "h5", "text": line[6:].strip()})
            index += 1
            continue
        if line.startswith("#"):
            blocks.append({"type": "para", "text": raw})
            index += 1
            continue

        image_match = _IMAGE.match(line)
        if image_match is not None:
            block: Block = {
                "type": "image",
                "alt": image_match.group(1),
                "src": image_match.group(2),
            }
            if pending_anchor:
                block["anchor"] = pending_anchor
                pending_anchor = ""
            caption_index = index + 1
            while caption_index < len(lines) and not lines[caption_index].strip():
                caption_index += 1
            if caption_index < len(lines):
                parsed_caption = _caption(lines[caption_index])
                if parsed_caption is not None:
                    block["caption"] = parsed_caption
                    index = caption_index
            blocks.append(block)
            index += 1
            continue

        if line.startswith(">"):
            quote_lines: list[str] = []
            while index < len(lines) and lines[index].lstrip().startswith(">"):
                quoted = lines[index].lstrip()[1:]
                quote_lines.append(quoted[1:] if quoted.startswith(" ") else quoted)
                index += 1
            blocks.append({"type": "blockquote", "lines": quote_lines})
            continue

        if line.startswith("|"):
            rows: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                rows.append(lines[index].strip())
                index += 1
            blocks.append({"type": "table", "rows": rows})
            continue

        if line.startswith("- "):
            items: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("- "):
                items.append(lines[index].strip())
                index += 1
            blocks.append({"type": "checklist", "items": items})
            continue

        if line == "---":
            blocks.append({"type": "hr"})
            index += 1
            continue

        paragraph = [raw.strip()]
        index += 1
        while index < len(lines) and not _is_boundary(lines[index]):
            paragraph.append(lines[index].strip())
            index += 1
        blocks.append({"type": "para", "text": "\n".join(paragraph)})

    return blocks


def classify_blockquote(lines: list[str]) -> tuple[str, list[str]]:
    first = next((line.strip() for line in lines if line.strip()), "").strip("*")
    if first == "프로젝트 진행 카드":
        return "progress_card", lines
    if first.startswith("CASE ·"):
        return "case", lines
    if first.startswith("Workflow ·"):
        return "workflow", lines
    if first == "주의" or first.startswith("Warning ·"):
        return "caution", lines
    if first in {"핵심 정리", "핵심 메시지"}:
        return "core_message", lines
    if first == "작은 축하":
        return "celebration", lines
    if first == "오늘 만든 프로젝트":
        return "today_made", lines
    if first.startswith("완료 ·"):
        return "done_marker", lines
    if first == "쑤캥의 한마디":
        return "author_note", lines
    if first in {"다음 Chapter Preview", "다음 PART Preview", "에필로그 Preview"}:
        return "preview", lines
    if first.startswith("QR ·"):
        return "qr", lines
    return "generic_quote", lines

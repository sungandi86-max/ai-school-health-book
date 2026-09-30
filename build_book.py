#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "Pillow==12.3.0",
#   "pypdf==6.10.0",
#   "reportlab==4.4.9",
# ]
# ///
# ─── How to run ───
# python build_book.py

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from hashlib import sha256
from pathlib import Path


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent
BASELINE = ROOT / "design-v2" / "fullbook" / "book-v3-final.pdf"
OUTPUT = ROOT / "design-v2" / "fullbook" / "book-v3-rebuild.pdf"
LAYOUT = ROOT / "design-v2" / "brand-polish" / "brand_build.py"
QR_SOURCE = ROOT / "design-v2" / "qr-resource-hub.txt"
QR_IMAGE = ROOT / "design-v2" / "qr-resource-hub.png"
RESOURCE_HUB_URL = "https://ai-school-health-resource-center.vercel.app/"
QR_IMAGE_SHA256 = "b43d271037b6228797a350ce3c3c12b3f1995d763cd367163c75e6b057b5981e"
QR_COUNT = 21
FONT_HASHES = {
    ROOT / "design-v2" / "brand-polish" / "fonts" / "NotoKR-Bold.ttf": (
        "21400876ceb902a1c416819a8efcad388fa5ec7e1e78dcad327d6c61e142f8d0"
    ),
    ROOT / "design-v2" / "brand-polish" / "fonts" / "NotoKR-Regular.ttf": (
        "3668c11c1a809e60642151672b44707af4977b437d47d33c5ca159e382f66299"
    ),
}


class BuildReproductionError(RuntimeError):
    message: str

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


def _write_qr_images(directory: Path) -> None:
    from PIL import Image

    qr_source = QR_SOURCE.read_text(encoding="utf-8").strip()
    if qr_source != RESOURCE_HUB_URL:
        raise BuildReproductionError("QR source URL differs from the verified Resource Hub URL")
    qr_hash = sha256(QR_IMAGE.read_bytes()).hexdigest()
    if qr_hash != QR_IMAGE_SHA256:
        raise BuildReproductionError(f"QR source image hash differs: {qr_hash}")
    with Image.open(QR_IMAGE) as image:
        if image.size != (350, 350):
            raise BuildReproductionError(f"Unexpected QR size: {image.size}")

    directory.mkdir(parents=True, exist_ok=True)
    for number in range(1, QR_COUNT + 1):
        shutil.copyfile(QR_IMAGE, directory / f"qr_{number:02d}.png")


def _run_layout(qr_directory: Path) -> None:
    environment = os.environ.copy()
    environment["BOOK_V3_QR_DIR"] = str(qr_directory)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.run([sys.executable, str(LAYOUT)], cwd=ROOT, env=environment, check=True)


def _validate_build_inputs() -> None:
    for path, expected_hash in FONT_HASHES.items():
        actual_hash = sha256(path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            raise BuildReproductionError(f"Font hash differs for {path}: {actual_hash}")


def _validate_output() -> None:
    from pypdf import PdfReader

    sys.path.insert(0, str(ROOT / "design-v2"))
    from parser import parse

    baseline = PdfReader(BASELINE)
    rebuilt = PdfReader(OUTPUT)
    if len(rebuilt.pages) != len(baseline.pages):
        raise BuildReproductionError(
            f"Page count differs: baseline={len(baseline.pages)}, rebuilt={len(rebuilt.pages)}"
        )
    baseline_size = baseline.pages[0].mediabox
    rebuilt_size = rebuilt.pages[0].mediabox
    if (baseline_size.width, baseline_size.height) != (rebuilt_size.width, rebuilt_size.height):
        raise BuildReproductionError("Page size differs from the v3 baseline")

    image_count = sum(len(page.images) for page in rebuilt.pages)
    qr_count = sum(
        image.image.size == (350, 350) for page in rebuilt.pages for image in page.images
    )
    if image_count != 74 or qr_count != QR_COUNT:
        raise BuildReproductionError(f"Image structure differs: images={image_count}, QR={qr_count}")

    def qr_pixel_hashes(reader: PdfReader) -> list[str]:
        return [
            sha256(image.image.convert("RGB").tobytes()).hexdigest()
            for page in reader.pages
            for image in page.images
            if image.image.size == (350, 350)
        ]

    if qr_pixel_hashes(rebuilt) != qr_pixel_hashes(baseline):
        raise BuildReproductionError("Rebuilt QR pixels differ from the v3 baseline")

    def image_pixel_hashes(reader: PdfReader) -> list[tuple[tuple[int, int], str]]:
        return [
            (image.image.size, sha256(image.image.convert("RGBA").tobytes()).hexdigest())
            for page in reader.pages
            for image in page.images
        ]

    if image_pixel_hashes(rebuilt) != image_pixel_hashes(baseline):
        raise BuildReproductionError("Embedded image pixels differ from the v3 baseline")

    def embedded_font_names(reader: PdfReader) -> set[str]:
        names: set[str] = set()
        for page in reader.pages:
            resources = page.get("/Resources")
            if resources is None or resources.get("/Font") is None:
                continue
            for reference in resources["/Font"].values():
                font = reference.get_object()
                names.add(str(font.get("/BaseFont")))
        return names

    if embedded_font_names(rebuilt) != embedded_font_names(baseline):
        raise BuildReproductionError("Embedded font names differ from the v3 baseline")

    baseline_texts = [page.extract_text() or "" for page in baseline.pages]
    rebuilt_texts = [page.extract_text() or "" for page in rebuilt.pages]
    def normalize(text: str) -> str:
        return "\n".join(line.rstrip() for line in text.replace("\r", "").splitlines())
    normalized_baseline = [normalize(text) for text in baseline_texts]
    normalized_rebuilt = [normalize(text) for text in rebuilt_texts]
    blank_pages = [
        number
        for number, page in enumerate(rebuilt.pages, start=1)
        if not rebuilt_texts[number - 1].strip() and not page.images
    ]
    if blank_pages:
        raise BuildReproductionError(f"Blank pages found: {blank_pages}")
    differing_pages = [
        number
        for number, pair in enumerate(zip(normalized_baseline, normalized_rebuilt), start=1)
        if pair[0] != pair[1]
    ]
    if differing_pages:
        raise BuildReproductionError(f"Extracted text differs on pages: {differing_pages}")

    page_number_errors = []
    for number, text in enumerate(rebuilt_texts, start=1):
        lines = {line.strip() for line in text.splitlines() if line.strip()}
        if str(number) not in lines:
            page_number_errors.append(number)
    if page_number_errors:
        raise BuildReproductionError(f"Missing printed page numbers: {page_number_errors}")

    def cover_positions(texts: list[str]) -> tuple[list[int], list[int], list[int]]:
        part_pages: list[int] = []
        chapter_pages: list[int] = []
        epilogue_pages: list[int] = []
        for number, text in enumerate(texts, start=1):
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            if not lines or lines[0] != str(number):
                continue
            if (
                len(lines) > 2
                and len(lines[1]) == 2
                and lines[1].isdigit()
                and lines[2].replace(" ", "").startswith("PART")
            ):
                part_pages.append(number)
            if len(lines) > 1 and lines[1].startswith("PART ") and " · CHAPTER " in lines[1]:
                chapter_pages.append(number)
            if "E P I L O G U E" in lines[:5]:
                epilogue_pages.append(number)
        return part_pages, chapter_pages, epilogue_pages

    baseline_covers = cover_positions(baseline_texts)
    rebuilt_covers = cover_positions(rebuilt_texts)
    if rebuilt_covers != baseline_covers or tuple(map(len, rebuilt_covers)) != (8, 22, 1):
        raise BuildReproductionError(f"Cover positions differ: {rebuilt_covers}")

    blocks = parse(ROOT / "book-source" / "book-source-final.md")
    table_count = sum(block["type"] == "table" for block in blocks)
    if table_count != 63:
        raise BuildReproductionError(f"Parsed table count differs: {table_count}")

    text_hash = sha256("\f".join(normalized_rebuilt).encode("utf-8")).hexdigest()
    print(
        "VALIDATED "
        f"pages={len(rebuilt.pages)} text_lines={sum(len(text.splitlines()) for text in rebuilt_texts)} "
        f"images={image_count} qr={qr_count} tables={table_count} text_sha256={text_hash}"
    )
    print(f"PART_COVERS {rebuilt_covers[0]}")
    print(f"CHAPTER_COVERS {rebuilt_covers[1]}")
    print(f"EPILOGUE_COVER {rebuilt_covers[2]}")


def main() -> int:
    if not BASELINE.is_file():
        raise FileNotFoundError(BASELINE)
    if OUTPUT.resolve() == BASELINE.resolve():
        raise BuildReproductionError("Rebuild output must not overwrite the v3 baseline")
    if OUTPUT.exists() and os.path.samefile(OUTPUT, BASELINE):
        raise BuildReproductionError("Rebuild output aliases the protected v3 baseline")
    _validate_build_inputs()
    if OUTPUT.exists():
        OUTPUT.unlink()

    with tempfile.TemporaryDirectory(prefix="book-v3-build-") as temporary:
        qr_directory = Path(temporary) / "qr"
        _write_qr_images(qr_directory)
        _run_layout(qr_directory)
    _validate_output()
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

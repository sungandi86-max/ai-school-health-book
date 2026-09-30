# v3 PDF Build Reproduction

## Build Entry Point

Verified single command on Windows/Codex:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\build_book.ps1
```

Portable fresh clone with `uv`:

```bash
uv run build_book.py
```

Python with the pinned dependencies already installed:

```bash
python build_book.py
```

`build_book.py` contains PEP 723 metadata pinning Python 3.11 or later, Pillow 12.3.0,
pypdf 6.10.0, and ReportLab 4.4.9.

## Source of Truth

The manuscript source of truth is:

```text
book-source/book-source-final.md
```

The build reads this file without modifying or copying it into the layout directory.

## Build Inputs

- Manuscript: `book-source/book-source-final.md`
- Images: `assets/*.png`
- QR target URL: `design-v2/qr-resource-hub.txt`
- Restored QR raster: `design-v2/qr-resource-hub.png`
- Fonts: `design-v2/brand-polish/fonts/NotoKR-Regular.ttf` and
  `design-v2/brand-polish/fonts/NotoKR-Bold.ttf`
- Layout: `design-v2/brand-polish/brand_build.py`
- Parser: `design-v2/parser.py`
- Protected comparison baseline: `design-v2/fullbook/book-v3-final.pdf`

The font files in `design-v2/brand-polish/fonts/` are explicitly retained because their
SHA-256 values match the font set selected by the v3 layout code. The other font subsets
under `design-v2/fonts/` and `design-v2/fullbook/fonts/` are not build inputs.

The QR URL is the Resource Hub URL recorded in the existing release and QA documents:

```text
https://ai-school-health-resource-center.vercel.app/
```

All 21 QR image references in the v3 PDF use the same restored 350 by 350 pixel raster.
The build copies that raster to the numbered temporary inputs expected by the legacy
layout code. It does not generate or substitute a new URL.

## Build Pipeline

1. `build_book.py` validates the protected baseline and fixed input paths.
2. It creates a temporary QR directory and prepares `qr_01.png` through `qr_21.png`.
3. `design-v2/parser.py` parses the source Markdown into the legacy block contract.
4. `design-v2/brand-polish/brand_build.py` renders those blocks with ReportLab.
5. The generated PDF is written to `design-v2/fullbook/book-v3-rebuild.pdf`.
6. The entry point compares the rebuilt PDF with the protected v3 baseline.
7. Temporary QR inputs are removed automatically.

No HTML, CSS, browser, or manual source-copy stage is used.

`design-v2/fullbook/full_build.py`, `design-v2/design_v2.py`, and
`design-v2/brand-polish/brand_samples.py` are retained historical v2/sample builders.
They are not invoked by the v3 reproduction entry point and are not supported build
commands for this task.

## Parser

`design-v2/parser.py` was reconstructed from the block fields consumed by
`brand_build.py` and `full_build.py`, the final Markdown structure, the Chapter template,
and the existing QA counts.

It emits only the legacy block types required by the layout:

```text
part, chapter, epilogue_head, h3, h4, h5, para, checklist, table,
image, hr, blockquote, keep_start, keep_end
```

The parser restores the existing blockquote classifications used by the layout:
progress card, CASE, Workflow, caution, core message, celebration, completed marker,
today's project, author note, preview, QR, and generic quote. Prompt detection remains in
the unchanged builder-side heuristic.

The parsed manuscript contains 8 PART blocks, 22 Chapter blocks, 63 tables, 9 images,
21 QR blocks, 20 CASE blocks, and 16 Workflow blocks. No manuscript text or heading is
rewritten by the parser.

## Output

The build creates:

```text
design-v2/fullbook/book-v3-rebuild.pdf
```

It never writes to or replaces:

```text
design-v2/fullbook/book-v3-final.pdf
```

## Validation

Verified on 2026-09-30 with the documented entry point:

- Pages: 288 / 288
- Page size: 419.5276 by 595.2756 pt / identical
- Extracted text lines: 5,110 / 5,110
- Normalized full-text SHA-256: identical
  `b22d31f117c15ec260588c672aa789b3d6247026bdcc7e7363bb46b30b9628f8`
- Text-different pages: 0
- PART cover pages: identical at 5, 25, 48, 81, 119, 157, 194, 231
- Chapter cover pages: identical at 6, 15, 26, 36, 49, 58, 70, 82, 95, 106,
  122, 133, 144, 159, 169, 179, 197, 207, 218, 234, 246, 257
- Epilogue cover: identical at page 273
- Printed page numbers: present for 1 through 288
- Image references: 74 / 74
- QR references: 21 / 21
- QR source SHA-256 and all 21 embedded QR pixel hashes: identical to the protected v3
- Parsed tables: 63
- Embedded font names: identical
- Brand-polish font file SHA-256 values: pinned and verified before rendering
- Embedded image pixel hashes: identical for all 74 image references
- Fully blank pages: 0
- Representative 144 dpi raster comparison: pages 1, 4, 23, 78, 189, 273,
  and 288 were pixel-identical
- Manual visual inspection: QR page 23, app-screen page 189, and epilogue page 273
  rendered without clipping, overlap, broken glyphs, or layout drift

### Manual QA Matrix

| Scenario | Surface | Evidence | Result |
|---|---|---|---|
| Single-command rebuild | PowerShell CLI | `powershell -NoProfile -ExecutionPolicy Bypass -File .\build_book.ps1`, exit 0 | PASS |
| Protected output | Filesystem and SHA-256 | Baseline stayed at `dd459539...a64f1f8`; rebuild used a separate path | PASS |
| Full PDF structure | pypdf over all 288 pages | Page size, 5,110 text lines, 74 images, 21 QR references, 63 parsed tables | PASS |
| Text and pagination | pypdf over all 288 pages | Zero text-different pages; identical PART, Chapter, and epilogue cover positions | PASS |
| Image and font fidelity | pypdf image/font traversal | All embedded image pixels and font names equal the baseline | PASS |
| Representative visual rendering | 144 dpi Poppler render | Pages 1, 4, 23, 78, 189, 273, and 288 were pixel-identical | PASS |
| Manual visual inspection | Rendered PNG inspection | Pages 23, 189, and 273 showed no clipping, overlap, broken glyphs, or drift | PASS |

## Differences From Existing v3

The PDFs are not byte-identical:

- Existing v3: 4,261,066 bytes,
  SHA-256 `dd459539d2e9a69ccd13a224e22a25c4c0a7ddacd717a272e7d10e016a64f1f8`
- Verified rebuild size: 4,261,110 bytes

The 44-byte difference is PDF serialization metadata, including the new creation time.
The rebuilt file SHA-256 changes when that creation time changes, so it is not used as a
reproduction criterion.
No structural, extracted-text, font-name, page-position, image-count, or tested raster
difference remains.

## Reproduction Status

REPRODUCIBLE

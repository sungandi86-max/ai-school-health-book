# Release Notes — v1.0.0

**출간일**: 2026-07-16
**도서명**: 『보건교사를 위한 AI 업무 자동화』

## 개요

보건교사가 반복되는 업무 하나를 관찰하고, 작게 나누고, AI에게 맡길 부분과 사람이 끝까지 판단해야 할 부분을 구분해가는 8개 PART · 22개 Chapter 프로젝트북의 첫 출간 버전입니다.

## 구성

- PART 1~8, Chapter 01~22, 에필로그로 구성된 원고 (`book-source/book-source-final.md`)
- 실제 프로젝트 화면 이미지 9종
- Chapter 02~22에 QR 코드 21개 — 스캔 시 Resource Hub(자료실) 랜딩 페이지로 연결
- A5 판형 최종 조판 PDF, 총 255페이지 (`pdf/book-final-pass2.pdf`)

## 이번 버전에서 확정된 사항

- 원고는 병합·QA를 마친 Single Source of Truth 상태로 고정되었습니다.
- QR 코드는 모두 동일한 정책 문구를 사용하며, 실제 Resource Hub 주소(`https://ai-school-health-resource-center.vercel.app/`)로 연결됩니다.
- PDF는 페이지 단위 전수 검수를 거쳐 발견된 조판 결함(54페이지 고아 문장) 1건을 수정 완료했습니다.
- 페이지 구조, 반복 컴포넌트(진행 카드·CASE·Workflow·표·이미지·QR) 배치, 폰트 임베딩, 문서 구조 모두 검증을 마쳤습니다.

## 알려진 제한 사항

- 본문에 사용된 서체는 원본 지정 서체(Noto Sans KR Thin)와 완전히 동일하지 않은 대체 서체(Noto Sans CJK KR 서브셋)를 사용했습니다. 시각적으로 유사하나 완전히 동일하지는 않습니다.

## 관련 문서

- [`CHANGELOG.md`](./CHANGELOG.md) — 버전별 변경 이력
- [`release/RELEASE_CHECKLIST.md`](./release/RELEASE_CHECKLIST.md) — 출간 전 최종 점검 결과
- [`release/PDF_FINAL_QA_PASS2.md`](./release/PDF_FINAL_QA_PASS2.md) — PDF 페이지 단위 전수 검수 보고서
- [`release/RELEASE_DESCRIPTION.md`](./release/RELEASE_DESCRIPTION.md) — GitHub Release 본문

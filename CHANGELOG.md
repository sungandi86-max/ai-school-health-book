# Changelog

이 저장소의 주요 변경 사항을 기록합니다. 형식은 [Keep a Changelog](https://keepachangelog.com/ko/1.0.0/)를 참고합니다.

## [1.0.0] - 2026-07-16

『보건교사를 위한 AI 업무 자동화』 첫 출간 버전.

### Added
- `book-source/book-source-final.md`: PART 1~8, Chapter 01~22, 에필로그 원고를 하나로 병합한 Single Source of Truth 추가
- 실제 프로젝트 화면 이미지 9종(IMG-001~IMG-009) 및 캡션 삽입
- `README.md`: 저장소 구조 및 작업 순서 안내 문서 추가
- `pdf/book-final-pass2.pdf`: A5 판형 최종 조판 PDF(255페이지) 추가
- `release/PDF_FINAL_QA_PASS2.md`: PDF 페이지 단위 전수 검수 보고서 추가

### Changed
- Chapter 02~22의 QR 코드 안내 문구 21건을 Resource Hub(자료실) 정책에 맞춰 통일된 템플릿으로 표준화
- QR 코드가 가리키는 대상 URL을 실제 Resource Hub 주소(`https://ai-school-health-resource-center.vercel.app/`)로 확정

### Fixed
- 54페이지에서 발생한 고아 문장(단독으로 남은 한 줄) 조판 결함 수정 — 본문 3개 문단을 하나의 단위로 묶어 자연스럽게 배치, 페이지 수(255)와 Chapter 06 시작 위치(55페이지)는 변경 없음

### Verified
- 원고 구조 QA: 제목 계층, PART/Chapter/실습/에필로그 완결성, 이미지 배치, Markdown 오류, 조판 앵커, 임시 문구 잔존 여부 — 전항목 이상 없음
- PDF QA: 페이지 연속성, 제목 줄바꿈, 반복 컴포넌트(진행 카드·CASE·Workflow·QR·표·이미지 등) 페이지 분리, QR 21개 디코딩(100% 목표 URL 일치), 폰트 임베딩, PDF 구조(qpdf 검증) — 전항목 이상 없음

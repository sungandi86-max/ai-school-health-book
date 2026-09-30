# AI 전자책 프로젝트 인수인계

기준일: 2026-10-01

## Current Status

- 기준 PDF: `design-v2/fullbook/book-v3-final.pdf`
- 기준 PDF 분량: 288쪽
- 빌드 재현 상태: `REPRODUCIBLE`
- 새 리디자인 초안: `book-source/book-source-redesign-draft.md`
- 새 원고 구조: 8 PART / 22 Chapter / 에필로그
- 기존 기준 원고와 기준 PDF는 보호 대상이며 수정하지 않는다.

## Current Direction

1. 보건교사의 바쁨을 AI 기능이 아니라 반복되는 실제 행동에서 발견한다.
2. 화면보다 먼저 사용자, 상태, 정보, 다음 행동을 설계한다.
3. 앱은 제품 소개가 아니라 구조화된 업무가 실제 운영으로 발전한 증거다.
4. AI에는 판단이 끝난 반복만 맡기고 개인정보와 최종 승인은 사람이 지킨다.
5. 독자는 마지막에 프롬프트가 아니라 자기 업무를 바꿀 설계 문서를 가져간다.

## Core App Cases

- 온라인 보건실
- 별도검사 도우미
- BOGUNON
- BOGUNON DESK

앱 기능은 전자책의 과거 설명이나 계획이 아니라 각 앱 저장소의 현재 구현을 기준으로 확인한다.

## Author Interview Status

- 온라인 보건실: 완료
- 별도검사 도우미: 완료. 단, 실제 검사 당일 사용 전이며 AI 시뮬레이션까지만 진행했다.
- BOGUNON: 완료
- BOGUNON DESK Chapter 20: 완료
- BOGUNON DESK Chapter 21: `PENDING — AFTER FEATURE FREEZE`

남은 Chapter 21 입력:

- DESK 기능 동결 버전
- 실제 설치본 기준 QA
- 실제 완주 가능한 업무 흐름
- 사용 순서와 결과 확인 방법
- 기존 방식과 달라진 행동
- 남은 문제
- 최종 출판용 mock 캡처

## Screenshot Status

- 온라인 보건실: 준비 가능. 최신 Firebase v2와 mock 데이터를 우선한다.
- 별도검사 도우미: 준비 가능. 설계된 운영 시나리오이며 실제 현장 검증 전이라고 명시한다.
- BOGUNON: 현재 구현된 기능 기준으로 준비 가능하다.
- BOGUNON DESK: `PENDING — AFTER FEATURE FREEZE`

모든 출판 화면은 실제 운영 구조를 유지하되 학교명, 학생, 교직원, 연락처, 건강정보와 계정 정보를 mock 데이터로 교체한다.

## Next Work

우선순위:

1. 이번 주 BOGUNON DESK 개발 마무리
2. `school-health-desk` 기능 동결
3. 실제 설치본 QA
4. Author Input 7 작성
5. DESK 출판용 mock 화면 캡처
6. 온라인 보건실 mock 캡처
7. 별도검사 도우미 mock 캡처
8. BOGUNON mock 캡처
9. 새 원고 전체 편집
10. PDF 조판
11. 최종 QA
12. 출간

## Build

Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\build_book.ps1
```

`uv` 사용 시:

```bash
uv run build_book.py
```

빌드 결과는 `design-v2/fullbook/book-v3-rebuild.pdf`에 생성되며 Git 추적 대상이 아니다. 기준본 `design-v2/fullbook/book-v3-final.pdf`를 덮어쓰지 않는다.

## Important Files

- `book-source/book-source-final.md`
  기존 기준 원고. 수정 금지.

- `book-source/book-source-redesign-draft.md`
  현재 리디자인 작업 원고.

- `NEW_TOC.md`
  확정에 가까운 새 목차.

- `APP_REPOSITORY_AUDIT.md`
  앱 저장소 구현 사실 감사.

- `SCREENSHOT_PLAN.md`
  출판 화면과 mock 데이터 계획.

- `REDESIGN_DRAFT_REPORT.md`
  현재 리디자인 상태와 남은 위험.

- `BUILD_REPRODUCTION.md`
  기존 v3 빌드 재현 방법과 검증 결과.

## Important Rules

- 실제 개인정보를 책에 넣지 않는다.
- 모든 출판용 화면은 mock 데이터를 사용한다.
- 별도검사 도우미는 아직 실제 현장 검증 전이라고 명시한다.
- BOGUNON DESK는 기능 동결 후 실제 구현되고 검증된 기능만 책에 넣는다.
- `School Health Hub` 명칭은 책에서 사용하지 않는다.
- 앱 기능은 실제 저장소의 현재 구현을 기준으로 한다.
- 미구현 기능을 사실형으로 쓰지 않는다.
- `book-source/book-source-final.md`와 `design-v2/fullbook/book-v3-final.pdf`는 보호한다.
- 기존 `release/`, `pdf/`, `assets/`를 리디자인 작업 중 임의로 수정하지 않는다.

## Resume At School

새로 받는 경우:

```bash
git clone https://github.com/sungandi86-max/ai-school-health-book.git
cd ai-school-health-book
```

이미 clone되어 있다면:

```bash
git switch main
git pull origin main
```

그 다음 아래 순서로 확인한다.

1. `PROJECT_HANDOFF.md`
2. `book-source/book-source-redesign-draft.md`
3. `SCREENSHOT_PLAN.md`
4. `REDESIGN_DRAFT_REPORT.md`

학교에서 가장 먼저 이어서 할 일은 BOGUNON DESK 기능 동결과 실제 설치본 QA다. 그 결과로 Chapter 21의 pending 입력과 최종 출판용 mock 캡처 범위를 확정한다.

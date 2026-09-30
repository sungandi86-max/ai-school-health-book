# 리디자인 통합 초안 보고서

## Summary

- 기존 8 PART·22 Chapter 리듬을 유지하면서 흐름을 `문제 발견 → 분해 → 구조화 → 첫 시스템 → 흐름 관리 → AI 보조 → 통합 → 나만의 업무환경`으로 재구성했다.
- 기존 원고의 현장 장면, 실패 기록, 표·Workflow·실습 구조를 살리고 일반적인 AI 설명과 도구 중심 서술을 압축했다.
- 네 앱의 현재 로컬 저장소를 직접 확인해 구현 사실을 본문에 반영했다.
- 2026-10-01까지 확인한 저자 인터뷰 6건을 반영해 앱의 개발 배경과 실제 운영 경험을 보강했다.
- BOGUNON DESK Chapter 21은 설치·테스트 단계이므로 `[AUTHOR INPUT PENDING — AFTER FEATURE FREEZE]`로 보류했다.
- 실제 개인정보를 추가하지 않았으며 모든 출판 화면은 mock 데이터 기반으로 계획했다.

## New Draft Path

- `book-source/book-source-redesign-draft.md`
- 구조: PART 8개, Chapter 22개, 에필로그 1개
- 에필로그 가제: `반복은 줄이고, 판단은 남기다`

## Repository Evidence Used

### 전자책

- repository: `C:/Users/보건실/OneDrive/문서/GitHub/ai-school-health-book`
- branch: `main`
- HEAD: `fe25739fce351b60463eacb1c877d66f0dba664c`
- 확인 경로: `book-source/book-source-final.md`, `NEW_TOC.md`, `CURRENT_BOOK_AUDIT.md`, `CONTENT_MIGRATION_MAP.md`, `NEW_BOOK_CONCEPT.md`, `APP_CASE_STUDY_PLAN.md`, `VISUAL_EDITORIAL_SYSTEM.md`, `LENGTH_PLAN.md`, `REDESIGN_EXECUTION_PLAN.md`
- 기준 PDF와 재현 빌드 파일은 수정하지 않았다.

### 온라인 보건실

- repository: `C:/Users/보건실/OneDrive/문서/GitHub/sehwa-health-portal`
- branch: `main`
- HEAD: `7685aae6b6959321708afd06853433e6785f8374`
- 주요 근거: `src/App.jsx`, `src/data/fallbackData.js`, `src/data/firebaseV2Navigation.js`, `src/components/FirebaseSignInActions.jsx`, `firestore.rules`, `docs/PORTAL_UI_GOVERNANCE.md`

### 별도검사 도우미

- repository: `C:/Users/보건실/OneDrive/문서/GitHub/school-health-check-scheduler`
- branch: `master`
- HEAD: `7cdda888413e6f8289e56618223b230ebad34b7e`
- 주요 근거: `src/App.tsx`, `src/types/healthCheck.ts`, `src/lib/operation.ts`, 운영 센터·교사용·관리자·현황판·보고서 component, `ACCESS_MATRIX.md`, `PROJECT.md`, `schema.sql`

### BOGUNON

- repository: `C:/Users/보건실/OneDrive/문서/GitHub/bogunon`
- branch: `main`
- HEAD: `bfdc46e991f79ed34ba6805c513151d344daa83a`
- 주요 근거: briefing, calendar, tasks, event-health-support, staff-contacts route/component와 행사·연락처 migration

### BOGUNON DESK

- repository: `C:/Users/보건실/OneDrive/문서/GitHub/school-health-desk`
- branch: `main`
- HEAD: `7fa8988750f008f6ea2c736df17f616ada076626`
- 주요 근거: `src/App.tsx`, `DashboardCanvas.tsx`, widget/tool registry, 공문 작업공간, BOGUNON workspace·auth 코드, `src-tauri/tauri.conf.json`, `src-tauri/Cargo.toml`, `package.json`

찾지 못한 핵심 저장소는 없다.

## Reused Content

### 거의 그대로 사용

- 기존 Chapter 01의 중단·재시작 장면과 하루 한 장면 기록 방식
- 기존 Chapter 02의 반복 행동 관찰과 개인정보 없는 기록 원칙
- 기존 Chapter 15의 같은 정보 다시 적지 않기 원리
- 기존 Chapter 22의 독자 적용 질문과 운영 기준 철학

### 편집 후 사용

- 기존 Chapter 03·18의 사람 판단과 개인정보 경계를 Chapter 04로 통합
- 기존 Chapter 04의 작은 첫 과제 선정을 Chapter 03으로 이동
- 기존 Chapter 05~07의 화면 우선 실패와 사용자 흐름을 온라인 보건실 사례로 재구성
- 기존 Chapter 08~14의 동사 분해, 상태, 행·열, 최소 필드를 PART 3과 앱 사례 전반에 분산
- 기존 Chapter 17~19의 AI 활용을 Chapter 15~16의 `중복 제거 → 반복 한 칸 → 사람 승인` 흐름으로 압축
- 기존 Chapter 20~21의 실제 사용·공동 운영 원리를 각 앱의 운영 기록에 재배치

## Compressed Content

- 일반 AI 개론과 도구별 기능 설명
- 범용 프롬프트 공식
- 일반적인 개발 단계 설명
- 보건교사 업무와 연결되지 않는 추상 Workflow
- 화면·앱 이름만 나열하는 기능 소개
- 같은 의미의 표·체크리스트 반복

## Removed / Deferred Content

- 저장소에서 확인되지 않는 앱 기능과 미래 계획
- 측정되지 않은 시간 절감·만족도·오류 감소 효과
- 별도검사 도우미의 여섯 표현을 하나의 통합 상태 머신으로 설명하는 기존 계획
- 온라인 보건실의 Firebase v2 전환이 완료됐다는 표현
- BOGUNON migration이 운영 DB에 모두 적용됐다는 표현
- BOGUNON DESK의 과거 mock UI, OCR·레거시 HWP·문서 이력 등 미완성 기능
- BOGUNON DESK의 기능 동결 전 실사용 검증과 최종 화면은 보류

## New Writing Added

- PART 3 앞의 `이제 화면이 아니라 업무 설계도를 만듭니다` 브리지
- 앱 저장소의 실제 route·상태·schema를 설명하는 사실 기반 문단
- 각 앱의 `기존 방식 → 문제 → 구조화 → 설계 → 화면 → 실제 사용 → 변화 → 한계` 골격
- 출판용 screenshot placeholder와 mock·개인정보 조건
- Chapter 15~16의 `같은 정보 다시 적지 않기 → 판단이 끝난 반복 한 칸 → 사람 확인·승인` 흐름
- Chapter 22의 다섯 최종 결과물 전체 양식

## Implemented Features Used in Book

### 온라인 보건실

- 오늘의 보건실, 제출·업로드, 검진·검사, 교육자료, 담임 협조, 학생 건강관리, FAQ route
- Firebase v2 제출·검진·교육·FAQ·관리 화면
- Microsoft Teams·Google 로그인 UI
- `staff`, `homeroom`, `health_teacher`, `admin` 역할과 Firestore rules

### 별도검사 도우미

- 세션·검사 종류·대상 학급·명단·조건·시간표
- 운영 센터, 교사용 화면, 관리자 화면, 가로형 현황판, 운영 보고서
- 학급 상태, 지연 분 값, 학생 상태를 나눈 실제 데이터 구조
- sample CSV와 mock QA 데이터

### BOGUNON

- 통합 홈, 월·주·일 캘린더, 업무 상태·검색·반복
- 행사 보건지원 정보와 준비물 체크리스트
- 학기별 교직원 배정, 연락처·그룹·즐겨찾기와 파일 가져오기
- Google OAuth와 user-scoped RLS를 위한 코드·migration

### BOGUNON DESK

- `DashboardCanvas` 기반 사용자 조정형 Windows 업무 데스크
- 위젯·Dock·명령 팔레트·검색
- BOGUNON 계정 연결, 빠른 추가, 업무 완료와 검색
- 업무 폴더, 빠른 메모, 계산기, 구매 도우미, 공문 작업공간
- 개인정보 사전 점검과 AI 전송 내용 확인
- DPAPI, CSP, 로컬 파일 처리, tray·자동 시작·알림·deep link·설치·자동 업데이트 코드

## Partial Features Excluded

### 온라인 보건실

- legacy와 Firebase v2가 공존하므로 완전 전환으로 서술하지 않았다.
- 모든 운영 계정에서 권한 검증이 완료됐다고 쓰지 않았다.

### 별도검사 도우미

- QR 토큰 검증, 만료·폐기·접근 로그, 완성된 인증·RoleGuard·Supabase RLS를 제외했다.
- Early Access 준비를 실제 학교 운영 완료로 서술하지 않았다.

### BOGUNON

- 실제 배포 DB migration 적용 여부와 현재 사용 빈도를 제외했다.
- 통합 홈에서 직접 표시되지 않는 업무 데이터를 홈 기능으로 주장하지 않았다.

### BOGUNON DESK

- 외부 링크 기능을 내부 구현으로 설명하지 않았다.
- OCR, 레거시 HWP, 문서 이력과 과거 mock UI를 제외했다.
- 0.2.0 구현을 실제 사용자 설치·운영 검증 완료로 확대하지 않았다.

## Author Interview Status

### 온라인 보건실

- 완료: 온라인 교무실 연수에서 시작한 첫 구현과 화면 중심 접근의 실패 경험 반영
- 완료: 담임교사의 월별 입실 현황 확인, 학년별 비밀번호 운영 부담, Firebase·Teams 계정·학기별 권한 전환 반영
- 현재 한계: Apps Script에서 Firebase v2로 완전히 이전되지 않은 기능이 남아 있음

### 별도검사 도우미

- 완료: 고교학점제 이동수업, 학생 위치 파악, 보건교사 문의 집중이라는 현장 배경 반영
- 완료: 지연·확인필요의 설계 의미와 AI 시뮬레이션 범위 반영
- 명시: 실제 검사 당일 사용 전이며, 다음 검사를 위한 첫 번째 가설임

### BOGUNON

- 완료: 다이어리·휴대폰 캘린더·Google Sheets·Excel에 흩어진 기존 관리 방식 반영
- 완료: 일정관리, 연간계획과 실무일정 연결, 보건지원강사 관리, 기존 도구 연결 방식 반영
- 현재 한계: 연락처 영역은 아직 덜 다듬어진 상태

### BOGUNON DESK

- Chapter 20 완료: 파일·공문·품의 작성의 반복, BOGUNON 연결 원칙, Windows 자동 실행 방향 반영
- Chapter 21: `PENDING — AFTER FEATURE FREEZE`
- 남은 입력: 기능 동결 버전, 실제 설치본 QA, 완주 가능한 업무 흐름, 사용 순서, 결과 확인, 달라진 행동, 남은 문제, 최종 mock 캡처

### Count

- 해결된 AUTHOR INPUT: 6
- 남은 일반 `[AUTHOR INPUT REQUIRED]`: 0
- `[AUTHOR INPUT PENDING — AFTER FEATURE FREEZE]`: 1

## Screenshot Placeholders

- 총 18개
- 온라인 보건실 4개
- 별도검사 도우미 5개
- BOGUNON 4개
- BOGUNON DESK 5개
- 온라인 보건실은 최신 Firebase v2를 우선해 mock 캡처를 준비할 수 있다. Apps Script 화면은 변화 비교가 필요할 때만 사용한다.
- 별도검사 도우미는 mock 운영 시나리오로 캡처할 수 있으나 실제 검사에서 검증된 결과처럼 설명하지 않는다.
- BOGUNON은 현재 구현 기능 기준으로 mock 캡처를 준비할 수 있다.
- BOGUNON DESK 5개는 `PENDING — AFTER FEATURE FREEZE`이며 이번 주 기능 동결 후 다시 확인한다.

## Workbook Elements

- Chapter 01: 하루 한 장면 해부표
- Chapter 02: 반복 업무 지도
- Chapter 03: 첫 개선 과제 선정표
- Chapter 04: 사람·시스템·정보 경계표
- Chapter 05~07: 업무 분해표, 상태 기준표, 업무 설계표와 mock 데이터
- Chapter 08~11: 실패 기록, 포털 정보 구조, 사용자 흐름, 운영 기록
- Chapter 12~14: 대상별 상태 정의, 역할 매트릭스, 예외 처리와 운영 기록
- Chapter 15~16: 중복 제거표, 사람·AI·재확인 역할표
- Chapter 17~21: 앱별 문제 지도, 기능 매핑, 운영 기록, 사실·추정 구분표
- Chapter 22: 업무 문제 지도, 사용자 흐름, 상태·정보 설계표, 도구 기획서, 운영 체크리스트

## Estimated Content Balance

첫 통합 초안의 서술 단위 기준 추정:

- 기존 원고의 장면·원리·표·실습 재사용 및 편집: 약 45%
- 앱 저장소 근거와 저자 인터뷰를 바탕으로 한 신규 작성: 약 45%
- 기능 동결 후 입력 및 screenshot placeholder: 약 10%

페이지 목표는 기존 계획의 270~315쪽을 유지한다. 일반론을 줄인 분량을 앱 사례와 화면에 배정하되, DESK 기능 동결과 실제 캡처가 끝난 뒤 조판 기준으로 다시 계산해야 한다.

## Risks Before Final Writing

- 온라인 보건실 캡처에서 Apps Script와 Firebase v2 화면을 섞으면 현재 운영 구조가 불명확해질 수 있다.
- 별도검사 도우미의 부분 구현된 접근 제어를 운영 보안 완료로 오해할 위험이 있다.
- 별도검사 도우미를 실제 검사 당일 검증된 시스템처럼 서술하면 안 된다.
- BOGUNON 연락처 영역은 아직 덜 다듬어진 상태임을 캡처와 본문에 반영해야 한다.
- BOGUNON DESK는 기능 동결 전 UI 변경 가능성이 있어 최종 캡처를 서두르면 안 된다.
- 기존 저장소들의 dirty/untracked 파일은 이번 작업과 무관하며 건드리지 않았다.

## Recommended Next Step

1. 이번 주 BOGUNON DESK 개발을 마무리하고 `school-health-desk` 기능을 동결한다.
2. 실제 설치본으로 완주 가능한 업무 흐름을 QA하고 Chapter 21의 pending 입력을 작성한다.
3. DESK 출판용 mock 화면을 캡처한다.
4. 온라인 보건실, 별도검사 도우미, BOGUNON의 mock 화면을 순서대로 캡처하고 개인정보를 검수한다.
5. 초안의 사실 문장과 실제 화면을 대조해 전체 원고를 편집한 뒤 조판·최종 QA로 이동한다.

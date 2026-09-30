# 앱 저장소 구현 상태 감사

감사 기준일: 2026-09-30
판정 원칙: README나 과거 기획보다 현재 브랜치의 route, component, schema/migration, 설정 파일을 우선한다. `IMPLEMENTED`는 코드와 화면이 존재한다는 뜻이며, 실제 학교 운영 성과까지 증명한다는 뜻은 아니다.

## 온라인 보건실

- repository path: `C:/Users/보건실/OneDrive/문서/GitHub/sehwa-health-portal`
- branch: `main`
- HEAD commit: `7685aae6b6959321708afd06853433e6785f8374`
- git status: `.claude/`, `.omo/`, `apps-script/Code.full-paste.gs`가 추적되지 않은 상태다. 이번 작업에서는 변경하지 않았다.
- 프로젝트 구성: Vite, React 18, Tailwind CSS, Firebase/Firestore. 기존 Google Sheets·Apps Script 기반 화면과 Firebase v2 화면이 함께 존재한다.
- 최근 변경 근거: 완료 제출 숨김, 교직원 식별자 자동 연결, 관리자 대시보드 계층 개선이 최근 커밋에 포함돼 있다.

### 주요 메뉴와 현재 화면

- 기존 포털: `/`, `/today`, `/upload`, `/checkup`, `/education`, `/homeroom`, `/student-care`, `/resources`, `/faq`
- Firebase v2: `/firebase-dashboard`, `/firebase-checkups`, `/firebase-education`, `/firebase-faq`, `/firebase-submissions`
- 관리자: 접근 요청, 감염병 보고, 사용자, 제출물, 상태, 교직원 제출 현황 화면
- 제출: 심폐소생술 연수 이수증, 개별 건강검진 확인, 채용검진 대체통보서 요청, 감염병 보고, 나의 제출 현황
- 홈 메뉴 데이터에는 오늘의 보건실, 제출·업로드 센터, 검진·검사 안내, 교육 자료실, 담임 협조 요청, 학생 건강관리 확인, 건강정보·이벤트, FAQ가 정의돼 있다.

### 실제 구현 기능

- 교직원이 업무 목적에 따라 들어가는 포털형 메뉴와 세부 route
- 오늘의 보건실, 제출·업로드, 검진·검사, 교육자료, 담임 협조, FAQ 화면
- Microsoft Teams 및 Google 로그인 버튼
- `staff`, `homeroom`, `health_teacher`, `admin` 역할과 학년도·학기별 배정 데이터 구조
- 보건교사·관리자용 제출 관리, 접근 요청, 감염병 보고, 교직원 제출 현황 화면
- 담임의 자기 학급 범위, 일반 교직원의 최소 기능, 보건교사 운영 기능을 구분하는 UI 정책

### IMPLEMENTED

- 위 route와 메뉴, 제출 폼, 보건교사·관리자 화면은 실제 소스에 존재한다.
- Firestore rules에 역할 및 사용자별 접근 조건이 정의돼 있다.
- 학생 건강관리 화면은 역할에 따라 자기 학급·통계·재실 여부 등을 다르게 보여주는 정책과 코드가 있다.

### PARTIAL

- 기존 Sheets·Apps Script 방식과 Firebase v2가 공존한다. 저장소만으로 전체 운영이 Firebase로 완전히 이전됐다고 판단할 수 없다.
- 코드에 권한 구조가 있으나, 모든 운영 계정·배포 환경에서의 권한 검증 완료 여부는 저장소만으로 확인할 수 없다.
- 실제 학교에서 어떤 메뉴가 얼마나 사용됐고 무엇을 고쳤는지는 저자 확인이 필요하다.

### PLANNED

- 조직 도메인 제한 등 문서에 미래 항목으로 적힌 기능은 현재 구현 기능으로 다루지 않는다.
- 코드나 route로 확인되지 않는 추가 포털 기능은 책에 넣지 않는다.

### 책에 써도 되는 기능

- 사람을 메뉴에 맞추는 대신 교직원의 방문 목적을 기준으로 메뉴를 묶은 구조
- 제출·조회·협조·자료 이용의 사용자 동선을 route로 연결한 방식
- 일반 교직원, 담임, 보건교사, 관리자의 역할별 화면과 접근 범위
- 기존 방식과 Firebase v2가 공존하는 이행 단계 자체를 현재 한계로 설명하는 내용

### 재캡처가 필요한 화면

- 포털 홈과 업무 목적별 메뉴
- 오늘의 보건실
- 제출·업로드 센터 및 나의 제출 현황
- 검진·검사, 교육자료, FAQ
- 보건교사 또는 관리자 제출 현황
- 역할별 학생 건강관리 화면

### 개인정보 주의점

- 실제 학교명, 교직원 이름, 학생 이름·학번, 건강정보, 감염병 보고 내용, 제출 파일과 연락처를 모두 mock 데이터로 교체해야 한다.
- 저장소의 기존 이미지나 설정에 실제 학교 식별 정보가 포함될 수 있으므로 그대로 출판하지 않는다.

### 근거 route/component/file

- `src/App.jsx`
- `src/data/fallbackData.js`
- `src/data/firebaseV2Navigation.js`
- `src/components/FirebaseSignInActions.jsx`
- `firestore.rules`
- `docs/PORTAL_UI_GOVERNANCE.md`
- `README.md`

### 제외해야 할 기능

- 미래 도메인 제한을 현재 완료 기능으로 표현하는 문장
- Firebase v2 전환이 완전히 끝났다는 주장
- 코드로 확인할 수 없는 실제 사용 성과와 사용자 반응

## 별도검사 도우미

- repository path: `C:/Users/보건실/OneDrive/문서/GitHub/school-health-check-scheduler`
- branch: `master`
- HEAD commit: `7cdda888413e6f8289e56618223b230ebad34b7e`
- git status: clean
- 프로젝트 구성: Vite, React 19, TypeScript, Firebase, Supabase, XLSX. 저장소 문서는 V2.0 Release Candidate·Early Access 준비 단계로 설명한다.
- 최근 변경 근거: 세션 접근 인덱스, 모바일 세션 관리, 멤버십 접근, 세션 범위 Firebase 접근 보강이 최근 커밋에 포함돼 있다.

### 주요 메뉴와 현재 화면

- 세션 관리, 설정, 계획, 결과
- 운영 센터
- 교사용 화면
- 관리자 화면
- 세로형·가로형 현황판
- 운영 보고서
- 명단 업로드, 학생 체크리스트, 검사 조건과 시간표 설정

### 실제 구현 기능

- 검사 세션 생성·선택과 검사 종류 구분
- 대상 학급·명단 업로드, 검사 조건 설정, 시간표 자동 배정
- 운영 센터에서 학급 진행과 학생 상태를 갱신하는 화면
- 교사용·관리자용·표시 전용 화면과 운영 보고서
- localStorage 기반 기본 저장과 선택적 Supabase/Firebase 연동 준비
- sample CSV와 QA용 예시 데이터

### 상태 모델에 대한 정확한 판정

- 학급 운영 상태: `대기`, `진행 중`, `완료`, `미도착`
- 운영 지연: 별도 상태 하나가 아니라 `delayedMinutes` 값으로 관리
- 학생 상태: `대기`, `완료`, `결석`, `조퇴`, `지각`, `추후검진`
- `확인 필요`: 일부 학생 예외 상태를 묶어 보여주는 UI 표현
- `이동`: 안내와 운영 단계의 표현이며, 하나의 공통 저장 상태로 확인되지 않는다.
- 따라서 `대기/이동/검사중/완료/지연/확인필요`가 하나의 통합 상태 열거형으로 구현됐다고 쓰면 안 된다.

### IMPLEMENTED

- 운영 센터, 교사용 화면, 관리자 화면, 가로형 현황판, 보고서 component가 존재한다.
- 세션·검사 종류·학급·학생 상태와 변경 기록 데이터 타입이 존재한다.
- 인쇄 가능한 운영 보고서와 개인정보 노출을 줄이기 위한 로그 필터가 존재한다.
- 역할별 접근 행렬과 관련 화면이 존재한다.

### PARTIAL

- 역할별 화면은 있으나 최종 인증·RoleGuard·QR 토큰 검증·RLS가 모두 완료된 상태는 아니다.
- Supabase schema와 repository가 있으나 문서상 실제 동기화·RLS·인증은 후속 작업이다.
- Early Access 준비 상태이며 실제 학교 운영 피드백은 저장소에서 확인되지 않는다.

### PLANNED

- 실제 QR 토큰 검증, 만료·폐기·접근 로그
- Supabase RLS와 완성된 인증
- 데이터 이전과 최종 보안 검토
- 문서에만 있고 코드로 확인되지 않는 추가 검사 유형

### 책에 써도 되는 기능

- 명단을 읽는 업무를 학급 진행, 학생 예외, 지연 정보로 분리한 설계
- 역할에 따라 같은 운영 정보를 교사용·관리자용·현황판으로 다르게 보여주는 구조
- 운영 보고서가 화면의 결과가 아니라 다음 운영을 위한 기록이 되는 구조
- 통합 6단계 상태가 아니라 서로 다른 대상별 상태 모델을 둔 실제 구현

### 재캡처가 필요한 화면

- 운영 센터
- 교사용 화면
- 관리자 화면
- 가로형 현황판
- 운영 보고서
- 세션 생성·검사 조건·시간표 설정

### 개인정보 주의점

- 학생 실명, 학번, 학급별 건강정보와 검사 결과를 사용하지 않는다.
- 3개 가상 학급과 가상 이름, 혼합 상태를 가진 전용 출판 세션을 만든 뒤 캡처해야 한다.

### 근거 route/component/file

- `src/App.tsx`
- `src/types/healthCheck.ts`
- `src/lib/operation.ts`
- `src/components/operation/OperationCenter.tsx`
- `src/components/teacher/TeacherDashboard.tsx`
- `src/components/admin/AdminDashboard.tsx`
- `src/components/display/OperationDisplay.tsx`
- `src/components/report/OperationReport.tsx`
- `ACCESS_MATRIX.md`
- `PROJECT.md`
- `schema.sql`
- `sample-data/qa-demo-roster.csv`

### 제외해야 할 기능

- 여섯 표현이 하나의 완성된 상태 머신이라는 설명
- QR 접근과 인증·RLS가 완성됐다는 설명
- 실제 학교 운영 성과나 측정하지 않은 시간 절감 수치

## BOGUNON

- repository path: `C:/Users/보건실/OneDrive/문서/GitHub/bogunon`
- branch: `main`
- HEAD commit: `bfdc46e991f79ed34ba6805c513151d344daa83a`
- git status: clean
- 프로젝트 구성: Next.js 16, React 19, Supabase. package version `0.23.1`.
- 최근 변경 근거: 교직원 연락처와 행사 보건지원, 업무 상태, 마스코트 관련 변경이 최근 커밋에 포함돼 있다.

### 주요 메뉴와 현재 화면

- 통합 홈: `/briefing`
- 일정: `/calendar`
- 업무: `/tasks`
- 행사 보건지원: `/event-health-support`
- 교직원 연락처: `/staff-contacts`
- 그 밖에 연간업무, 실무일정, 프로젝트, 워크플로, 약품, AED, 건강지원 인력, 기록 도우미, 설정 화면이 현재 navigation에 존재한다.

### 실제 구현 기능

- 통합 홈에서 날짜 기록, 일정, 학교 정보, 운동 관련 정보와 월·주 단위 정보를 조합해 보여주는 화면
- 월·주·일 캘린더와 일정·업무·학교 날짜 기록
- 업무의 분류, 반복, 상태, 검색, 프리셋, 워크플로 연결
- 체육대회·수련활동·현장체험학습 등 행사별 보건지원 준비와 체크리스트
- 교직원 연락처, 학기별 배정, 부서·학년·담당·내선·즐겨찾기·그룹 관리
- 연락처 파일 가져오기와 미리보기·병합·검토 필요 분류
- Google OAuth와 사용자 범위 Supabase 정책을 위한 코드·migration

### IMPLEMENTED

- 통합 홈, 캘린더, 업무, 행사 보건지원, 교직원 연락처 route와 UI가 존재한다.
- 업무 상태는 `planned`, `inProgress`, `waitingForReply`, `needsCheck`, `completed`, `onHold`로 정의돼 있다.
- 행사 보건지원에는 행사 유형, 날짜·장소·예상 인원·담당자·메모·상태와 준비물 체크리스트 schema가 존재한다.
- 교직원 연락처에는 학년도·학기별 배정, 그룹, 즐겨찾기와 user-scoped RLS migration이 존재한다.

### PARTIAL

- migration과 코드가 있다는 사실은 확인됐지만 실제 배포 DB에 모든 migration이 적용됐는지는 저장소만으로 확인할 수 없다.
- 통합 홈 component가 업무 데이터를 직접 표시한다고 단정할 수 없다. 현재 component에서는 전달된 일부 업무 prop이 화면에 사용되지 않는다.
- 실제 학교에서 어떤 기능이 매일 사용됐고 어떤 변화가 있었는지는 저자 확인이 필요하다.

### PLANNED

- roadmap이나 메모에만 있는 기능은 현재 기능으로 쓰지 않는다.
- 실제 배포·사용 확인이 없는 기능 확장 계획은 본문에서 제외한다.

### 책에 써도 되는 기능

- 일정, 업무, 행사 준비, 연락처처럼 흩어진 보건업무 정보를 각 데이터 구조로 바꾼 과정
- 문제 → 필요한 행동 → 기능 → 데이터 → 다음 행동의 연결
- 행사 보건지원의 행사 정보와 준비물 체크리스트 구조
- 학년도·학기별로 바뀌는 교직원 연락처 배정 구조

### 재캡처가 필요한 화면

- 현재 통합 홈
- 월·주·일 캘린더
- 업무 목록과 상태 변경
- 행사 보건지원 목록·상세·체크리스트
- 교직원 연락처 검색·그룹·학기 배정

### 개인정보 주의점

- 실제 교직원 이름, 전화번호, 내선, 부서 배정, 학교 일정과 행사 담당자를 노출하지 않는다.
- 가상 교직원, 가상 행사와 가상 학교 일정을 사용한다.

### 근거 route/component/file

- `app/(app)/briefing/page.tsx`
- `components/briefing/briefing-screen.tsx`
- `app/(app)/calendar/page.tsx`
- `app/(app)/tasks/page.tsx`
- `app/(app)/event-health-support/page.tsx`
- `app/(app)/staff-contacts/page.tsx`
- `supabase/migrations/20260928090000_create_event_health_support.sql`
- `supabase/migrations/20260923120000_create_staff_contacts.sql`
- `README.md`
- `package.json`

### 제외해야 할 기능

- 통합 홈이 현재 직접 제공하지 않는 업무 요약을 제공한다는 설명
- migration 존재만으로 운영 배포가 완료됐다는 설명
- 측정하지 않은 시간 절감, 만족도, 오류 감소 수치

## BOGUNON DESK

- repository path: `C:/Users/보건실/OneDrive/문서/GitHub/school-health-desk`
- branch: `main`
- HEAD commit: `7fa8988750f008f6ea2c736df17f616ada076626`
- git status: `.omo/evidence/desk-default-code-review.md`, `.omo/evidence/desk-default-dashboard-layout-gate-review.md`가 추적되지 않은 상태다. 이번 작업에서는 변경하지 않았다.
- 프로젝트 구성: Tauri 2, React, Vite, TypeScript, Rust. package/Cargo/Tauri version `0.2.0`.
- 최근 변경 근거: 0.2.0 release 준비, 자동 업데이트, 통합 업무 데스크 재설계, 공문 파싱 분리, OAuth·스프레드시트 처리 보강이 최근 커밋에 포함돼 있다.

### 주요 메뉴와 현재 화면

- 12열 기반 사용자 조정형 업무 데스크 `DashboardCanvas`
- 날짜·시계, 오늘 요약, 우선 업무, 월간 달력, 오늘 업무, 빠른 메모, 다가오는 일정, D-Day, 주간 일정, 알림 위젯
- 편집 가능한 Dock: 홈, 온라인 보건실, BOGUNON, 도구함, 공문, AED, 기록 도우미, 검진 도구, 업무 폴더, 빠른 메모, 설정
- 명령 팔레트와 검색
- 계산기, 구매 도우미, 공문 작업공간

### 실제 구현 기능

- Windows 데스크톱 앱의 사용자 조정형 위젯 레이아웃
- BOGUNON 계정·일정·업무 연동과 빠른 추가, 업무 완료 처리, 작업공간 검색
- 기기 안에서 관리하는 업무 폴더 즐겨찾기와 세션형 빠른 메모
- 구매 도우미의 XLSX/XLS/CSV/텍스트 PDF 로컬 분석, 열 매핑, 템플릿, 정산·내보내기
- 공문 작업공간의 새 초안·수정·요약, PDF/HWPX 로컬 가져오기와 BOGUNON 빠른 추가 인계
- 선택적 OpenAI/Gemini 사용, 개인정보 사전 점검, 차단 조건, 실제 전송 문구 확인 후 승인
- Supabase 세션의 Windows DPAPI 보호, CSP, 로컬 파일 처리
- tray, 닫을 때 tray 이동, 자동 시작, 알림, deep link, NSIS 설치와 0.2.0 자동 업데이트 코드

### IMPLEMENTED

- 현재 `App` 진입점은 과거 mock 화면이 아니라 `DashboardCanvas` 기반 통합 업무 데스크다.
- 위젯 레지스트리, Dock, 도구 패널, BOGUNON 연동, 로컬 파일 도구가 실제 코드에 존재한다.
- 공문 AI 기능은 자동 전송이 아니라 개인정보 점검과 `AI 전송 내용 확인` 단계를 거친다.
- 자동 업데이트는 현재 0.2.0 코드와 Tauri 설정에 구현돼 있다.

### PARTIAL

- 0.2.0 release 준비와 구현은 확인되지만 실제 사용자의 설치·업데이트 성공과 학교 운영 사용은 저장소만으로 확인할 수 없다.
- 외부 Dock 항목은 DESK 내부 구현이 아니라 설정된 URL이나 다른 앱으로 연결되는 항목이다.
- BOGUNON 연결은 계정·배포 환경과 migration 상태에 영향을 받는다.

### PLANNED

- 코드에 없는 OCR, 레거시 HWP 처리, 문서 이력 등은 현재 기능으로 쓰지 않는다.
- 과거 mock UI와 폐기된 설계는 현재 화면으로 다루지 않는다.
- 기능 동결 전의 추가 계획은 최종 캡처 대상으로 확정하지 않는다.

### 책에 써도 되는 기능

- 웹 도구들을 하나의 Windows 업무 시작점으로 묶는 현재 레이아웃
- 로컬 파일 처리와 외부 서비스 연결을 구분한 설계
- AI로 보내기 전 개인정보를 점검하고 전송 내용을 사람이 승인하는 흐름
- 빠른 메모를 임시로 두고 확인 후 실제 일정·업무로 넘기는 흐름

### 재캡처가 필요한 화면

- 현재 `DashboardCanvas` 전체 화면
- 레이아웃 편집과 Dock
- BOGUNON 연결 상태와 빠른 추가
- 구매 도우미의 mock 파일 분석 결과
- 공문 작업공간의 mock 문서와 AI 전송 확인
- 설정의 보안·업데이트 관련 화면은 기능 동결 후 선택한다.

### 개인정보 주의점

- 실제 업무 폴더 경로, 계정 이메일, 최근 문서명, 일정, 업무, 학교명, 공문 내용과 API key가 보이지 않게 한다.
- mock 문서와 별도 데모 계정 또는 완전히 비식별화한 로컬 상태를 사용한다.

### 근거 route/component/file

- `src/App.tsx`
- `src/components/dashboard/DashboardCanvas.tsx`
- `src/dashboard/widgetRegistry.tsx`
- `src/tools/toolRegistry.ts`
- `src/components/desktop/OfficialDocumentPanel.tsx`
- BOGUNON workspace repository·auth 관련 `src` 파일
- `src-tauri/tauri.conf.json`
- `src-tauri/Cargo.toml`
- `package.json`
- `README.md`

### 제외해야 할 기능

- 과거 mock UI를 현재 화면처럼 소개하는 내용
- OCR·레거시 HWP·문서 이력을 완료 기능처럼 쓰는 내용
- 외부 연결 도구를 DESK 내부 기능처럼 쓰는 내용
- 실제 배포와 운영 성과가 확인됐다는 주장

## 감사 결론

- 네 앱 저장소를 모두 로컬에서 식별했다. 찾지 못한 핵심 앱 저장소는 없다.
- 책에서 사실형으로 설명할 수 있는 범위는 현재 코드·화면·schema로 확인된 기능까지다.
- 실제 필요가 생긴 사건, 학교에서의 사용 장면, 사용 후 변화, 사용자 반응은 저장소로 확인할 수 없으므로 새 원고에서 `[AUTHOR INPUT REQUIRED]`로 분리한다.
- 별도검사 도우미는 여섯 표현을 하나의 상태 머신으로 단순화하지 않고, 학급·운영·학생의 서로 다른 상태 모델을 그대로 설명해야 한다.
- BOGUNON DESK는 현재 main의 `DashboardCanvas`와 0.2.0 구현을 기준으로 하며 최종 캡처는 기능 동결 후 진행한다.

# Release Checklist — v1.0.0

『보건교사를 위한 AI 업무 자동화』 출간 전 최종 점검 결과입니다. 아래 항목은 그동안 진행된 각 단계별 QA(원고 구조 검수, QR 정책 정렬, PDF 페이지 단위 전수 검수, 54페이지 조판 결함 수정)를 종합한 최종 결과입니다.

## 1. 원고 (book-source-final.md)

| 항목 | 결과 |
|---|---|
| PART 1~8, Chapter 01~22, 에필로그 완결성 | PASS |
| 제목 계층 구조(H1~H5) | PASS |
| 이미지 9종(IMG-001~IMG-009) 배치 및 캡션 | PASS |
| Markdown 문법 오류 | PASS |
| 조판 앵커(PAGE BREAK, KEEP BLOCK TOGETHER) | PASS |
| 임시 문구·Placeholder·TODO 잔존 여부 | PASS (0건) |
| 중복 heading | PASS (0건) |

## 2. QR 정책

| 항목 | 결과 |
|---|---|
| Chapter 02~22 QR 안내 문구 21건 정책 문구 통일 | PASS |
| 금지 문구 잔존 여부 | PASS (0건) |
| QR 목표 URL(`https://ai-school-health-resource-center.vercel.app/`) 일치 | PASS (21/21) |

## 3. PDF (book-final-pass2.pdf)

| 항목 | 결과 |
|---|---|
| 총 페이지 수 | PASS (255페이지, A5) |
| 페이지 연속성(누락·중복·빈 페이지) | PASS |
| PART/Chapter/실습/에필로그 표지 및 진입 페이지 | PASS |
| 제목 줄바꿈(단어 중간 절단 없음) | PASS |
| 본문 텍스트 무결성(깨진 문자·치환 문자 없음) | PASS |
| 반복 컴포넌트 페이지 분리 없음(진행 카드·CASE·Workflow·오늘 만든 프로젝트·쑤캥의 한마디·오늘 바뀐 것·Preview) | PASS |
| 표 63개(잘림·겹침·행 높이) | PASS |
| 이미지 9개(크롭·왜곡·해상도·캡션 동일 페이지 배치) | PASS |
| QR 21개(디코딩 성공률·여백·크기) | PASS (21/21, 100%) |
| 폰트 임베딩(서브셋) | PASS |
| PDF 구조 검증(qpdf) | PASS |
| 54페이지 고아 문장 결함 | PASS (수정 완료, 8bf4d09) |

## 4. 최종 확인

- 페이지 54 수정이 다른 페이지에 영향을 주지 않았음을 255페이지 전수 텍스트 비교로 확인 (수정 전후 차이: 53, 54페이지만)
- Chapter 06 시작 위치(55페이지), 전체 페이지 수(255) 변경 없음

## 최종 판정

**출간 가능**

전 항목 PASS, 미해결 FAIL 없음.

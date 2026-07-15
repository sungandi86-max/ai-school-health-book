# 『보건교사를 위한 AI 업무 자동화』 원고 저장소

보건교사가 반복 업무를 관찰하고, 작게 나누고, AI에게 맡길 부분과 사람이 끝까지 판단할 부분을 구분해가는 8개 PART · 22개 Chapter 프로젝트북의 출간 원고 저장소입니다.

이 저장소는 **책 원고만 관리**합니다. 보건교사를 위한 실습 자료·프롬프트·템플릿을 제공하는 Resource Hub(자료실 웹사이트)는 별도 저장소(`ai-school-health-resource-center`)에서 관리하며, 이 저장소에는 포함하지 않습니다.

## 폴더 구조

```
book-source/   PART 1~8, Chapter 01~22, 에필로그 원고 및 병합본(book-source-final.md)
docs/          BOOK_STYLE.md(편집·시각 스타일 기준), CHAPTER_TEMPLATE.md(Chapter 구성 기준)
assets/        실제 프로젝트 화면 이미지 (책 안 증거 자료)
pdf/           최종 조판본 PDF
```

## Single Source of Truth

`book-source/book-source-final.md` 는 PART 1~8, Chapter 01~22, 에필로그 원고를 하나로 병합한 최종본이며, 이후 모든 출간·조판·개정판·전자책 작업의 기준이 되는 단일 원본입니다. 원고를 수정할 때는 이 파일을 기준으로 작업하고, 개별 PART/Chapter 파일이 아닌 이 파일을 최신 상태로 유지합니다.

## 작업 순서

1. `book-source/` 안의 PART/Chapter 원고를 직접 수정합니다. (본문, 문체, CASE, Workflow, 실습, QR 정책, Chapter 번호·실습 번호는 임의로 바꾸지 않습니다.)
2. `docs/BOOK_STYLE.md`, `docs/CHAPTER_TEMPLATE.md` 기준에 맞춰 편집합니다.
3. 변경 사항을 `book-source/book-source-final.md`에 반영해 병합본을 최신화합니다.
4. `assets/`의 실제 화면 이미지가 필요한 경우 `IMG-001` 형식의 앵커와 1~2문장 캡션을 함께 추가합니다.
5. PART 1~8, Chapter 01~22, 에필로그 존재 여부, 이미지 링크, 중복 heading, TODO/Placeholder 잔존 여부를 검증합니다.
6. `feature/...` 브랜치에서 작업 후 Pull Request로 병합합니다.

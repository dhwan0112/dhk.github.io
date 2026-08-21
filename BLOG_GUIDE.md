# 블로그 포스트 작성 가이드

## 파일 생성

### 위치
`_posts/` 폴더

### 파일명
```
YYYY-MM-DD-제목.md
```
예: `2025-01-18-lammps-tutorial.md`

---

## 템플릿

```markdown
---
title: "포스트 제목"
date: 2025-01-18
category: Tutorial
tags: [태그1, 태그2]
description: "목록 페이지에 표시될 2~3문장 요약 (생략하면 본문 앞부분 320자가 대신 표시됨)"
---

본문 시작. `description`을 쓰지 않으면 코드 블록까지 포함한 본문 앞부분이 그대로 미리보기에 노출되므로, 가능하면 직접 써 주는 것이 좋습니다.

## 소제목

본문 내용...

### 코드

```python
print("Hello World")
```

### 수학 공식

인라인: $E = mc^2$

블록:
$$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$

### 이미지

![설명](/assets/images/example.jpg)

### 표

| 항목 | 값 |
|------|-----|
| A | 100 |
| B | 200 |
```

---

## 목록 페이지 동작

- `/blog/`는 모든 글을 최신순으로 한 줄 구분선 목록으로 보여줍니다 (카드 없음).
- 상단의 태그 줄과 각 글의 태그를 누르면 `?tag=이름`으로 필터링됩니다.
- 글 페이지에서는 `##`/`###` 제목이 자동으로 우측 목차(1280px 이상 화면)에 올라갑니다. 제목을 두 개 이상 써야 목차가 나타납니다.

## 카테고리 목록

| Category | 설명 |
|----------|------|
| `Tutorial` | 튜토리얼, 가이드 |
| `Computation` | 계산화학, 시뮬레이션 |
| `Research` | 연구 노트, 논문 리뷰 |
| `Study` | 공부 정리, 개념 설명 |
| `Thoughts` | 생각, 에세이 |
| `Project` | 프로젝트 기록 |

**새 카테고리 추가:** 위 표에 추가하고, 포스트에서 `category: 새카테고리` 사용

---

## 태그 예시

- 과목: `Chemistry`, `Physics`, `Math`, `Biology`
- 도구: `LAMMPS`, `Python`, `VASP`, `Gaussian`
- 유형: `Tutorial`, `Review`, `Notes`

---

## 업로드 방법

### GitHub 웹에서
1. `_posts/` 폴더 → "Add file" → "Create new file"
2. 파일명: `2025-01-18-my-post.md`
3. 템플릿 복사 후 내용 작성
4. "Commit changes" 클릭

### 로컬 Git
```bash
# 파일 생성 후
git add _posts/2025-01-18-my-post.md
git commit -m "Add blog post: 제목"
git push
```

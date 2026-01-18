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
---

첫 문단은 목록 페이지에 미리보기로 표시됩니다.

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

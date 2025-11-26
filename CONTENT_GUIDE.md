# 콘텐츠 추가 가이드 (Content Management Guide)

이 문서는 웹사이트에 새로운 콘텐츠(이미지, 동영상, 연구 노트 등)를 쉽게 추가하는 방법을 설명합니다.

## 목차
1. [연구 결과 추가하기](#연구-결과-추가하기)
2. [연구 노트 추가하기](#연구-노트-추가하기)
3. [동영상 추가하기](#동영상-추가하기)
4. [이미지 업로드하기](#이미지-업로드하기)

---

## 연구 결과 추가하기

### 위치
`content/research-results.json`

### 이미지 추가

```json
{
  "images": [
    {
      "id": 1,
      "title": "결과물 제목",
      "description": "실험 결과, 데이터 시각화, 또는 분자 구조에 대한 간단한 설명",
      "date": "2024-03-15",
      "imageUrl": "images/results/my-image.jpg",
      "category": "분광학"
    }
  ]
}
```

**필드 설명:**
- `id`: 고유 번호 (순차적으로 증가)
- `title`: 결과물의 제목
- `description`: 간단한 설명
- `date`: 날짜 (YYYY-MM-DD 형식)
- `imageUrl`: 이미지 파일 경로
- `category`: 카테고리 (선택사항)

---

## 동영상 추가하기

### YouTube 동영상

```json
{
  "videos": [
    {
      "id": 1,
      "title": "실험 영상 제목",
      "description": "실험 영상 또는 시연에 대한 설명",
      "date": "2024-03-20",
      "videoType": "youtube",
      "videoUrl": "https://www.youtube.com/embed/VIDEO_ID",
      "category": "합성"
    }
  ]
}
```

**YouTube 동영상 ID 찾기:**
1. YouTube에서 동영상 열기
2. URL 확인: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
3. `v=` 뒤의 부분이 VIDEO_ID: `dQw4w9WgXcQ`
4. embed URL 만들기: `https://www.youtube.com/embed/dQw4w9WgXcQ`

### Vimeo 동영상

```json
{
  "videoType": "vimeo",
  "videoUrl": "https://player.vimeo.com/video/VIDEO_ID"
}
```

### 로컬 동영상 파일

```json
{
  "videoType": "file",
  "videoUrl": "videos/my-experiment.mp4"
}
```

**동영상 파일 업로드 단계:**
1. 동영상 파일을 `videos/` 폴더에 업로드
2. 파일 경로를 `videoUrl`에 입력 (예: `videos/experiment-2024-03.mp4`)

---

## 연구 노트 추가하기

### 위치
`content/research-notes.json`

### 예시

```json
{
  "notes": [
    {
      "id": 1,
      "title": "실험 제목",
      "date": "2024-03-15",
      "category": "합성",
      "objective": "실험의 목적 또는 연구 질문에 대한 간단한 설명",
      "procedure": [
        "실험 절차 1단계",
        "실험 절차 2단계",
        "실험 절차 3단계"
      ],
      "observations": "실험 중 관찰한 세부 사항. 예상치 못한 결과, 색 변화, 또는 관찰된 현상 포함.",
      "data": "원시 데이터, 측정값, 또는 예비 분석. 표, 계산, 또는 데이터 파일 링크 포함 가능.",
      "conclusions": "결과의 예비 해석 및 다음 단계",
      "attachments": [
        {
          "name": "image_001.jpg",
          "type": "image"
        },
        {
          "name": "data_table.xlsx",
          "type": "file"
        }
      ]
    }
  ]
}
```

**필드 설명:**
- `id`: 고유 번호
- `title`: 실험 제목
- `date`: 실험 날짜 (YYYY-MM-DD)
- `category`: 카테고리 (합성, 분석, 특성화 등)
- `objective`: 실험 목적
- `procedure`: 실험 절차 (배열 형식)
- `observations`: 관찰 내용
- `data`: 데이터 및 측정값
- `conclusions`: 결론 및 다음 단계
- `attachments`: 첨부 파일 목록 (선택사항)

---

## 이미지 업로드하기

### 1. GitHub 웹 인터페이스 사용

1. GitHub 저장소로 이동
2. `images/` 폴더로 이동 (없으면 생성)
3. "Add file" → "Upload files" 클릭
4. 이미지 파일 드래그 앤 드롭
5. "Commit changes" 클릭

### 2. 로컬에서 추가

```bash
# 1. 이미지를 images/ 폴더에 복사
cp my-image.jpg images/results/

# 2. Git에 추가
git add images/results/my-image.jpg

# 3. 커밋
git commit -m "Add research result image"

# 4. 푸시
git push
```

### 이미지 최적화 팁
- 웹용 이미지 크기: 1920px 이하
- 파일 형식: JPG, PNG, WebP
- 파일 크기: 500KB 이하 권장

---

## 콘텐츠 추가 작업 흐름

### 단계별 가이드

#### 1. JSON 파일 편집

```bash
# content/research-results.json 또는 research-notes.json 편집
nano content/research-results.json
```

또는 GitHub 웹 인터페이스에서:
1. 파일로 이동
2. 연필 아이콘(Edit) 클릭
3. 내용 편집
4. "Commit changes" 클릭

#### 2. 새 항목 추가

**기존 항목 복사:**
1. 마지막 항목 전체를 복사
2. 쉼표(,) 추가
3. 붙여넣기
4. 내용 수정 (id, title, description, date 등)

**예시:**
```json
{
  "images": [
    {
      "id": 1,
      "title": "첫 번째 결과",
      ...
    },
    {
      "id": 2,
      "title": "두 번째 결과",
      ...
    }
  ]
}
```

#### 3. 변경사항 확인

1. 웹사이트에서 해당 페이지 새로고침
2. 새 콘텐츠가 표시되는지 확인
3. 링크와 이미지가 올바르게 작동하는지 확인

---

## 문제 해결

### 콘텐츠가 표시되지 않을 때

1. **JSON 형식 확인**
   - 쉼표(,) 위치 확인
   - 중괄호 {} 와 대괄호 [] 매칭 확인
   - 온라인 JSON 검증 도구 사용: https://jsonlint.com

2. **파일 경로 확인**
   - 이미지/동영상 파일이 올바른 위치에 있는지 확인
   - 경로에 오타가 없는지 확인

3. **브라우저 캐시 지우기**
   - Chrome/Edge: Ctrl + Shift + R
   - Mac: Cmd + Shift + R

### JSON 문법 오류 예시

**잘못된 예:**
```json
{
  "images": [
    {
      "id": 1,
      "title": "제목"
    }  // <- 쉼표 누락
    {
      "id": 2,
      "title": "제목"
    }
  ]
}
```

**올바른 예:**
```json
{
  "images": [
    {
      "id": 1,
      "title": "제목"
    },
    {
      "id": 2,
      "title": "제목"
    }
  ]
}
```

---

## 추가 도움말

### 파일 구조
```
dhk.github.io/
├── content/
│   ├── research-results.json    # 연구 결과 데이터
│   └── research-notes.json      # 연구 노트 데이터
├── images/
│   └── results/                 # 결과 이미지
├── videos/                      # 로컬 동영상
└── js/
    └── content-loader.js        # 콘텐츠 로딩 스크립트
```

### 유용한 링크
- JSON 검증: https://jsonlint.com
- 이미지 압축: https://tinypng.com
- 동영상 압축: https://www.handbrake.fr

---

## 지원

문제가 발생하거나 도움이 필요한 경우:
- JSON 형식 오류는 jsonlint.com에서 확인
- 파일 경로와 이름에 특수문자나 공백이 없는지 확인
- 브라우저 콘솔(F12)에서 오류 메시지 확인

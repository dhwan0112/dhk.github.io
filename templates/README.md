# 실험 일지 템플릿 (Lab Note Templates)

이 폴더에는 실험 일지 작성을 위한 템플릿이 포함되어 있습니다.

## 파일 설명

### 1. `lab-note-template.md`
상세한 실험 기록을 위한 마크다운 템플릿입니다.

**사용 방법:**
1. 이 파일을 복사하여 새 파일 생성
2. 파일명을 실험 날짜와 이름으로 변경 (예: `2024-03-15-촉매-합성.md`)
3. 각 섹션을 채워넣기
4. 로컬에 보관하거나 웹사이트에 업로드

**포함 섹션:**
- 실험 정보 (제목, 날짜, 카테고리)
- 실험 목적
- 시약 및 재료 (표 형식)
- 실험 절차 (단계별)
- 관찰 사항
- 데이터 및 분석
- 결과
- 분석 데이터 (NMR, IR, UV-Vis 등)
- 토의 및 결론
- 참고문헌
- 첨부 파일 체크리스트

**장점:**
- 완전한 실험 기록 유지
- 나중에 논문 작성 시 참고 가능
- 모든 세부 사항 체계적으로 정리
- Markdown 형식으로 GitHub에서 바로 읽기 가능

### 2. `lab-note-template.json`
웹사이트 업로드를 위한 JSON 템플릿입니다.

**사용 방법:**
1. 이 파일의 구조를 참고
2. `content/research-notes.json` 파일 열기
3. 새 항목을 배열에 추가
4. Git으로 커밋 및 푸시

**포함 필드:**
- `id`: 고유 번호
- `title`: 실험 제목
- `date`: 실험 날짜
- `category`: 카테고리
- `objective`: 실험 목적
- `procedure`: 실험 절차 (배열)
- `observations`: 관찰 사항
- `data`: 데이터 및 분석
- `conclusions`: 결론
- `attachments`: 첨부 파일 목록

**장점:**
- 웹사이트에 바로 표시
- 간단한 형식으로 빠른 업로드
- 다른 사람과 쉽게 공유

## 사용 시나리오

### 시나리오 1: 간단한 실험 기록
→ `lab-note-template.json` 사용
→ 웹사이트에 바로 업로드

### 시나리오 2: 상세한 연구 기록
→ `lab-note-template.md` 사용
→ 로컬에 보관 + 요약본을 JSON으로 웹사이트에 업로드

### 시나리오 3: 논문 준비용
→ `lab-note-template.md` 사용
→ 모든 세부 사항 기록
→ GitHub 저장소에 보관

## 빠른 시작 예시

### Markdown 템플릿으로 실험 기록하기

```bash
# 1. 템플릿 복사
cp templates/lab-note-template.md experiments/2024-03-15-synthesis.md

# 2. 에디터로 열기
nano experiments/2024-03-15-synthesis.md

# 3. 내용 작성 후 저장

# 4. Git에 추가
git add experiments/2024-03-15-synthesis.md
git commit -m "Add synthesis experiment log"
git push
```

### JSON으로 웹사이트에 업로드하기

```bash
# 1. JSON 파일 편집
nano content/research-notes.json

# 2. 새 항목 추가 (템플릿 참고)

# 3. 저장 후 Git 푸시
git add content/research-notes.json
git commit -m "Add new lab note"
git push
```

## 팁

1. **일관성 유지**: 항상 같은 형식으로 기록하면 나중에 찾기 쉽습니다
2. **즉시 기록**: 실험 직후 바로 기록하면 세부 사항을 잊지 않습니다
3. **사진 첨부**: 실험 사진을 꼭 찍어서 첨부하세요
4. **백업**: 중요한 실험은 Markdown과 JSON 둘 다 작성하는 것을 권장합니다

## 문의

템플릿 수정이 필요하거나 새로운 필드가 필요한 경우 자유롭게 수정하세요!

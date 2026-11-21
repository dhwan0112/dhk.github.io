# 모던 Fortran 가이드 작성 규칙

`fortran/*.md`를 고치거나 장을 더할 때 따르는 규칙이다. 기계로 검사하는 규칙은 아래 표에 강제 수단을 적었고, 나머지는 판단이 필요한 규칙이다.

## 검사 명령

```sh
python3 tools/fortran_guide.py lint
python3 tools/fortran_guide.py examples
bundle exec jekyll build && python3 tools/fortran_guide.py site _site
```

## 규칙과 강제 수단

| 규칙 | 강제 수단 | 위치 |
|---|---|---|
| front matter는 `title`, `order`, `permalink`만 쓴다 | lint | `tools/fortran_guide.py` |
| 주소는 `/fortran/`(서문)과 `/fortran/NN-slug/`이고 파일 이름과 같다 | lint | `tools/fortran_guide.py` |
| `order`는 1부터 빈틈없이 이어지고 파일 번호와 같다 | lint | `tools/fortran_guide.py` |
| 본문에 Liquid, kramdown 속성, `<script>`를 쓰지 않는다 | lint | `tools/fortran_guide.py` |
| 펜스 언어는 `fortran`, `sh`, `text`만 쓴다 | lint | `tools/fortran_guide.py` |
| 모든 `fortran` 블록은 예제 파일과 같고, 바로 윗줄에 `<!-- file: chNN/name.f90 -->`나 `<!-- excerpt: ... -->`를 단다 | lint | `tools/fortran_guide.py` |
| 실행 결과 블록은 `<!-- output: chNN/name.out -->`를 달아 `.out` 파일과 맞춘다 | lint | `tools/fortran_guide.py` |
| 예제는 그 장 번호의 폴더 `examples/fortran/chNN/`에 둔다 | lint | `tools/fortran_guide.py` |
| 모든 예제 파일은 어느 장에든 나온다 | lint | `tools/fortran_guide.py` |
| 예제는 `-std=f2018 -Wall -Wextra`로 경고 없이 컴파일된다. 남기는 경고는 `.warning`에 적고 결정 로그에 이유를 쓴다 | examples | `tools/fortran_guide.py` |
| 예제의 실제 출력은 `.out`과 같다 | examples | `tools/fortran_guide.py` |
| 이미지는 `fortran/images/`에만 둔다 | lint | `tools/fortran_guide.py` |
| 가이드 안 링크는 있는 장을 가리킨다 | lint, site | `tools/fortran_guide.py` |
| 용어표의 셋째 열 표기를 쓰지 않는다 | lint | `docs/fortran-guide-glossary.md` |
| 문법과 표준에 대한 서술은 표준 문서, gfortran 문서, fortran-lang.org로 확인하고 출처를 결정 로그에 적는다 | 없음 (판단 필요) | 이 문서 |
| 한국어 평서문으로 간결하게 쓰고, 과장과 상투적 도입부를 쓰지 않는다 | 없음 (판단 필요) | 이 문서 |
| 레거시 문법은 옛 코드를 읽기 위한 맥락으로만 다룬다 | 없음 (판단 필요) | 이 문서 |
| 예제 코드에 설명 주석을 달지 않는다. 설명은 본문에 쓴다. 주석 문법 자체를 보여 주는 예제만 예외다 | 없음 (판단 필요) | 이 문서 |

## 장의 모양

- 첫 문단 한두 문장에 이 장에서 무엇을 배우는지 쓴다.
- 이어서 설명과 예제를 번갈아 쓰고, 마지막에 `## 흔한 실수`를 둔다. 쓸 내용이 없는 절은 만들지 않는다.
- 제목은 `##`와 `###`만 쓴다. 장 제목은 레이아웃이 `title`로 출력하므로 본문에 `#`를 쓰지 않는다.
- 다른 장은 `[5장](/fortran/05-variables/)`처럼 절대 경로로 가리킨다.
- 컴파일러 메시지를 보여 줄 때는 실제로 받은 메시지를 옮기고 gfortran 판 번호를 적는다.
- `print *`처럼 출력 모양을 컴파일러가 정하는 예제는 공백 수가 컴파일러마다 다를 수 있다. 출력 모양이 요점인 예제는 형식 지정을 쓴다.

## 문체

- "~다", "~한다"로 끝나는 평서문을 쓴다.
- "강력한", "매우 중요한", "이제 ~해 보자" 같은 꾸밈말을 쓰지 않는다.
- 한 문장에 한 가지를 말한다. 같은 내용을 장 끝에서 다시 요약하지 않는다.
- 영어 원어는 그 장에서 처음 나올 때만 괄호로 적는다.

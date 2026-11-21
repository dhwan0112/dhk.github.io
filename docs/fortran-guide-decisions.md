# 모던 Fortran 가이드 결정 로그

판단이 들어간 결정만 적는다. 결정을 뒤집을 때는 기존 줄을 고치지 않고 새 줄을 추가해 무엇을 대체하는지 적는다.

## 결정

| 날짜 | 범위 | 결정 | 근거 | 버린 대안 | 검증 방법 |
|---|---|---|---|---|---|
| 2026-11-21 | 주소 | 서문을 `/fortran/`, 나머지 장을 `/fortran/NN-slug/`에 둔다. 부록 A와 B는 21, 22번을 쓴다. | 주소를 파일 이름에서 만들면 엔진을 바꿔도 같은 주소를 다시 만들 수 있다. 부록에 글자를 쓰면 NN 형식이 깨진다. | `/guides/fortran/` 아래 두기(사용자가 `/fortran/`을 지정), 부록을 `/fortran/a-legacy/`로 두기 | lint가 `permalink == /fortran/<파일 이름>/`과 파일 번호 == `order`를 검사한다. |
| 2026-11-21 | 구조 | 장 파일은 Jekyll 컬렉션이 아닌 일반 페이지로 두고, 레이아웃은 `_config.yml`의 `defaults`(경로 `fortran`)로 지정한다. | front matter를 `title`, `order`, `permalink` 셋으로 제한해야 하므로 `layout` 키를 쓸 수 없다. | 컬렉션 `_fortran` (폴더 이름에 밑줄이 붙어 엔진 중립성이 떨어진다) | lint가 front matter 키 집합을 검사한다. |
| 2026-11-21 | 레이아웃 | 기존 가이드(`guides/lammps/` 등)와 같은 독립 HTML 구조와 `guides/assets/css/guide.css`를 쓰고, 사이드바 묶음과 장 번호, 이전/다음 링크는 `_layouts/fortran.html`이 `order`로 만든다. | 기존 가이드는 사이트 공통 레이아웃이 아니라 자체 사이드바가 있는 독립 페이지다. | 사이트 공통 `page` 레이아웃(기존 가이드와 모양이 달라진다) | 로컬 빌드 결과를 기존 LAMMPS 가이드 페이지와 나란히 비교했다. |
| 2026-11-21 | 레이아웃 | 장 목록은 `site.pages`가 아니라 `site.html_pages`에서 고른다. | `_config.yml`에 `pages`라는 컬렉션이 있어 Liquid의 `site.pages`가 그 컬렉션(`_pages/`)을 가리킨다. 일반 페이지 목록은 `site.html_pages`에 남아 있다. | 기존 `pages` 컬렉션 이름 바꾸기(기존 주소와 설정을 건드린다) | 시험 페이지로 두 목록의 크기를 출력해 확인했다(`site.pages` 0개, `site.html_pages` 3개). |
| 2026-11-21 | 레이아웃 | 사이드바 묶음(1-4, 5-10, 11-14, 15-17, 18-20, 부록)은 레이아웃에 고정한다. | 묶음 이름을 front matter에 넣으면 키 제한을 어긴다. | `_data`에 목차 파일 두기(엔진을 바꿀 때 옮길 파일이 늘어난다) | 빌드한 사이드바를 확인했다. |
| 2026-11-21 | 레이아웃 | 쪽 안 목차는 빌드하지 않고 브라우저에서 `h2`로 만든다. | kramdown의 `{:toc}` 같은 엔진 전용 문법을 본문에 쓰지 않기 위해서다. | 본문에 `{:toc}` | lint가 `{:`를 금지한다. |
| 2026-11-21 | 레이아웃 | 모든 장 아래에 원본 저자와 Stanford 저작권 표기를 짧게 붙인다. | 원본의 이용 허락 조건이 "all author and copyright information is retained"이다. 서문 한 곳보다 모든 쪽에 남기는 편이 조건을 확실히 지킨다. | 서문에만 표기 | 빌드한 각 장 아래쪽을 확인했다. |
| 2026-11-21 | 코드 블록 | Fortran 코드는 ```fortran 블록에만 쓰고, 셸 명령은 ```sh, 실행 결과는 ```text 블록에 쓴다. 그 밖의 언어 표시나 들여쓰기 코드 블록, Liquid `highlight` 태그는 쓰지 않는다. | 지시는 "코드는 fortran fenced 블록으로만"이다. 컴파일 명령과 출력까지 fortran으로 표시하면 강조가 틀어진다. | 명령도 fortran 블록에 넣기 | lint가 펜스 언어를 `fortran`, `sh`, `text`로 제한한다. |
| 2026-11-21 | 예제 일치 | 블록 바로 윗줄에 HTML 주석 `<!-- file: chNN/name.f90 -->`(전체 파일), `<!-- excerpt: ... -->`(파일의 연속한 줄), `<!-- output: chNN/name.out -->`(실행 결과)를 단다. | HTML 주석은 CommonMark, kramdown, Pandoc 모두에서 본문 문법을 해치지 않는다. 펜스 정보 문자열에 경로를 넣으면 `fortran` 뒤에 엔진마다 다르게 읽히는 속성이 붙는다. | 펜스 정보 문자열(```fortran file=...`), 별도 대응표 파일(본문과 표가 따로 어긋날 수 있다) | lint가 내용 불일치, 표시 없는 fortran 블록, 어느 장에도 나오지 않는 예제 파일을 오류로 보고한다. 일부러 한 글자를 바꿔 실패하는지 확인했다. |
| 2026-11-21 | 예제 | 예제 하나는 파일 하나이고, 기대 결과는 같은 이름의 옆 파일(`.out`, `.in`, `.flags`, `.warning`, `.compile-error`, `.run-error`)로 둔다. | 예제와 기대 결과가 한 폴더에 나란히 있으면 고칠 때 함께 보인다. | 예제 전체를 적은 매니페스트 파일 하나(충돌이 잦고 예제와 떨어져 있다) | `tools/fortran_guide.py examples`가 옆 파일 규칙을 적용한다. |
| 2026-11-21 | 예제 | 모든 예제를 `-std=f2018 -Wall -Wextra`로 컴파일하고, 경고는 `.warning` 파일에 적은 것만 허용한다. `.warning`이 있는 예제는 이 로그에 경로와 이유를 적어야 한다. | 경고 0이 목표이고, 남기는 경고는 이유를 기록하라는 지시를 기계가 강제하게 했다. | `-Werror`(의도적으로 경고를 보여 주는 예제를 둘 수 없다) | 검사기가 예상하지 않은 경고, 나오지 않은 예상 경고, 로그에 없는 경로를 오류로 보고한다. |
| 2026-11-21 | 예제 | 고정 형식 예제(부록 A)는 `.f` 확장자를 쓴다. | gfortran은 확장자로 소스 형식을 정한다. `.f90`에 `-ffixed-form`을 붙이면 파일만 보고 형식을 알 수 없다. | `.f90` + `-ffixed-form` | 검사기가 `.f`도 같은 옵션으로 컴파일한다. |
| 2026-11-21 | CI | CI는 Ubuntu의 `gfortran-14`로, 로컬 검증은 gfortran 15.2로 한다. | ubuntu-latest(24.04)의 기본 gfortran은 13이다. 두 판에서 모두 통과하면 독자 환경 차이에 덜 민감하다. | CI에서 gfortran 15 설치(공식 패키지가 없다) | CI 실행 기록과 로컬 실행 결과를 둘 다 확인했다. |
| 2026-11-21 | 용어 | 용어는 `docs/fortran-guide-glossary.md` 표를 따르고, 셋째 열의 표기는 lint가 금지한다. | 같은 개념에 다른 말이 섞이는 실수는 사람이 매번 찾기 어렵다. | 문서로만 규칙 두기 | 금지 표기를 일부러 넣어 lint가 실패하는지 확인했다. |
| 2026-11-21 | 원전 | 한국어 본문은 Stanford 원본을 바탕으로 새로 쓰고, 선행 한국어판(오병성 역)은 장 구성과 용어를 대조하는 데만 썼다. 선행판의 "어레이", "지정", "공통 블록"은 따르지 않고 "배열", "대입", "common 블록"으로 쓴다. | 지시 사항이다. 선행판의 문장을 쓰지 않으려고 본문을 쓸 때 선행판을 열어 두지 않았다. | | 본문과 선행판의 문장을 대조했다. |
| 2026-11-21 | 장 구성 | 원본의 "How to use Fortran on the Unix computers at Stanford"(4장)와 18.3절의 강의 계정 경로는 옮기지 않고 4장을 gfortran과 fpm 설치로 바꾼다. 선행판의 학과 전용 장(물리학과 사용법, 그림표, SLATEC)도 옮기지 않는다. | 지시 사항이다. 특정 기관 환경이라 지금 독자에게 쓸모가 없다. | | 장 목록을 원본, 선행판과 대조했다. |
| 2026-11-21 | 장 구성 | 원본 14장(data, block data)은 따로 두지 않고 5장(초기화)과 부록 A(`data`, `block data`)로 나눈다. 원본 13장(common blocks)은 16장 "모듈로 데이터 공유하기"로 바꾸고 common 문법은 부록 A로 옮긴다. | 지시한 장 목록에 data 장이 없다. 새 코드에는 선언 시 초기화와 모듈을 쓴다. | | 장 목록 대조 |
| 2026-11-21 | 경고 | ch21/truncated.f 의 경고 "Line truncated"를 남긴다. | 72열을 넘은 부분이 말없이 잘려 값이 바뀌는 사고를 보여 주는 예제라서 경고가 나와야 한다. 경고를 읽는 습관을 독자가 직접 보게 한다. | 경고가 나오지 않게 고치기(옛 문법을 보여 주는 예제의 목적이 사라진다) | `.warning`에 적고 `python3 tools/fortran_guide.py examples`로 같은 경고가 나오는지 확인했다(gfortran 15.2). |
| 2026-11-21 | 경고 | ch21/old_loops.f 의 경고 "Labeled DO statement"를 남긴다. | 문번호 do는 폐기 예정 기능이다. 옛 코드를 읽는 장이므로 -std=f2018이 폐기 예정 기능에 내는 경고를 그대로 보여 준다. 새 코드에는 쓰지 말라는 경고를 독자가 직접 보게 한다. | 경고가 나오지 않게 고치기(옛 문법을 보여 주는 예제의 목적이 사라진다) | `.warning`에 적고 `python3 tools/fortran_guide.py examples`로 같은 경고가 나오는지 확인했다(gfortran 15.2). |
| 2026-11-21 | 경고 | ch21/computed_goto.f 의 경고 "Computed GOTO"를 남긴다. | computed goto는 폐기 예정 기능이고, 옛 코드에서 알아볼 수 있어야 한다. 새 코드에는 쓰지 말라는 경고를 독자가 직접 보게 한다. | 경고가 나오지 않게 고치기(옛 문법을 보여 주는 예제의 목적이 사라진다) | `.warning`에 적고 `python3 tools/fortran_guide.py examples`로 같은 경고가 나오는지 확인했다(gfortran 15.2). |
| 2026-11-21 | 경고 | ch21/common_swap.f 의 경고 "COMMON block"를 남긴다. | common 블록은 폐기 예정 기능이다. 순서가 어긋난 common이 값을 바꿔 읽는 사고를 보여 준다. 새 코드에는 쓰지 말라는 경고를 독자가 직접 보게 한다. | 경고가 나오지 않게 고치기(옛 문법을 보여 주는 예제의 목적이 사라진다) | `.warning`에 적고 `python3 tools/fortran_guide.py examples`로 같은 경고가 나오는지 확인했다(gfortran 15.2). |
| 2026-11-21 | 경고 | ch21/block_data.f 의 경고 "BLOCK DATA construct와 COMMON block"를 남긴다. | block data와 common은 폐기 예정 기능이고, 둘이 짝으로 쓰인다. 새 코드에는 쓰지 말라는 경고를 독자가 직접 보게 한다. | 경고가 나오지 않게 고치기(옛 문법을 보여 주는 예제의 목적이 사라진다) | `.warning`에 적고 `python3 tools/fortran_guide.py examples`로 같은 경고가 나오는지 확인했다(gfortran 15.2). |
| 2026-11-21 | 경고 | ch21/equiv_overlay.f 의 경고 "EQUIVALENCE statement"를 남긴다. | equivalence는 폐기 예정 기능이다. 새 코드에는 쓰지 말라는 경고를 독자가 직접 보게 한다. | 경고가 나오지 않게 고치기(옛 문법을 보여 주는 예제의 목적이 사라진다) | `.warning`에 적고 `python3 tools/fortran_guide.py examples`로 같은 경고가 나오는지 확인했다(gfortran 15.2). |
| 2026-11-21 | 경고 | ch21/char_star.f 의 경고 "Old-style character length"를 남긴다. | character*n 형식은 폐기 예정 기능이다. 새 코드에는 쓰지 말라는 경고를 독자가 직접 보게 한다. | 경고가 나오지 않게 고치기(옛 문법을 보여 주는 예제의 목적이 사라진다) | `.warning`에 적고 `python3 tools/fortran_guide.py examples`로 같은 경고가 나오는지 확인했다(gfortran 15.2). |
| 2026-11-21 | 경고 | ch21/stmt_function.f 의 경고 "Statement function"를 남긴다. | 문 함수는 폐기 예정 기능이다. 새 코드에는 쓰지 말라는 경고를 독자가 직접 보게 한다. | 경고가 나오지 않게 고치기(옛 문법을 보여 주는 예제의 목적이 사라진다) | `.warning`에 적고 `python3 tools/fortran_guide.py examples`로 같은 경고가 나오는지 확인했다(gfortran 15.2). |
| 2026-11-21 | 경고 | ch21/entry_point.f 의 경고 "ENTRY statement"를 남긴다. | entry는 폐기 예정 기능이다. 새 코드에는 쓰지 말라는 경고를 독자가 직접 보게 한다. | 경고가 나오지 않게 고치기(옛 문법을 보여 주는 예제의 목적이 사라진다) | `.warning`에 적고 `python3 tools/fortran_guide.py examples`로 같은 경고가 나오는지 확인했다(gfortran 15.2). |
| 2026-11-21 | 경고 | ch19/warn_demo.f90 의 경고 "Unused variable, Change of value in conversion, Equality comparison for REAL, Unused dummy argument"를 남긴다. | -Wall과 -Wextra가 켜는 경고가 실제로 어떤 메시지를 내는지 한 파일로 보여 주는 장이므로 경고가 나와야 한다. | 경고가 나오지 않게 고치기(예제의 목적이 사라진다) | `.warning`에 적고 `python3 tools/fortran_guide.py examples`로 같은 경고가 나오는지 확인했다(gfortran 15.2). |
| 2026-11-21 | 경고 | ch19/implicit_iface.f90 의 경고 "Procedure called with an implicit interface"를 남긴다. | -Wimplicit-interface는 -Wall에 들어 있지 않아 따로 켜야 하는 경고임을 보여 주는 예제다. | 경고가 나오지 않게 고치기(예제의 목적이 사라진다) | `.warning`에 적고 `python3 tools/fortran_guide.py examples`로 같은 경고가 나오는지 확인했다(gfortran 15.2). |
| 2026-11-21 | 예제 | 경고 하나를 보여 주는 것이 목적인 짧은 예제(4장 `unused`, 6장 `constant_division`·`real_to_integer`·`cmplx_kind`, 7장 `float_equal`)는 `.flags`에 `-Werror=<경고 이름>`을 주고 `.compile-error`로 경고 문구를 검사한다. 본문에는 `-Werror` 없이 받은 실제 경고를 싣는다. | 경고가 나오는지 기계가 확인하면서 경고 0 규칙의 예외(`.warning`)를 늘리지 않는다. | `.warning`과 결정 로그 행 추가 | examples 검사 |
| 2026-11-21 | 예제 | 여러 파일로 된 예제를 위해 옆 파일 `.with`를 더했다. `program` 문이 없는 소스는 `-c`로만 컴파일하고 실행하지 않는다. | 4장의 모듈 파일과 주 프로그램, fpm이 만든 `src`와 `app` 파일이 셸 heredoc과 `text` 블록에 있어 검사를 받지 않았다. Fortran 코드를 `fortran` 블록으로만 쓴다는 규칙을 지키려면 여러 파일 예제를 검사기가 다뤄야 한다. | heredoc 유지(코드가 검사 밖에 남는다) | `main.with`, `area_calc_app.with`로 두 쌍을 컴파일하고 출력을 비교했다. |
| 2026-11-21 | 본문 | 7장의 `logical` 선언과 12장의 `read`/`write` 형태 설명을 `text` 블록에서 빼서 예제 발췌(excerpt)와 본문 문장으로 바꿨다. | 위와 같은 이유. | | lint |
| 2026-11-21 | 용어 | kind 상수 이름은 모든 장에서 `dp`로 통일한다. 18장 초안의 `wp`를 `dp`로 바꿨다. | 5장부터 `dp`를 쓰고 있어 한 장만 다른 이름을 쓰면 독자가 다른 개념으로 오해한다. | `wp`(working precision)로 통일 | lint, examples |
| 2026-11-21 | 용어 | 표준의 Annex는 "부속서"로 쓴다. 21장 초안의 "부록 B.3.10" 같은 표기를 "표준 부속서 B.3.10"으로 바꿨다. | 이 가이드의 부록 A, B와 헷갈린다. | | grep |
| 2026-11-21 | 원전 | 원본과 다르게 쓴 곳: 원본의 "call-by-reference"는 표준의 인수 결합(15.5.2.3)으로 고쳐 썼다(11장). "단항 -가 다른 연산자보다 우선"은 표 10.1에 맞게 고쳤다(`-a**2`는 -4, 6장). "예약어는 변수 이름으로 못 쓴다"는 Fortran에 예약어가 없으므로 고쳤다(5장). 너비 없는 `F`, `E` 형식은 표준이 아니므로 `F8.3`, `E12.5`로 바꾸고, "5-9는 올림"은 gfortran이 정확한 중간값을 짝수 쪽으로 반올림하는 것을 보이며 고쳤다(13장). "Fortran 77은 재귀를 허용하지 않는다"는 이전 표준의 상황이고 Fortran 2018에서는 기본으로 재귀 가능하다고 적었다(11장, N2161 5.26). | 원본은 1995-97년 Fortran 77 기준이라 지금 표준이나 컴파일러와 맞지 않는 서술이 있다. | 원본 서술을 그대로 옮기기 | 각 장의 예제와 표준 조항 |
| 2026-11-21 | 원전 | 원본 18장의 Netlib 전자우편과 ftp 접근, 상용 라이브러리 평가("NR은 NAG나 IMSL에 비교가 안 된다"), 원본 19장의 "가능성 높은 조건을 먼저" 지침은 지금도 맞는지 확인할 출처가 없어 뺐다. | 확인하지 못한 주장은 쓰지 않는다는 규칙. | | |
| 2026-11-21 | CI | 예제 검사를 Ubuntu 24.04 컨테이너(podman)의 gfortran 14.2와 참조 `libblas-dev`, `liblapack-dev`로 미리 돌려 CI 환경에서도 통과하는지 확인했다. 로컬 BLAS는 alternatives로 OpenBLAS를 가리킨다. | `.compile-error`, `.run-error`, `.warning` 문구가 판에 따라 다를 수 있다. | | 173개 소스 모두 통과(14.2.0, 15.2.0) |
| 2026-11-21 | 검증 | 22개 장을 390px 폭 헤드리스 Chromium으로 열어 문서 폭이 화면을 넘지 않는지, `pre`, `table`, `img`가 오른쪽으로 넘치지 않는지 확인했다. 기존 페이지는 이 브랜치 전후 빌드 결과를 비교해 사이드바 링크 한 줄과 빌드 시각 말고는 바뀌지 않았음을 확인했다. | | | 일회성 확인(스크립트는 저장소에 두지 않았다) |
| 2026-11-21 | 원전 | 22개 장을 선행 한국어판 본문과 한글 14글자 단위로 대조해 겹치는 문자열이 없음을 확인했다. | 선행판 문장을 가져오지 않는다는 지시를 확인하는 방법이다. | | 겹침 0건 |

## 확인한 출처

| 출처 | 확인한 내용 |
|---|---|
| Stanford Fortran 77 Tutorial, https://web.stanford.edu/class/me200c/tutorial_77/ (2026-11-21 내려받음) | 서문의 저자, 수정자, 이용 허락 문구, 저작권 표기 "Copyright © 1995-7 by Stanford University. All rights reserved.", 장 구성 |
| 오병성 역 Fortran Tutorial, http://seismic.yonsei.ac.kr/fortran/ (EUC-KR, 2026-11-21 내려받음) | 표지의 "Copyright © 1999. All rights reserved. 충남대학교 물리학과 오 병성", 장 구성과 용어 |
| Fortran 2018 최종 작업 초안 J3/18-007r1, https://j3-fortran.org/doc/year/18/18-007r1.pdf | 이름 63자(C601), 자유 형식 132자와 이어지는 줄 255개(6.3.2), 고정 형식 열 규칙(6.3.3), 암시적 타입(8.7), 초기화가 주는 save(8.4, 8.6.7), 모듈 변수의 save(8.5.16), 연산자 우선순위(표 10.1), 정수 나눗셈(10.1.5.2.2), 피연산자 평가 생략(10.1.7), 대입과 자동 재할당(10.2.1.3), `where`(10.2.3.2), do 반복 횟수(11.1.7.4.1), `select case`(11.1.9), 목록 지시 입출력(13.10), 편집 기술자와 형식 되풀이(13.3, 13.4, 13.7), 인수 결합(15.5.2.3, 15.5.2.13), 명시적 인터페이스가 필요한 경우(15.4.2.2), pure와 elemental(15.7, 15.8), 파생 타입(7.5), 부속서 B의 삭제·폐기 예정 기능 |
| John Reid, The new features of Fortran 2018 (WG5 N2161) | 기본 재귀와 `non_recursive`(5.26), 산술 if와 비블록 do 삭제(5.32), common·equivalence·block data·문번호 do 폐기 예정(5.33) |
| WG5 N1891(Fortran 2008 새 기능), N2212(Fortran 2023 새 기능), WG5 표준 페이지 https://wg5-fortran.org/ | 표준의 판, ISO 번호, 발행 시기, 무제한 반복 형식과 모듈 변수 save가 Fortran 2008에서 들어온 것 |
| gfortran 매뉴얼 https://gcc.gnu.org/onlinedocs/gfortran/ (Error and Warning Options, Code Gen Options, Fortran Dialect Options, Debugging Options, ISO_FORTRAN_ENV, Directory Options, Fortran 2018 status) | `-std`, `-Wall`과 `-Wextra`가 켜는 경고, `-Wimplicit-interface`, `-fcheck` 값, `-ffpe-trap`, `-finit-real`, `-fno-backtrace`, `-fimplicit-none`, `-std=legacy`와 `-fallow-argument-mismatch`, `-J`/`-I`, `-fexternal-blas`, `iso_fortran_env` 상수 |
| fortran-lang.org (quickstart, best practices, install_gfortran, compilers), fpm 문서 https://fpm.fortran-lang.org/ | gfortran 설치 방법, 스타일 지침, fpm 명령과 `fpm.toml`; fpm 0.12.0으로 `fpm new`, `build`, `run`, `test`를 직접 실행해 출력 확인 |
| Netlib BLAS, LAPACK, LAPACK Users' Guide, `dgemv.f`, `dgemm.f`, `dgesv.f` 헤더 | BLAS 수준과 이름 규칙, `lda`, `dgesv`의 `info`, LAPACK 3.12.1, Users' Guide 3판 |
| IBM 704 FORTRAN 설명서(1956), Computer History Museum 아카이브 | 이름 "Mathematical Formula Translating System" |
| NAG, Perforce IMSL, Numerical Recipes, NIST GAMS 사이트 | 20장의 상용 라이브러리 현황 |
| Open Library ISBN 조회 | 22장의 책 서지 정보 |

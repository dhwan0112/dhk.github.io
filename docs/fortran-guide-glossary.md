# 모던 Fortran 가이드 용어표

가이드 본문(`fortran/*.md`)은 아래 표의 한국어 표기를 쓴다. 셋째 열의 표기는 `python3 tools/fortran_guide.py lint`가 코드 블록과 인라인 코드 밖에서 찾아 오류로 보고한다. 원어를 괄호로 함께 적는 것은 그 장에서 처음 나올 때 한 번이면 된다.

| 영어 | 한국어 | 쓰지 않는 표기 |
|---|---|---|
| array | 배열 | 어레이 |
| array section | 배열 부분 | 배열 섹션, 부분 배열 |
| whole-array operation | 배열 전체 연산 | |
| element | 원소 | 엘리먼트 |
| shape | 형상 | |
| rank | 차원 수 | 랭크 |
| extent | 크기 | |
| column-major order | 열 우선 순서 | 컬럼 메이저, 열 주도 |
| leading dimension | 선행 차원 | 리딩 차원 |
| allocatable array | 할당 가능 배열 | 동적 배열 |
| assumed-shape array | 가정 형상 배열 | 형상 인계 배열, 모양 가정 배열 |
| assumed-size array | 가정 크기 배열 | 크기 인계 배열 |
| explicit-shape array | 명시 형상 배열 | |
| subprogram | 부프로그램 | 서브프로그램, 하위 프로그램 |
| procedure | 프로시저 | 프로시져 |
| subroutine | 서브루틴 | 서브 루틴 |
| function | 함수 | |
| intrinsic procedure | 내장 프로시저 | 고유 함수, 본래 함수 |
| intrinsic function | 내장 함수 | 내재 함수 |
| internal procedure | 내부 프로시저 | |
| module | 모듈 | |
| module procedure | 모듈 프로시저 | |
| dummy argument | 가인수 | 더미 인수, 형식 인수, 형식 인자 |
| actual argument | 실인수 | 실제 인자, 실 인자 |
| argument | 인수 | 인자 |
| explicit interface | 명시적 인터페이스 | 명시 인터페이스 |
| implicit interface | 암시적 인터페이스 | 묵시적 인터페이스 |
| interface block | 인터페이스 블록 | |
| implicit typing | 암시적 타입 지정 | 묵시적 형, 암묵적 타입 |
| type | 타입 | 자료형 |
| intrinsic type | 내장 타입 | 기본형 |
| derived type | 파생 타입 | 유도 타입, 유도형, 사용자 정의형 |
| component | 성분 | 컴포넌트, 멤버 변수 |
| type-bound procedure | 타입 결합 프로시저 | |
| kind type parameter | kind 매개변수 | 카인드, 종류 매개변수 |
| named constant | 이름 붙은 상수 | 명명 상수 |
| attribute | 속성 | |
| declaration | 선언 | |
| assignment | 대입 | 지정문 |
| allocation | 할당 | |
| expression | 식 | 수식문 |
| logical expression | 논리식 | |
| relational operator | 관계 연산자 | 비교 연산자 |
| integer division | 정수 나눗셈 | |
| double precision | 배정밀도 | 더블 프리시전, 2배 정밀도 |
| single precision | 단정밀도 | |
| character string | 문자열 | 스트링 |
| statement | 문 | |
| construct | 구문 | |
| loop | 반복문 | 루프 |
| statement label | 문번호 | 문장 번호, 라벨 번호, 레이블 번호 |
| free source form | 자유 형식 | 자유 양식, 프리 폼 |
| fixed source form | 고정 형식 | 고정 양식, 픽스드 폼 |
| obsolescent feature | 폐기 예정 기능 | 구식 기능 |
| deleted feature | 삭제된 기능 | |
| common block | common 블록 | 공통 블록, 커먼 블록 |
| format statement | 형식문 | 포맷문, 서식문, 출력 형식문 |
| format specification | 형식 지정 | 포맷 문자열 |
| edit descriptor | 편집 기술자 | 편집 서술자, 포맷 코드 |
| list-directed input/output | 목록 지시 입출력 | 리스트 지향, 자유 형식 입출력 |
| unit | 장치 번호 | 유닛 |
| record | 레코드 | |
| end of file | 파일 끝 | |
| compiler | 컴파일러 | |
| link | 링크 | |
| runtime check | 런타임 검사 | 실행 시간 검사 |
| warning | 경고 | |
| package manager | 패키지 관리자 | 패키지 매니저 |
| standard | 표준 | |
| host association | 호스트 연관 | |
| use association | use 연관 | |

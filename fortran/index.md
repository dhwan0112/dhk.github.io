---
title: 서문
order: 1
permalink: /fortran/
---

이 가이드는 Fortran으로 과학 계산 프로그램을 처음 쓰는 사람을 위한 입문서다. Stanford 대학의 Fortran 77 Tutorial을 바탕으로 하되, 내용은 지금 쓰는 Fortran(자유 형식, Fortran 2008과 2018 표준)에 맞춰 새로 썼다.

## 이 가이드가 다루는 것

원본과 마찬가지로 완전한 참고서가 아니다. 자주 쓰는 기능만 골랐고 세부 규칙은 많이 생략했다. 예제는 과학 계산, 그중에서도 선형대수 쪽에 맞췄다.

- 2장부터 4장까지는 Fortran이 어떤 언어인지, 소스 파일의 모양, 컴파일러와 fpm 설치를 다룬다.
- 5장부터 10장까지는 변수와 타입, 식, 조건문, 반복문, 배열을 다룬다.
- 11장부터 17장까지는 부프로그램과 모듈, 입출력, 파생 타입으로 프로그램을 나누고 묶는 방법을 다룬다.
- 18장부터 20장까지는 프로그래밍 스타일, 디버깅, BLAS와 LAPACK 연결을 다룬다.
- 부록 A는 옛 Fortran 77 코드를 읽을 때 마주치는 문법을 모았다. 새 코드에 쓰라는 뜻이 아니다.

본문의 예제는 모두 실제 파일로 저장소의 [examples/fortran](https://github.com/dhwan0112/dhk.github.io/tree/main/examples/fortran)에 있다. 모든 예제는 gfortran에서 `-std=f2018 -Wall -Wextra`로 컴파일하고 실행해 본문의 결과와 비교했다.

## 이 가이드를 읽는 방법

장마다 처음 한두 문장에 무엇을 배우는지 적고, 설명과 예제를 거쳐 흔한 실수로 끝낸다. 예제는 직접 입력해 컴파일해 보는 편이 좋다. 컴파일 방법은 [4장](/fortran/04-environment/)에 있다.

출력 예시는 gfortran으로 실행한 결과다. `print *`처럼 출력 모양을 컴파일러에 맡기는 문장은 다른 컴파일러에서 공백 수가 다를 수 있다.

## 출처와 저작권

### 원본

- 제목: Fortran 77 Tutorial
- 주소: https://web.stanford.edu/class/me200c/tutorial_77/
- 저자: Erik Boman (Stanford, 1995년 12월)
- 수정: Sarah T. Whitlock (Stanford, 1997년 1월), Paul H. Hargrove (Stanford, 1997년 12월)
- 저작권 표기: Copyright © 1995-7 by Stanford University. All rights reserved.

원본 서문에 따르면 이 튜토리얼은 Erik Boman이 1996년 겨울 학기 Stanford 대학 강의 SCCM-001-F: Introduction to Fortran에 쓰려고 만들었고, 이후 Sarah T. Whitlock과 Paul H. Hargrove가 해마다 다른 과목 번호로 열린 Fortran 강의에 맞게 고쳤다. 원본의 개요는 T.F. Coleman과 C. Van Loan의 "Handbook for Matrix Computations"(SIAM)를, Fortran 90을 다룬 부분은 L. Nyhoff와 S. Leestma의 "FORTRAN 77 for Engineers and Scientists with an Introduction to Fortran 90"(Prentice Hall)을 바탕으로 했다.

원본의 이용 조건은 서문에 다음과 같이 적혀 있다.

> Permission to use this tutorial for educational and other non-commercial purposes is granted provided all author and copyright information is retained.

교육과 그 밖의 비상업적 목적에 한해, 저자와 저작권 정보를 모두 남긴다는 조건으로 이용을 허락한다는 뜻이다.

### 선행 한국어판

- 제목: Fortran Tutorial 한국어판
- 옮긴이: 오병성 (충남대학교 물리학과, 1999)
- 주소: http://seismic.yonsei.ac.kr/fortran/ (옮긴이가 아닌 제3자가 올린 사본)
- 저작권 표기: Copyright © 1999. All rights reserved. 충남대학교 물리학과 오 병성

선행 한국어판은 장 구성과 용어를 대조하는 데만 참고했다. 이 가이드의 문장은 선행판에서 가져오지 않았다.

### 이 가이드

이 가이드는 위 원본을 현대 Fortran에 맞게 고쳐 쓴 2차 저작물이며, 비상업적 교육 목적으로만 공개한다. 원본의 이용 조건에 따라 위의 저자와 저작권 정보를 그대로 남긴다. 이 가이드를 옮기거나 고쳐 쓸 때도 이 절의 정보를 함께 남겨야 한다.

원본과 달라진 점은 다음과 같다.

- 고정 형식 대신 자유 형식(`.f90`)으로 쓰고, Fortran 2008과 2018 표준의 문법을 쓴다.
- 원본 4장의 Stanford Unix 환경 설명과 18.3절의 강의 계정 경로는 빼고, gfortran과 fpm 설치로 바꿨다.
- common 블록을 다룬 장은 모듈로 데이터를 공유하는 장으로 바꾸고, common 블록과 `block data`, `goto`, 고정 형식은 부록 A에서 옛 코드를 읽는 법으로 다룬다.
- 파생 타입과 할당 가능 배열처럼 Fortran 77에 없던 기능을 더했다.

틀린 곳은 [GitHub 이슈](https://github.com/dhwan0112/dhk.github.io/issues)로 알려 주면 고친다.

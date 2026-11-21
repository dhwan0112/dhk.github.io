---
title: 더 읽을 자료
order: 22
permalink: /fortran/22-further-reading/
---

이 부록은 가이드를 읽은 뒤 더 찾아볼 표준 문서, 컴파일러 문서, 학습 자료, 라이브러리, 책을 모은다. 적힌 웹 주소는 2026년 11월 21일에 모두 열리는 것을 확인했다.

## 표준 문서

- [WG5](https://wg5-fortran.org/): Fortran 표준을 다루는 ISO/IEC JTC1/SC22/WG5의 사이트다. [Fortran 2023](https://wg5-fortran.org/f2023.html) 쪽은 현행 표준이 2023년 11월에 발행된 ISO/IEC 1539:2023이고 ISO에서 구입할 수 있다고 안내한다. [Fortran 2018](https://wg5-fortran.org/f2018.html) 쪽에도 문서 목록이 있다.
- [J3](https://j3-fortran.org/): Fortran 표준 위원회 J3의 사이트다. [Fortran 2018 최종 작업 초안(J3/18-007r1)](https://j3-fortran.org/doc/year/18/18-007r1.pdf)을 내려받을 수 있다. 이 가이드는 문법을 확인할 때 이 초안을 썼다.
- John Reid, [The New Features of Fortran 2018](https://wg5-fortran.org/N2151-N2200/N2161.pdf)(WG5 N2161): Fortran 2008을 기준으로 달라진 점을 요약한 문서이며, 저자는 이 글이 WG5가 승인한 공식 문서가 아니라고 밝힌다.
- John Reid, [The New Features of Fortran 2023](https://wg5-fortran.org/N2201-N2250/N2212.pdf)(WG5 N2212): 같은 저자의 Fortran 2023 판이다.

## 컴파일러와 도구

- [gfortran 매뉴얼](https://gcc.gnu.org/onlinedocs/gfortran/): 이 가이드가 쓴 옵션의 설명이 모두 여기에 있다. [언어 방언 옵션](https://gcc.gnu.org/onlinedocs/gfortran/Fortran-Dialect-Options.html)에 `-std`가, [경고 옵션](https://gcc.gnu.org/onlinedocs/gfortran/Error-and-Warning-Options.html)에 `-Wall`과 `-Wextra`가, [코드 생성 옵션](https://gcc.gnu.org/onlinedocs/gfortran/Code-Gen-Options.html)에 `-fcheck`와 `-finit-real`이, [디버깅 옵션](https://gcc.gnu.org/onlinedocs/gfortran/Debugging-Options.html)에 `-ffpe-trap`과 `-fno-backtrace`가 있다.
- [fortran-lang.org의 컴파일러 목록](https://fortran-lang.org/compilers/): gfortran 말고 다른 컴파일러를 찾을 때 본다.
- [fpm(Fortran Package Manager)](https://fpm.fortran-lang.org/): Fortran의 패키지 관리자다. 프로젝트를 만들고 컴파일해서 실행하는 일까지 한다. [튜토리얼](https://fpm.fortran-lang.org/tutorial/hello-fpm.html)이 첫 프로젝트를 만드는 과정을 보여 준다.

## 학습 자료와 모범 사례

- [fortran-lang.org의 학습 자료](https://fortran-lang.org/learn/): 설치부터 문법, 빌드까지 모아 둔 입구다. [빠른 시작](https://fortran-lang.org/learn/quickstart/)과 [프로그램 빌드](https://fortran-lang.org/learn/building_programs/)가 있다.
- [Fortran 모범 사례](https://fortran-lang.org/learn/best_practices/): [18장](/fortran/18-style/)의 확인 출처다. 스타일 가이드, 모듈과 프로그램, 다차원 배열, 정수 나눗셈을 다룬다.
- [Fortran Discourse](https://fortran-lang.discourse.group/): Fortran 커뮤니티의 토론 게시판이다.
- [Fortran 표준 라이브러리 stdlib](https://stdlib.fortran-lang.org/)와 [패키지 목록](https://fortran-lang.org/packages/): 직접 짜기 전에 이미 있는 패키지를 찾아본다.

## 수치 라이브러리

[20장](/fortran/20-blas-lapack/)에서 다룬 라이브러리의 자료다.

- [Netlib](https://www.netlib.org/): 수학 소프트웨어 저장소다.
- [BLAS](https://www.netlib.org/blas/)와 [LAPACK](https://www.netlib.org/lapack/): 기준 구현과 설명이다. LAPACK 페이지는 현재 판이 3.12.1이라고 적고 있다.
- [LAPACK Users' Guide](https://www.netlib.org/lapack/lug/): LAPACK의 해설서다. 3판(SIAM, 1999)이다.
- [Reference-LAPACK의 GitHub 저장소](https://github.com/Reference-LAPACK/lapack): LAPACK 페이지가 소스 저장소로 안내하는 곳이다.
- [OpenBLAS](https://www.openmathlib.org/OpenBLAS/): 최적화한 BLAS 구현이다.
- [GAMS](https://gams.nist.gov/): NIST의 수학 소프트웨어 안내서다.

## 책

- Michael Metcalf, John Reid, Malcolm Cohen, *Modern Fortran Explained: Incorporating Fortran 2018*, Oxford University Press, 2018. ISBN 978-0-19-881189-3.
- Michael Metcalf, John Reid, Malcolm Cohen, Reinhold Bader, *Modern Fortran Explained: Incorporating Fortran 2023*, Oxford University Press, 2023. ISBN 978-0-19-887657-1.
- Milan Curcic, *Modern Fortran: Building efficient parallel applications*, Manning Publications, 2020. ISBN 978-1-61729-528-7. [출판사 페이지](https://www.manning.com/books/modern-fortran).

## 이 가이드의 원본

이 가이드는 Stanford의 [Fortran 77 Tutorial](https://web.stanford.edu/class/me200c/tutorial_77/)을 바탕으로 현대 Fortran에 맞게 새로 썼다.

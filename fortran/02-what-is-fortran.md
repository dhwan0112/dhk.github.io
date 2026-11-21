---
title: Fortran이란
order: 2
permalink: /fortran/02-what-is-fortran/
---

이 장에서는 Fortran이라는 이름이 어디서 왔는지, 표준이 어떻게 바뀌어 왔는지, 표준과 컴파일러 확장이 어떻게 다른지, 그리고 지금도 Fortran을 쓰는 이유를 본다.

## 이름의 유래

Fortran은 1950년대에 IBM에서 시작된 프로그래밍 언어다. 1956년 10월자 IBM 704용 설명서는 이 시스템을 "The IBM Mathematical Formula Translating System FORTRAN"이라고 소개한다. 이름은 수식(formula)을 번역(translation)한다는 뜻의 FORmula TRANslation에서 왔다.

초기에는 FORTRAN으로 대문자로 썼다. 표준을 관리하는 WG5의 페이지는 FORTRAN 66과 FORTRAN 77은 대문자로, Fortran 90부터는 Fortran으로 쓴다. 이 가이드도 Fortran으로 쓴다.

## 표준의 변천

Fortran은 국제 표준이 있는 언어다. 표준은 ISO/IEC 산하 JTC 1/SC 22의 작업반 WG5가 관리한다. 표준은 몇 해마다 개정되고, 개정판은 발행 연도를 붙여 Fortran 90, Fortran 2018처럼 부른다. FORTRAN 66은 ANSI 표준 X3.9-1966으로 먼저 나왔고, 아래 표의 ISO 번호는 `ISO R 1539-1972`다. FORTRAN 77의 ISO 번호는 `ISO 1539-1980`이다. 그래서 이 두 판은 이름의 숫자와 공식 번호의 연도가 다르다.

| 비공식 이름 | 공식 번호 | 눈에 띄는 변화 |
|---|---|---|
| FORTRAN 66 | ISO R 1539-1972 | 표준으로 정해진 첫 판 |
| FORTRAN 77 | ISO 1539-1980 | 이 가이드의 원본(Stanford Fortran 77 Tutorial)이 다룬 판 |
| Fortran 90 | ISO/IEC 1539:1991 | 자유 형식 도입 |
| Fortran 95 | ISO/IEC 1539-1:1997 | Fortran 90의 작은 확장 |
| Fortran 2003 | ISO/IEC 1539-1:2004 | 큰 확장. 객체 지향 기능과 C와의 상호 운용 |
| Fortran 2008 | ISO/IEC 1539-1:2010 | 병렬 계산용 `coarray`가 가장 큰 확장. 서브모듈, `do concurrent`, `contiguous` 속성 |
| Fortran 2018 | ISO/IEC 1539-1:2018 | 기술 명세 ISO/IEC TS 29113:2012(C와의 상호 운용 확장)와 ISO/IEC TS 18508:2015(병렬 기능 추가)를 표준에 포함 |
| Fortran 2023 | ISO/IEC 1539:2023 | 훨씬 긴 문 길이, 조건식, 도 단위 삼각함수 |
| Fortran 2028 | 작업 중 | WG5가 다음 개정판에 붙인 작업명 |

각 판은 앞 판의 확장이다. Fortran 2018 표준은 몇 가지 예외와 삭제된 기능(deleted feature)을 빼면 Fortran 77, 90, 95, 2003, 2008을 따르는 프로그램이 그대로 Fortran 2018을 따른다고 적는다. 그래서 오래전에 쓴 표준 코드도 지금의 컴파일러로 컴파일되는 경우가 많다.

Fortran 2018 부속서 B가 삭제된 기능으로 드는 것은 Fortran 90의 실수 `do` 변수, `pause` 문, `assign` 문과 지정 `go to` 문, `H` 편집 기술자, 그리고 Fortran 2008의 산술 `if` 문과 블록이 아닌 `do` 구문이다. 또 `common` 블록, `equivalence` 문, 문번호를 쓰는 `do` 반복문은 Fortran 2018에서 폐기 예정 기능(obsolescent feature)이 되었다. 옛 코드에서 이런 기능을 만났을 때 읽는 법은 [부록 A](/fortran/21-legacy-code/)에서 다룬다.

WG5는 2023년 11월에 Fortran 2023이 발행되었다고 적고, 그 뒤 개정판의 작업명을 Fortran 2028이라고 부른다. 2026년 7월 WG5 소식에는 Fortran 2028 위원회 초안(committee draft)이 올라와 있지만 공개 문서는 아니다. 이 가이드는 Fortran 2018을 기준으로 쓰고, 컴파일 옵션도 `-std=f2018`을 쓴다.

## 표준과 컴파일러 확장

컴파일러는 표준을 구현하면서 표준에 없는 기능도 함께 받아 주는 경우가 많다. 이를 컴파일러 확장(extension)이라고 한다. 옛 코드에 흔한 `real*8`이 그 예다. `real*8`은 8바이트 실수라는 뜻으로 쓰이지만 Fortran 표준에는 없다.

<!-- file: ch02/real8.f90 -->
```fortran
program real8
  implicit none
  real*8 :: x

  x = 2.5d0
  print '(f6.2)', x
end program real8
```

gfortran은 기본값(`-std=gnu`)에서 표준 전체에 gfortran 확장을 더한 언어를 받아 들인다. 그래서 위 프로그램은 옵션 없이 컴파일된다. 표준만 허용하려면 `-std=f2018`을 준다. 표준에 없는 문법은 그때 오류가 된다. 다음은 gfortran 15.2의 메시지다.

```text
real8.f90:3:9:

    3 |   real*8 :: x
      |         1
Error: GNU Extension: Nonstandard type declaration REAL*8 at (1)
```

`x`의 선언이 실패했으므로 뒤이어 `x`에 암시적 타입이 없다는 오류가 따라온다.

확장을 쓴 코드는 gfortran에서만 돌아갈 수 있다. 다른 컴파일러가 같은 확장을 같은 뜻으로 받아 준다는 보장이 없다. 표준만 쓴 코드는 표준을 구현한 어느 컴파일러에서나 같은 뜻을 가진다. 이 가이드의 예제는 모두 `-std=f2018`로 컴파일되는 표준 코드다. 8바이트 실수는 `real*8` 대신 kind 매개변수로 쓰는데, 이는 [5장](/fortran/05-variables/)에서 다룬다.

## 지금도 Fortran을 쓰는 이유

Fortran은 수치 계산과 과학 계산을 위해 만들어진 언어이고, 그 목적에 맞는 장점이 지금도 남아 있다.

**배열 연산.** 배열은 언어의 기본 요소다. 반복문 없이 배열 전체를 한 식으로 계산할 수 있다.

<!-- file: ch02/array_sum.f90 -->
```fortran
program array_sum
  implicit none
  real :: a(4), b(4), c(4)

  a = [1.0, 2.0, 3.0, 4.0]
  b = 10.0
  c = a * 2.0 + b
  print '(4f6.1)', c
  print '(f6.1)', sum(c)
end program array_sum
```

<!-- output: ch02/array_sum.out -->
```text
  12.0  14.0  16.0  18.0
  60.0
```

`c = a * 2.0 + b`는 원소마다 계산해 `c`의 같은 위치에 넣는 식이다. 배열은 [10장](/fortran/10-arrays/)에서 자세히 다룬다.

**성능.** 표준에는 컴파일러가 최적화하기 쉽도록 프로그래머가 지키는 약속이 들어 있다. 가인수와 연결된 변수는 그 가인수를 통해서만 바꿀 수 있다는 제한(Fortran 2018 표준 15.5.2.13), `do concurrent`의 반복 사이에 데이터 의존이 없어야 한다는 제한, 메모리에 연속으로 놓인다는 것을 알리는 `contiguous` 속성이 그런 예다. 표준은 `do concurrent`의 제한을, 컴파일러가 프로그램만 보아서는 알 수 없어 어렵거나 불가능했을 최적화를 허용하기 위한 것이라고 설명한다. fortran-lang.org도 Fortran을 고성능 병렬 프로그래밍 언어로 소개한다.

**오래된 과학 코드.** 선형대수 라이브러리 LAPACK은 netlib 소개에 따르면 Fortran 90으로 쓰여 있고, BLAS의 Fortran 77 참조 구현도 netlib에서 받을 수 있다. 이미 쓰여 있는 라이브러리와 프로그램을 다른 언어로 옮기려면 비용이 든다. 그래서 새 프로그램이 이 라이브러리를 부르고([20장](/fortran/20-blas-lapack/)), 옛 Fortran 코드를 읽고 고쳐야 하는 일도 생긴다.

**표준과 호환성.** 앞에서 본 것처럼 표준은 ISO/IEC 문서이고 새 판이 옛 판의 코드를 대부분 그대로 받아 준다. 표준만 쓰면 컴파일러를 바꾸거나 새 판으로 올려도 프로그램이 같은 뜻을 가진다.

## 흔한 실수

- `real*8`, `integer*4`처럼 컴파일러 확장을 표준 문법으로 오해한다. gfortran은 기본값에서 이를 조용히 받아 주므로 `-std=f2018`을 주기 전에는 드러나지 않는다.
- 판 이름의 숫자와 ISO 번호의 연도를 같다고 여긴다. FORTRAN 66의 ISO 번호는 1972년이고 FORTRAN 77은 1980년이다.
- Fortran 77 시절의 고정 형식 규칙이 지금도 적용된다고 여긴다. 자유 형식은 Fortran 90에서 도입되었고 이 가이드의 코드는 모두 자유 형식이다.

---
title: 환경 준비
order: 4
permalink: /fortran/04-environment/
---

이 장에서는 gfortran을 설치하고, 소스 파일 하나와 여러 개를 컴파일해 실행하는 법을 익힌다. 이 가이드에서 권하는 컴파일 옵션과, 프로젝트를 한꺼번에 빌드해 주는 패키지 관리자(package manager) fpm도 소개한다.

## gfortran 설치

Fortran 프로그램은 컴파일러(compiler)가 기계가 실행할 수 있는 파일로 바꾸어야 돌아간다. 이 가이드는 GNU 컴파일러 모음의 Fortran 컴파일러 gfortran을 쓴다. 설치 명령은 환경마다 다르다.

Ubuntu와 Debian에서는 `apt`로 설치한다.

```sh
sudo apt install gfortran
```

macOS에서는 Homebrew의 `gcc` 패키지가 gfortran을 포함한다.

```sh
brew install gcc
```

conda를 쓴다면 conda-forge 채널의 패키지를 설치한다. Linux, macOS, Windows에서 모두 쓸 수 있다.

```sh
conda install conda-forge::gfortran
```

Windows에서 Unix 같은 개발 환경이 필요하면 fortran-lang.org는 WSL(Windows Subsystem for Linux)을 권한다. 관리자 권한 PowerShell에서 `wsl --install`을 실행하고 재부팅하면 Linux 배포판이 설치된다. 배포판이 Ubuntu나 Debian이면 그 안에서 위의 `apt` 명령을 그대로 쓴다.

```sh
wsl --install
```

MSYS2를 쓰는 방법도 있다. MSYS2 설치 프로그램으로 설치한 뒤 UCRT64 터미널에서 다음 명령을 실행한다.

```sh
pacman -S mingw-w64-ucrt-x86_64-gcc-fortran
```

설치를 마치면 버전을 확인한다. 출력은 환경마다 다르다.

```sh
gfortran --version
```

```text
GNU Fortran (Ubuntu 15.2.0-16ubuntu1) 15.2.0
```

이 가이드의 출력은 gfortran 15.2로 확인했다.

## 컴파일하고 실행하기

텍스트 편집기로 다음 파일을 `hello.f90`라는 이름으로 저장한다. 확장자 `.f90`는 gfortran에게 이 파일이 자유 형식이라고 알려 준다.

<!-- file: ch04/hello.f90 -->
```fortran
program hello
  implicit none

  print *, 'Hello, gfortran!'
end program hello
```

`-o` 뒤에 실행 파일의 이름을 적어 컴파일한다. 컴파일에 성공하면 아무것도 출력하지 않고 실행 파일이 생긴다.

```sh
gfortran -o hello hello.f90
./hello
```

<!-- output: ch04/hello.out -->
```text
 Hello, gfortran!
```

`-o`를 생략하면 실행 파일 이름은 `a.out`이 된다. 현재 폴더는 실행 파일을 찾는 경로에 들어 있지 않은 경우가 많으므로 `hello`가 아니라 `./hello`로 실행한다.

## 여러 파일 컴파일하기

프로그램이 커지면 소스를 여러 파일로 나눈다. 다음은 모듈 `geometry`를 `geometry.f90`에, 그것을 쓰는 주 프로그램을 `main.f90`에 둔 예다. 모듈은 [16장](../16-modules/)에서 자세히 다룬다. 여기서는 파일을 나누어 컴파일하는 방법만 본다.

`geometry.f90`:

<!-- file: ch04/geometry.f90 -->
```fortran
module geometry
  use, intrinsic :: iso_fortran_env, only: real64
  implicit none
  integer, parameter :: dp = real64
  real(dp), parameter :: pi = 3.14159265358979324_dp

contains

  function circle_area(r) result(area)
    real(dp), intent(in) :: r
    real(dp) :: area

    area = pi * r**2
  end function circle_area
end module geometry
```

`main.f90`:

<!-- file: ch04/main.f90 -->
```fortran
program main
  use geometry, only: dp, circle_area
  implicit none
  real(dp) :: r

  r = 2.0_dp
  print '(a, f10.5)', 'area = ', circle_area(r)
end program main
```

파일을 모두 한 명령에 적으면 gfortran이 차례로 컴파일하고 링크(link)한다.

```sh
gfortran -std=f2018 -Wall -Wextra geometry.f90 main.f90 -o area
./area
```

<!-- output: ch04/main.out -->
```text
area =   12.56637
```

이 명령은 내부에서 두 단계를 거친다. 먼저 소스 파일마다 오브젝트 파일(`.o`)을 만들고, 그 오브젝트 파일을 링크해 실행 파일을 만든다. `-c`를 주면 첫 단계에서 멈춘다.

```sh
gfortran -std=f2018 -Wall -Wextra -c geometry.f90
gfortran -std=f2018 -Wall -Wextra -c main.f90
gfortran geometry.o main.o -o area
```

`-c`로 모듈 파일을 컴파일하면 `geometry.f90`, `geometry.o` 말고도 `geometry.mod`가 생긴다. `.o`에는 컴파일된 코드가, `.mod`에는 모듈이 내보내는 이름과 프로시저의 인터페이스가 들어 있다. `main.f90`의 `use geometry`를 컴파일하려면 컴파일러가 `geometry.mod`를 읽어야 하므로, 모듈이 든 파일을 그 모듈을 쓰는 파일보다 먼저 컴파일해야 한다. 순서를 바꾸면 gfortran 15.2는 다음 메시지를 내고 멈춘다.

```sh
gfortran main.f90 geometry.f90 -o area
```

```text
main.f90:2:7:

    2 |   use geometry, only: dp, circle_area
      |       1
Fatal Error: Cannot open module file ‘geometry.mod’ for reading at (1): No such file or directory
compilation terminated.
```

`.mod` 파일은 기본으로 현재 폴더에 생긴다. `-J 폴더`는 `.mod`를 놓을 폴더를 정하고, `-I 폴더`는 `.mod`를 찾을 폴더를 더한다. `-J`를 준 폴더는 `use`가 찾는 폴더에도 들어간다.

```sh
mkdir build
gfortran -J build -c geometry.f90
gfortran -I build -c main.f90
```

## 권하는 컴파일 옵션

이 가이드는 모든 예제를 다음 옵션으로 컴파일한다.

```sh
gfortran -std=f2018 -Wall -Wextra 파일.f90 -o 실행파일
```

- `-std=f2018`은 Fortran 2018 표준에 없는 문법을 오류로 만든다([2장](../02-what-is-fortran/)). 이 옵션을 주지 않으면 gfortran은 자신의 확장을 조용히 받아 준다.
- `-Wall`은 피하는 것이 좋다고 판단하는 코드에 경고(warning)를 낸다. gfortran 매뉴얼에 따르면 쓰지 않는 변수(`-Wunused`), 상수끼리의 정수 나눗셈(`-Winteger-division`), 값이 달라질 수 있는 암시적 변환(`-Wconversion`)에 대한 경고가 여기에 든다.
- `-Wextra`는 `-Wall`에 더해, 실수를 `==`로 비교하는 코드(`-Wcompare-reals`) 같은 문제가 될 수 있는 용법을 알려 준다.

경고는 오류가 아니므로 컴파일은 끝까지 진행되고 실행 파일도 만들어진다. 그래도 경고는 모두 읽고 없앤다. 다음 프로그램에서 `n`은 선언만 하고 쓰지 않았다.

<!-- file: ch04/unused.f90 -->
```fortran
program unused
  implicit none
  integer :: n, total

  total = 10
  print '(i0)', total
end program unused
```

`-Wall`을 주면 gfortran 15.2는 다음 경고를 낸다.

```text
unused.f90:3:14:

    3 |   integer :: n, total
      |              1
Warning: Unused variable ‘n’ declared at (1) [-Wunused-variable]
```

런타임 검사(runtime check)와 디버깅용 옵션은 [19장](../19-debugging/)에서 다룬다.

## fpm으로 프로젝트 관리하기

파일이 늘면 컴파일 순서와 옵션을 손으로 챙기기 어렵다. fpm(Fortran Package Manager)은 소스를 읽어 모듈 의존 관계를 알아내고, 순서에 맞게 컴파일해 실행 파일을 만든다. 이 절의 출력은 fpm 0.12.0으로 확인했다.

fpm은 다음 방법 가운데 하나로 설치한다. 어느 쪽이든 `fpm --version`으로 확인한다.

```sh
pipx install fpm
brew install fpm
conda install fpm
pacman -S mingw-w64-ucrt-x86_64-fpm
```

각각 PyPI의 pipx, macOS의 Homebrew, conda-forge가 추가된 conda, MSYS2 UCRT64 터미널에서 쓰는 명령이다. fpm 저장소의 릴리스 페이지에서 실행 파일을 직접 받아도 된다.

### 프로젝트 만들기

`fpm new 이름`은 이름과 같은 폴더를 만들고 기본 구조를 채운다. 폴더 안에서 `git init`도 실행한다.

```sh
fpm new area_calc
cd area_calc
```

만들어진 폴더 구조는 다음과 같다.

```text
area_calc
├── README.md
├── app
│   └── main.f90
├── fpm.toml
├── src
│   └── area_calc.f90
└── test
    └── check.f90
```

- `src/`에는 모듈과 프로시저가 든 소스를 둔다. 라이브러리가 되는 부분이다.
- `app/`에는 실행 파일이 되는 주 프로그램을 둔다.
- `test/`에는 테스트 프로그램을 둔다.

`app/main.f90`은 `src/area_calc.f90`의 모듈을 쓰는 가장 작은 프로그램이다.

<!-- file: ch04/area_calc_app.f90 -->
```fortran
program main
  use area_calc, only: say_hello
  implicit none

  call say_hello()
end program main
```

`src/area_calc.f90`은 다음과 같다.

<!-- file: ch04/area_calc.f90 -->
```fortran
module area_calc
  implicit none
  private

  public :: say_hello
contains
  subroutine say_hello
    print *, "Hello, area_calc!"
  end subroutine say_hello
end module area_calc
```

### fpm.toml

`fpm.toml`은 프로젝트의 설명서(manifest)다. `fpm new`가 만든 파일은 다음과 같다.

```text
name = "area_calc"
version = "0.1.0"
license = "license"
author = "Jane Doe"
maintainer = "jane.doe@example.com"
copyright = "Copyright 2026, Jane Doe"
[build]
auto-executables = true
auto-tests = true
auto-examples = true
module-naming = false
[install]
library = false
test = false
[fortran]
implicit-typing = false
implicit-external = false
source-form = "free"
```

`author`, `maintainer`, `copyright`는 git 설정에 사용자 이름과 이메일이 있으면 그 값으로 채워지고, 없으면 위처럼 예시 값이 들어간다. 고쳐 쓴다.

`[build]`의 `auto-executables`와 `auto-tests`가 참이면 fpm이 `app/`과 `test/` 폴더에서 주 프로그램을 스스로 찾는다. `[fortran]`의 `implicit-typing = false`는 fpm이 `implicit none`을 모든 파일에 적용한다는 뜻이다. 다른 라이브러리를 쓸 때는 `[dependencies]` 표에 적는다. fpm 튜토리얼은 Fortran 표준 라이브러리 stdlib을 다음처럼 가져온다.

```text
[dependencies]
stdlib = "*"
```

### 빌드, 실행, 테스트

`fpm build`는 컴파일과 링크를 하고, `fpm run`은 필요하면 다시 빌드한 뒤 `app/`의 프로그램을 실행하고, `fpm test`는 `test/`의 프로그램을 실행한다.

```sh
fpm build
```

```text
 + mkdir -p build/dependencies
[  0%]                  area_calc.f90
[ 25%]                  area_calc.f90  done.
[ 25%]                       main.f90
[ 25%]                 libarea_calc.a
[ 50%]                 libarea_calc.a  done.
[ 75%]                       main.f90  done.
[ 75%]                      area_calc
[100%]                      area_calc  done.
[100%] Project compiled successfully.
```

```sh
fpm run
```

```text
Project is up to date
 Hello, area_calc!
```

```sh
fpm test
```

```text
[  0%]                      check.f90
[ 50%]                      check.f90  done.
[ 50%]                          check
[100%]                          check  done.
[100%] Project compiled successfully.
 Put some tests in here!
```

빌드 결과는 `build/` 폴더에 쌓인다. `.o`, `.mod`, 실행 파일이 모두 이 안에 들어가므로 소스 폴더가 어질러지지 않는다. `fpm build`는 `build/` 안에 `.gitignore`를 만들어 git이 이 폴더를 무시하게 한다.

테스트 프로그램은 확인에 실패하면 `error stop`으로 끝나게 쓴다. 0이 아닌 종료 상태로 끝나면 `fpm test`는 `<ERROR> Execution for object " check " returned exit code  1`이라고 알리고 실패로 끝난다. `error stop` 문은 프로그램을 오류 상태로 끝낸다.

fpm이 gfortran에 넘기는 옵션도 확인할 수 있다. `fpm build --verbose`로 컴파일 명령을 보면 기본(debug) 프로파일은 `-Wall -Wextra`와 `-g -fcheck=bounds` 같은 옵션을 주지만 `-std=f2018`은 주지 않는다. 이 가이드의 옵션을 쓰려면 `--flag`로 지정한다. 이때 기본 옵션은 빠지고 지정한 옵션이 쓰인다.

```sh
fpm build --flag "-std=f2018 -Wall -Wextra"
```

최적화를 켠 빌드는 `fpm build --profile release`로 만든다.

## 흔한 실수

- 실행 파일을 `./` 없이 부른다. 현재 폴더가 실행 파일을 찾는 경로에 없으면 `command not found`가 나온다.
- 파일을 나누어 컴파일할 때 모듈이 든 파일을 나중에 컴파일한다. `Cannot open module file` 오류가 나온다. fpm을 쓰면 이 순서를 직접 챙기지 않아도 된다.
- 모듈을 고친 뒤 그 모듈을 쓰는 파일을 다시 컴파일하지 않는다. 옛 `.o`를 그대로 링크하면 프로시저 인수가 바뀐 경우에도 링크가 성공하고, 실행하면 틀린 값이 나올 수 있다. 모듈을 고치면 그것을 쓰는 파일도 다시 컴파일한다.
- 컴파일 경고를 보고도 넘어간다. 경고는 대개 오타나 값이 달라지는 변환을 가리킨다.
- fpm 명령을 `fpm.toml`이 없는 폴더에서 실행한다. fpm은 `fpm.toml`을 찾지 못했다는 오류를 내고 멈춘다.

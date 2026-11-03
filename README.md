# E1-1 개발 워크스테이션 구축 — 내 컴퓨터에 '작업실' 꾸미기

> 코디세이 올인원 1기 · 저장소: Github과 Codyssey를 연동하기 위해 만들어진 Repository입니다.

## 1. 개요

"내 컴퓨터에서만 되는" 문제를 줄이려고, 누가 써도 같은 방식으로 실행되는 작업실을 직접 꾸몄다.

- **터미널**: 폴더·파일을 만들고 옮기고, 권한을 바꿨다.
- **Docker**: 컨테이너를 켜고 끄고, Dockerfile 로 내 웹 서버 이미지를 만들었다. 포트·바인드 마운트·볼륨도 확인했다.
- **Git/GitHub**: 내 이름표를 설정하고, 결과를 이 저장소에 올렸다.

**미션 요구사항과 내가 한 것이 맞는지 대조표 → [mission-check.md](e1-1-workstation/docs/mission-check.md)**

**이걸 왜 하나 — AI 와 무슨 관계인지 → [why-this-matters.md](e1-1-workstation/docs/why-this-matters.md)**

모든 단계는 명령과 출력으로 증명했다. 전체 로그는 [logs/terminal.md](e1-1-workstation/logs/terminal.md) 에 있다.

## 2. 실행 환경

| 항목 | 내용 |
|---|---|
| OS | Windows 11 Pro 26H2 (OS 빌드 26300.9711), 교육장 공용 PC — [winver 화면](e1-1-workstation/screenshots/winver.png) |
| 셸·터미널 | Git Bash (MINGW64 UCRT64), 명령 프롬프트(cmd) |
| Docker | `Docker version 29.9.2, build a82e528` · Docker Desktop 4.97.0 (WSL2 기반, `OSType: linux`, `x86_64`) |
| Git | git version 2.56.0.windows.4 |

## 3. 수행 항목 체크리스트

- [x] 터미널: `pwd`, `ls -la`, `cd`, `mkdir`, `touch`, `echo`, `cat`, `cp`, `mv`(이동·이름변경), `rm`
- [x] 권한: 파일 1개(644 → 600), 폴더 1개(755 → 700 → 755) 전/후 비교
- [x] Docker 점검: `docker --version`, `docker info`
- [x] Docker 운영: `pull`, `images`, `run`, `ps`, `ps -a`, `logs`, `stats`, `stop`, `rm`
- [x] `hello-world` 실행, `ubuntu` 컨테이너 안에서 명령 실행
- [x] `attach` 와 `exec` 차이 관찰
- [x] Dockerfile 로 커스텀 이미지 `my-web:1.0` 빌드
- [x] 포트 매핑 2개(8080, 8081) 접속 확인
- [x] 바인드 마운트: 호스트 파일 수정이 컨테이너에 바로 반영
- [x] 볼륨: 컨테이너를 지워도 데이터 유지
- [x] Git 설정(`user.name`, `user.email`, `init.defaultBranch main`)
- [x] VS Code GitHub 로그인 (`011cyon-dot (GitHub)`) — [사진](e1-1-workstation/screenshots/vscode-github.jpg)

## 4. 검증 방법과 결과

| 항목 | 확인한 명령 | 결과 | 증거 |
|---|---|---|---|
| 숨김 파일 | `ls` vs `ls -la` | `.secret` 은 `ls -la` 에서만 보임 | [로그 1](e1-1-workstation/logs/terminal.md#1-터미널-조작) |
| 파일 권한 | `chmod 600 memo.txt` 전후 `ls -l` | `-rw-r--r--` → `-rw-------` | [로그 2](e1-1-workstation/logs/terminal.md#2-권한) |
| 폴더 권한 | `chmod 700`, `chmod 755` 전후 `ls -ld` | `drwxr-xr-x` → `drwx------` → `drwxr-xr-x` | [로그 2](e1-1-workstation/logs/terminal.md#2-권한) |
| Docker 동작 | `docker run hello-world` | `Hello from Docker!` | [로그 3](e1-1-workstation/logs/terminal.md#3-docker-점검과-운영) |
| 컨테이너 상태 | `stop` 뒤 `ps` / `ps -a` | `ps` 에서 사라지고 `ps -a` 에 `Exited (0)` | [로그 3](e1-1-workstation/logs/terminal.md#3-docker-점검과-운영) |
| attach/exec | 각각 들어갔다 `exit` 뒤 `ps -a` | exec 뒤 `Up`, attach 뒤 `Exited (0)` | [로그 4](e1-1-workstation/logs/terminal.md#4-attach-와-exec) |
| 커스텀 이미지 | `docker build -t my-web:1.0 .` | `docker images` 에 `my-web:1.0` | [Dockerfile](e1-1-workstation/web/Dockerfile) |
| 포트 매핑 | `curl http://localhost:8080`, `:8081` | 둘 다 `<h1>Kim Jongjin workstation</h1>` | [로그 6](e1-1-workstation/logs/terminal.md#6-포트-매핑), [브라우저 사진](e1-1-workstation/screenshots/browser-8080-8081.png) |
| 바인드 마운트 | 파일 수정 전후 `curl :8082` | `before` → `after - changed on host` | [로그 7](e1-1-workstation/logs/terminal.md#7-바인드-마운트) |
| 볼륨 | 쓰기 → 컨테이너 삭제 → 새 컨테이너에서 읽기 | `saved-in-volume` 유지 | [로그 8](e1-1-workstation/logs/terminal.md#8-볼륨) |
| Git 설정 | `git config --list` | user.name, user.email, init.defaultbranch=main | [로그 9](e1-1-workstation/logs/terminal.md#9-git-설정) |

## 5. 커스텀 이미지 (Dockerfile)

- **베이스 이미지**: `nginx:alpine`. 가벼운 웹 서버라 정적 페이지 한 장을 띄우기에 알맞다.
- **커스텀 포인트**: nginx 기본 홈페이지를 내 페이지(`index.html`)로 바꿨다.

```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
```

```
$ cd e1-1-workstation/web
$ docker build -t my-web:1.0 .
$ docker run -d --name web1 -p 8080:80 my-web:1.0
$ curl http://localhost:8080
<h1>Kim Jongjin workstation</h1>
```

> `-p 8080:80` 은 이 PC의 모든 네트워크(`0.0.0.0`)에 문을 연다. 교육장처럼 같은 망을 쓰는 곳에서는 `-p 127.0.0.1:8080:80` 으로 내 PC에서만 열리게 하는 게 안전하다.

## 6. 내 말로 정리 (평가 질문)

화면에 나온 출력을 하나씩 읽는 법 → **[출력 읽는 법](e1-1-workstation/docs/reading-outputs.md)**

- **절대 경로 vs 상대 경로**
  - 절대 경로는 꼭대기부터 다 적는다. 예: `cd /c` 는 어디서 쳐도 C 드라이브로 간다.
  - 상대 경로는 지금 위치를 기준으로 한다. 예: `cd workstation` 은 지금 폴더 안의 workstation 으로 간다.
- **권한 755·644**
  - r=4, w=2, x=1 을 더해 나·그룹·나머지 순서로 적는다.
  - 644 = `rw-r--r--`: 나만 쓰고, 남은 읽기만 한다.
  - 755 = `rwxr-xr-x`: 나만 고치고, 남은 들어가기·실행만 한다.
- **포트 매핑이 필요한 이유**
  - 컨테이너는 격리돼 있어 바깥에서 바로 못 들어간다.
  - `-p 8080:80` 으로 내 컴퓨터 8080번과 컨테이너 80번을 이어 줘야 브라우저로 접속된다.
- **볼륨**
  - 컨테이너는 지우면 안의 파일도 사라진다.
  - 볼륨은 Docker 가 따로 보관하는 저장소라, 컨테이너를 지워도 데이터가 남는다.
  - 바인드 마운트는 내 폴더를 그대로 연결하는 것이다.
- **Git vs GitHub**
  - Git 은 내 컴퓨터에서 변경 기록을 남기는 도구다(commit).
  - GitHub 은 그 기록을 올려 두고 함께 쓰는 인터넷 저장소다(push/pull).

## 7. 트러블슈팅

### ① 리눅스 명령이 안 됨 (PowerShell)
- **문제**: `cd ~/coding/...` 를 치니 "경로가 존재하지 않습니다" 가 나왔다. `touch` 같은 명령도 없었다.
- **원인 가설**: PowerShell 은 리눅스 셸이 아니고, 그 주소는 다른 컴퓨터의 것이다.
- **확인**: 줄 앞이 `PS C:\...>` 였다.
- **해결**: `& "C:\Program Files\Git\bin\bash.exe"` 로 Git Bash 에 들어갔다. 줄 앞이 `$` 로 바뀌었다.

### ② 한글 입력 상태로 쳐서 명령이 깨짐
- **문제**: `cd\ 작업실` → `No such file or directory`, `pwd` → `command not found`
- **원인 가설**: 한글 입력기가 켜져 있어 보이지 않는 글자가 섞였다.
- **확인**: 오류 메시지에 `\354\236\221...`, `\343\205pwd` 처럼 깨진 바이트가 보였다.
- **해결**: 영어 입력으로 바꾸고, 폴더 이름도 영어(`workstation`)로 정했다.

### ③ 대소문자 실수
- **문제**: `mkdir -P me/docs` → `unknown option -- P`. 다음 `cd me` 도 실패했다.
- **원인 가설**: 리눅스 옵션은 대소문자를 구분한다.
- **해결**: `mkdir -p me/docs` 로 다시 쳤다. 바깥에 잘못 생긴 `memo.txt` 는 `mv memo.txt me/` 로 옮겼다.

### ④ Git Bash 에서 chmod 가 안 먹힘
- **문제**: `chmod 600`, `chmod 700` 을 해도 `ls -l` 결과가 그대로였다.
- **원인 가설**: 윈도우 파일 시스템(NTFS)은 리눅스 권한 방식을 쓰지 않는다.
- **확인**: 전후 `-rw-r--r--` 가 똑같았다.
- **해결**: `docker run -it --rm ubuntu bash` 로 진짜 리눅스 안에서 다시 했더니 바뀌었다.

### ⑤ 설치 직후 `docker: command not found`
- **문제**: Docker Desktop 을 깔고 엔진이 켜졌는데 터미널이 docker 를 못 찾았다.
- **원인 가설**: 터미널은 켜질 때 프로그램 위치(PATH)를 읽는데, 설치 전에 연 창이었다.
- **해결**: 터미널을 닫고 새로 여니 `docker info` 가 됐다.

### ⑥ 켜진 컨테이너는 못 지움
- **문제**: `docker rm web` → `cannot remove container "web": container is running`
- **해결**: `docker stop web` 으로 끈 뒤 `docker rm web` 했다.

### ⑦ 셸마다 경로 쓰는 법이 다름
- **문제**: cmd 에서 `cd /c/workstation` → "지정된 경로를 찾을 수 없습니다". Git Bash 에서 `"\c\Program Files\..."` → `No such file or directory`
- **원인**: cmd·PowerShell 은 `C:\workstation`, Git Bash 는 `/c/workstation` 처럼 `/` 를 쓴다.
- **해결**: 셸에 맞게 고쳐 썼다. Git Bash 에서 `docker run -v` 를 쓸 때는 `MSYS_NO_PATHCONV=1` 을 붙였다. Git Bash 가 `/usr/share/...` 를 윈도우 주소로 바꾸지 않게 하려는 것이다.

## 8. 보안

- 토큰·비밀번호·인증 코드는 이 문서에 넣지 않았다.
- 공용 PC라 실습 뒤 GitHub 로그아웃과 Windows 자격 증명 삭제를 한다.

## 9. 느낀점

처음엔 AI 과정에서 왜 터미널과 Docker 부터 하나 싶었다. 해 보니 AI 프로그램도 결국 어느 컴퓨터에서든 똑같이 돌아가야 쓸 수 있고, 그 바탕이 컨테이너·포트·볼륨·Git 이었다. 자세한 연결은 [why-this-matters.md](e1-1-workstation/docs/why-this-matters.md).

---

## (지난 실습) 출석부 attend.py — 11-02

날짜와 이름을 넣으면 출석이 쌓이고 목록을 볼 수 있는 프로그램. 파일 하나, 외부 라이브러리 없음.

```
python attend.py                      # 메뉴
python attend.py add 김종진            # 오늘 출석
python attend.py add 김종진 2026-11-02 # 날짜 지정
python attend.py list [2026-11-02]    # 목록 (날짜별)
python attend.py count                # 사람별 횟수
```
맥은 `python3`. 기록은 `attendance.csv`(엑셀로 열림) — 이름이 들어가서 git 에는 올리지 않는다.
school run ok 11-02
home run ok 11-02

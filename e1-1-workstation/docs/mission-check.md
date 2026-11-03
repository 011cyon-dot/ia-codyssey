# 미션 요구사항 ↔ 내가 한 것 대조

E1-1 미션 문서의 요구사항을 하나씩 놓고, 실제로 한 것과 증거가 맞는지 확인했다.

- ✅ 했고 증거도 있음
- 🔶 했지만 증거(사진·출력)가 부족함
- ⬜ 아직 안 함

## 수행 항목

| 미션 요구사항 | 내가 한 것 | 증거 | 상태 |
|---|---|---|---|
| 터미널: `pwd`, `ls -la`(숨김 포함), `cd`, `mkdir`, `cp`, `mv`(이동·이름변경), `rm`, `cat`, `touch` | 전부 실행. `.secret` 숨김 파일이 `ls -la` 에서만 보이는 것 확인 | [로그 1](../logs/terminal.md#1-터미널-조작) | ✅ |
| 권한: 파일 1개·폴더 1개 chmod 전/후 비교 (`ls -l`) | 파일 644→600, 폴더 755→700→755. Git Bash 에서는 안 바뀌어서 ubuntu 컨테이너 안에서 함 | [로그 2](../logs/terminal.md#2-권한) | ✅ |
| Docker 점검: `docker --version`, `docker info` | 둘 다 실행. `Docker version 29.9.2, build a82e528` | [로그 3](../logs/terminal.md#3-docker-점검과-운영) | ✅ |
| Docker 운영: `images`, `pull`, `run`, `stop`, `ps`, `ps -a`, `logs`, `stats` | 전부 실행, 끝에 `rm` 까지 | [로그 3](../logs/terminal.md#3-docker-점검과-운영) | ✅ |
| `hello-world` 실행 | `Hello from Docker!` | [로그 3](../logs/terminal.md#3-docker-점검과-운영) | ✅ |
| ubuntu 컨테이너에 들어가 `ls`·`echo` | 들어가서 `cd`, `echo`, `mkdir`, `chmod`, `ls -l` 실행 | [로그 2](../logs/terminal.md#2-권한) | ✅ |
| attach 와 exec 차이 관찰 | exec 뒤 `Up`, attach 뒤 `Exited (0)` | [로그 4](../logs/terminal.md#4-attach-와-exec) | ✅ |
| 커스텀 이미지: 베이스·커스텀 포인트·빌드/실행 로그 | (A)안: `nginx:alpine` + 내 `index.html` 로 교체 → `my-web:1.0` | [Dockerfile](../web/Dockerfile), [로그 5](../logs/terminal.md#5-커스텀-이미지-빌드) | ✅ |
| 포트 매핑 `-p 호스트:컨테이너`, 브라우저(주소창 포함) 또는 curl 증거 | 8080, 8081 두 개. curl 로 둘 다 확인 | [로그 6](../logs/terminal.md#6-포트-매핑), [브라우저 사진](../screenshots/browser-8080-8081.png) | ✅ |
| 바인드 마운트: 호스트 파일 수정 전/후 반영 | `before` → `after - changed on host` | [로그 7](../logs/terminal.md#7-바인드-마운트) | ✅ 다시 해서 `before` → `after` 둘 다 확인 |
| 볼륨: 생성→연결→쓰기→컨테이너 삭제→새 컨테이너에서 확인 | `saved-in-volume` 이 남아 있음 | [로그 8](../logs/terminal.md#8-볼륨) | ✅ |
| Git: `user.name`, `user.email`, `init.defaultBranch main` → `git config --list` | 셋 다 설정, `--list` 확인 | [로그 9](../logs/terminal.md#9-git-설정) | ✅ |
| VS Code GitHub 로그인·연동 스크린샷 | 왼쪽 아래 계정 메뉴에 `011cyon-dot (GitHub)` | [사진](../screenshots/vscode-github.jpg) | ✅ |

## 제출물(README)

| 미션 요구사항 | 상태 |
|---|---|
| 공개 저장소, 링크 하나로 전부 확인 | ✅ `011cyon-dot/ia-codyssey` (Public), 첫 화면에 미션 README |
| 프로젝트 개요 | ✅ README 1번 |
| 실행 환경 (OS·셸·Docker·Git 버전) | ✅ Windows 11 Pro 26H2, Git, Docker 버전 모두 있음 ([winver](../screenshots/winver.png)) |
| 수행 항목 체크리스트 | ✅ README 3번 |
| 검증 방법 + 결과 위치 링크 | ✅ README 4번 |
| 트러블슈팅(막혔던 일) 2건 이상 (문제→원인→확인→해결) | ✅ 7건 (README 7번 "막혔던 일과 푼 방법") |
| 터미널 명령과 출력 기록 | ✅ [logs/terminal.md](../logs/terminal.md) |
| 토큰·비밀번호·인증코드 마스킹 | ✅ 문서에 없음. 이메일도 가림 |

## 제약 조건

| 미션 제약 | 상태 |
|---|---|
| CLI 로만 | ✅ Docker Desktop 은 `winget` 으로 설치. 창은 엔진을 켜고 첫 화면을 넘기는 데만 씀 |
| Dockerfile 직접 작성 | ✅ `echo` 로 두 줄 직접 작성 |
| README 만 보고 재현 가능 | ✅ 명령을 순서대로 적음. 윈도우 경로는 다른 OS 쓰는 법도 적음 |
| 결과 예시를 그대로 내지 않기 | ✅ 오늘 내가 친 명령과 출력, 내 페이지 내용으로 작성 |

## 보너스 (선택)

| 항목 | 상태 |
|---|---|
| Docker Compose (단일·멀티 컨테이너, up/down/ps/logs) | ⬜ |
| 환경 변수로 포트 바꾸기 | ⬜ |
| GitHub SSH 키 | ⬜ |

## 남은 일
필수 항목은 모두 끝. 보너스(Compose·환경 변수 포트·SSH 키)는 선택.

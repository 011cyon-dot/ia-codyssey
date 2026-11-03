# 내 명령어 노트 + 💬 코멘트

실습하면서 Notepad++ 에 직접 정리한 노트(`change.log`)를 옮겨 적고, 줄마다 코멘트를 달았다.
**내 메모** = 내가 쓴 것(오타만 고침), **💬** = 더 알아 둘 것·헷갈리기 쉬운 것.

## 0. 터미널 준비

| 명령 | 내 메모 | 💬 |
|---|---|---|
| `& "C:\Program Files\Git\bin\bash.exe"` | PowerShell 안에서 Git Bash(리눅스식 터미널)를 켠다 | `&` 는 PowerShell 에서 "따옴표 안 프로그램을 실행해라"는 표시. 줄 앞이 `PS C:\>` → `$` 로 바뀌면 성공 |
| `"C:\Program Files\Git\bin\bash.exe"` | CMD(명령 프롬프트) 안에서 Git Bash 를 켠다. `&` 삭제 | cmd 는 `&` 가 필요 없다. 셸마다 문법이 다르다는 첫 예 |

## 1. 터미널 조작

| 명령 | 내 메모 | 💬 |
|---|---|---|
| `cd /c` | C 드라이브로 이동 (절대 경로) | Git Bash 는 `C:\` 를 `/c` 로 쓴다 |
| `mkdir -p workstation` | 폴더 만들기. 있어도 오류 없이 (`-p`) | `-P`(대문자)는 다른 뜻 → 오류. 리눅스는 대소문자를 가린다 |
| `cd workstation` | workstation 폴더로 이동 | `/` 로 시작하지 않으니 **상대 경로** |
| `pwd` | 지금 내가 있는 위치 출력 | 길을 잃으면 제일 먼저 칠 것 |
| `touch memo.txt` | 빈 파일 만들기 | 이미 있으면 내용은 그대로, 수정 시간만 바뀐다 |
| `echo "my first memo" > memo.txt` | 파일에 글 쓰기 (`>` 는 덮어쓰기) | `>>` 는 이어 붙이기. `>` 를 잘못 쓰면 원래 내용이 사라진다 |
| `cat memo.txt` | 파일 내용 보기 | |
| `mkdir -p me/docs` | me 와 그 안의 docs 를 한 번에 | 여기서 `-p` 는 "중간 폴더도 같이 만들기" |
| `mv memo.txt me/` | 파일을 me 폴더로 옮기기 | 끝의 `/` 는 "폴더 안으로"라는 뜻을 분명히 해 준다 |
| `cd me` | me 폴더로 들어가기 | |
| `cp memo.txt docs/copy.txt` | docs 안에 copy.txt 라는 이름으로 복사 | 복사하면서 이름도 바꿀 수 있다 |
| `mv docs/copy.txt docs/backup.txt` | 이름 바꾸기 (mv 로 함) | 리눅스엔 "이름 바꾸기" 명령이 따로 없다. 같은 폴더 안 이동 = 이름 바꾸기 |
| `touch .secret` | 점으로 시작하는 숨김 파일 만들기 | 설정 파일(`.gitignore`, `.env`)이 다 이 방식 |
| `ls` | 목록 보기 (숨김 파일은 안 보임) | |
| `ls -la` | 숨김 파일까지 자세히 (권한·크기·날짜) | `-l` 자세히 + `-a` 전부. 읽는 법은 [출력 읽는 법](reading-outputs.md) |
| `rm docs/backup.txt` | 파일 지우기 (휴지통 없이 바로) | **되돌릴 수 없다.** `rm -r` 은 폴더째라 더 조심 |
| `cd ..` | 한 칸 위 폴더로 | `..` = 위 폴더, `.` = 지금 폴더 |

## 2. 권한

| 명령 | 내 메모 | 💬 |
|---|---|---|
| `docker run -it --rm ubuntu bash` | 리눅스(ubuntu) 일회용 컨테이너에 들어가기, 나오면 자동 삭제(`--rm`) | Git Bash(윈도우 파일)에선 chmod 가 안 먹어서 진짜 리눅스로 들어간 것 |
| `touch memo.txt` / `mkdir docs` | 빈 파일 / 빈 폴더 만들기 | |
| `ls -l memo.txt` | 파일 권한 보기 | |
| `ls -ld docs` | 폴더 자체의 권한 보기 (`-d` 없으면 폴더 안을 보여 줌) | 잘 잡은 포인트 |
| `chmod 600 memo.txt` | 나만 읽기(4)+쓰기(2)=6, 남은 0,0 → `rw-------` | 비밀 키 파일은 이렇게 둔다 |
| `chmod 700 docs` | 나만 읽기+쓰기+들어가기=7 → `rwx------` | 폴더의 x 는 "실행"이 아니라 **들어가기** |
| `chmod 644 memo.txt` | 원래대로 (나 6, 남 4=읽기만) | 일반 파일의 기본값 |
| `chmod 755 docs` | 원래대로 (나 7, 남 5=보기+들어가기) | 일반 폴더의 기본값 |
| `exit` | 컨테이너에서 나오기 (자동 삭제) | `--rm` 이라 안에서 만든 파일도 같이 사라진다 |

## 3. Docker 설치·점검

| 명령 | 내 메모 | 💬 |
|---|---|---|
| `winget install -e --id Docker.DockerDesktop` | 윈도우 설치 도구로 Docker Desktop 설치 | `-e` = 이름이 정확히 같은 것만 |
| `"/c/Program Files/Docker/Docker/Docker Desktop.exe" &` | Docker 프로그램 켜기 (`&` 는 뒤에서 실행) | 여기 `&` 는 PowerShell 의 `&` 와 **다른 뜻**. bash 에선 줄 끝 `&` = 뒤에서 돌리기 |
| `docker --version` | Docker 버전 확인 | 29.9.2 |
| `docker info` | 엔진 상태 (리눅스 위에서 도는지, CPU·메모리 등) | `docker: command not found` 면 터미널을 새로 열기(PATH) |

## 4. Docker 운영

| 명령 | 내 메모 | 💬 |
|---|---|---|
| `docker run hello-world` | 시험용 이미지를 받아 실행. "Hello from Docker!" | 이미지가 없으면 알아서 pull 한다 |
| `docker pull nginx:alpine` | nginx 웹 서버 이미지(설계도) 받기 | `:alpine` = 태그. 가벼운 버전이라는 뜻 |
| `docker images` | 받아 둔 이미지 목록 | |
| `docker run -d --name web nginx:alpine` | 백그라운드(`-d`)로 켜고 이름은 web | 이름을 안 주면 `kind_sanderson` 처럼 아무 이름이 붙는다 |
| `docker ps` | 켜진(실행 중) 컨테이너 목록 | |
| `docker ps -a` | 꺼진 것까지 전부 | `Exited (0)` = 정상 종료 |
| `docker stats --no-stream web` | CPU·메모리 사용량 한 번만 | `--no-stream` 없으면 계속 갱신 → Ctrl+C 로 나옴 |
| `docker stop web` | 컨테이너 끄기 | |
| `docker rm web` | 지우기 (켜져 있으면 불가 → 먼저 stop) | `rm -f` 는 켜져 있어도 강제로 |

## 5. attach 와 exec

| 명령 | 내 메모 | 💬 |
|---|---|---|
| `docker run -dit --name box ubuntu bash` | ubuntu 를 뒤에서 켜 두기 (`-it` 로 bash 가 안 꺼지게) | `-dit` = `-d` + `-i` + `-t` 를 붙여 쓴 것 |
| `docker exec -it box bash` | 새 창을 열고 들어가기. 나와도 box 는 안 꺼짐 | 평소엔 exec 를 쓴다 |
| `docker attach box` | 주인 창에 붙기. `exit` 하면 box 가 꺼짐 | 꺼지지 않고 나오려면 Ctrl+P → Ctrl+Q |

## 6. 내 이미지 만들기

| 명령 | 내 메모 | 💬 |
|---|---|---|
| `echo "<h1>...</h1>" > index.html` | 내 홈페이지 한 장 만들기 | 이게 나중에 브라우저에 뜬다 |
| `echo "FROM nginx:alpine" > Dockerfile` | 설명서 첫 줄: nginx 를 바탕으로 | 첫 줄은 `>` (새로 쓰기) |
| `echo "COPY index.html ..." >> Dockerfile` | 둘째 줄: 내 페이지로 교체 (`>>` 는 이어 붙이기) | 여기서 `>` 를 쓰면 첫 줄이 지워진다 |
| `docker build -t my-web:1.0 .` | 설명서대로 이미지 만들기. `-t` 이름표, `.` 지금 폴더 | 끝의 `.` 을 빼먹기 쉽다 |
| `mv ~/Dockerfile ~/index.html /c/workstation/web/` | 엉뚱한 곳(홈)에 생긴 파일을 제자리로 | `~` = 내 홈 폴더. 만들기 전에 `pwd` 확인 습관 |

## 7. 포트 매핑

| 명령 | 내 메모 | 💬 |
|---|---|---|
| `docker run -d --name web1 -p 8080:80 my-web:1.0` | 내 PC 8080번 문 → 컨테이너 80번 문 | 순서는 **내 PC:컨테이너** |
| `docker run -d --name web2 -p 8081:80 my-web:1.0` | 같은 이미지를 8081 로 하나 더 | 같은 8080 을 두 번 쓰면 `port is already allocated` |
| `curl http://localhost:8080` | 터미널에서 내 웹 페이지 열어 보기 | 브라우저 대신 터미널로 보는 것 |

## 8. 바인드 마운트

| 명령 | 내 메모 | 💬 |
|---|---|---|
| `MSYS_NO_PATHCONV=1 docker run ... -v "C:/workstation/site:/usr/share/nginx/html" ...` | 내 폴더를 컨테이너 안에 그대로 연결. 앞 주문은 Git Bash 가 경로를 바꾸지 못하게 | 컨테이너 안에서 지워도 내 파일이 지워진다. 읽기만 시키려면 끝에 `:ro` |
| `echo "<h1>after...</h1>" > index.html` → `curl` | 내 파일만 고쳤는데 컨테이너 결과가 바로 바뀜 | 다시 build 할 필요가 없다 → 개발할 때 편함 |

## 9. 볼륨

| 명령 | 내 메모 | 💬 |
|---|---|---|
| `docker volume create mydata` | Docker 가 관리하는 저장소 만들기 | |
| `docker volume ls` | 볼륨 목록 | |
| `docker run -d --name vol1 -v mydata:/data ubuntu sleep infinity` | 볼륨을 연결해 켜 두기 | `sleep infinity` = 할 일 없이 계속 켜져 있기 |
| `docker exec vol1 sh -c "echo saved-in-volume > /data/note.txt"` | 볼륨에 글 쓰기 | `/data/ note.txt` 처럼 띄우면 다른 뜻이 된다 |
| `docker rm -f vol1` | 컨테이너 강제 삭제 (`-f` 는 켜져 있어도) | |
| `docker run --rm -v mydata:/data ubuntu cat /data/note.txt` | 새 컨테이너에서 읽기 → 글이 남아 있음 | 이게 볼륨의 핵심 증거 |

## 10. Git

| 명령 | 내 메모 | 💬 |
|---|---|---|
| `git config --global user.name "011cyon-dot"` | 커밋에 찍힐 내 이름 | `--global` = 이 PC 의 내 계정 전체에 적용 |
| `git config --global user.email "..."` | 커밋에 찍힐 내 이메일 | GitHub 가입 메일과 같게 |
| `git config --list` | 설정 전부 보기 | 같은 항목이 두 번 나오면 **아래쪽**이 이긴다 |
| `git config --global init.defaultBranch main` | 새 저장소 기본 가지 이름을 main 으로 | |
| `git clone https://github.com/011cyon-dot/ia-codyssey.git` | 원격 저장소를 통째로 복사 (하위 폴더 포함) | 처음 한 번만. 그다음부터는 `git pull` |
| `cp -r web site ia-codyssey/e1-1-workstation/` | web 과 site 를 둘 다 통째로 복사 (`-r` = 안쪽까지) | 맨 끝 하나가 목적지, 앞은 전부 복사할 것 |
| `git status` | 무엇이 바뀌었는지 보기 | 막히면 제일 먼저 칠 것 |
| `git add .` | 바뀐 파일을 이번 기록에 담기 | |
| `git commit -m "..."` | 내 컴퓨터에 기록 남기기 | 아직 GitHub 에는 없다 |
| `git push` | GitHub 에 올리기 | `rejected` 면 먼저 `git pull` |

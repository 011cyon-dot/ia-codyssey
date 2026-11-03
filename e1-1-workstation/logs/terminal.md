# 터미널 로그 (2026-11-03, 교육장 공용 PC)

실제로 친 명령과 출력. 사용자·컴퓨터 이름이 붙은 줄 앞부분은 `$`(Git Bash), `C:\>`(cmd), `#`(컨테이너 안) 로 줄였다. `ls -la` 의 사용자 이름은 `user` 로 가렸다. 긴 출력은 `...` 로 줄였다. 명령 끝의 메모는 실행되지 않는 주석이다: Git Bash·컨테이너 줄은 `# 뜻`, cmd(`C:\>`) 줄은 `& REM 뜻` (cmd 는 `#` 를 주석으로 모른다).

## 1. 터미널 조작
```
$ cd /c                                           # C 드라이브로 (절대 경로)
$ mkdir -p workstation                            # 폴더 만들기, 있어도 오류 없이
$ cd workstation                                  # 그 폴더로 (상대 경로)
$ pwd                                             # 지금 위치
/c/workstation
$ touch memo.txt                                  # 빈 파일
$ echo "my first memo" > memo.txt                 # 글 쓰기 (> 덮어쓰기)
$ cat memo.txt                                    # 내용 보기
my first memo
$ mkdir -p me/docs                                # me 와 그 안 docs 를 한 번에
$ mv memo.txt me/                                 # 파일을 me 로 옮기기
$ cd me                                           # me 로 들어가기
$ pwd                                             # 위치 확인
/c/workstation/me
$ ls                                              # 목록 (숨김 안 보임)
docs  memo.txt
$ cat memo.txt                                    # 옮긴 뒤에도 내용 그대로
my first memo
$ cp memo.txt copy.txt                            # 복사
$ mv copy.txt docs/                               # docs 로 옮기기
$ mv docs/copy.txt docs/backup.txt                # 이름 바꾸기
$ touch .secret                                   # 숨김 파일 (점으로 시작)
$ ls -la                                          # 숨김까지 자세히 → .secret 보임
total 1
drwxr-xr-x 1 user 1049089  0 Nov  3 15:47 .
drwxr-xr-x 1 user 1049089  0 Nov  3 15:45 ..
-rw-r--r-- 1 user 1049089  0 Nov  3 15:47 .secret
drwxr-xr-x 1 user 1049089  0 Nov  3 15:47 docs
-rw-r--r-- 1 user 1049089 14 Nov  3 15:45 memo.txt
$ rm docs/backup.txt                              # 지우기 (휴지통 없음)
$ ls -la docs                                     # docs 가 비었는지 확인
total 0
drwxr-xr-x 1 user 1049089 0 Nov  3 15:48 .
drwxr-xr-x 1 user 1049089 0 Nov  3 15:47 ..
$ cd ..                                           # 한 칸 위로
$ pwd                                             # 위치 확인
/c/workstation
```

## 2. 권한
Git Bash(윈도우 파일)에서는 chmod 를 해도 바뀌지 않았다(트러블슈팅 ④). 그래서 ubuntu 컨테이너 안에서 했다.
```
C:\> docker run -it --rm ubuntu bash            & REM 진짜 리눅스에 들어감, 나오면 자동 삭제
# cd /tmp                                         # 임시 폴더로
# echo "hello" > memo.txt                         # 파일 만들기
# ls -l memo.txt                                  # 전: rw-r--r-- (644)
-rw-r--r-- 1 root root 6 Nov  3 07:21 memo.txt
# chmod 600 memo.txt                              # 나만 읽기·쓰기
# ls -l memo.txt                                  # 후: rw------- (600)
-rw------- 1 root root 6 Nov  3 07:21 memo.txt
# exit                                            # 나오기 → 컨테이너 삭제
C:\> docker run -it --rm ubuntu bash            & REM 다시 들어감
# mkdir /tmp/docs                                 # 폴더 만들기
# ls -ld /tmp/docs                                # 전: rwxr-xr-x (755)
drwxr-xr-x 2 root root 4096 Nov  3 07:22 /tmp/docs
# chmod 700 /tmp/docs                             # 나만 전부
# ls -ld /tmp/docs                                # 후: rwx------ (700)
drwx------ 2 root root 4096 Nov  3 07:22 /tmp/docs
# chmod 755 /tmp/docs                             # 원래대로
# ls -ld /tmp/docs                                # 다시 755
drwxr-xr-x 2 root root 4096 Nov  3 07:22 /tmp/docs
# exit                                            # 나오기
```

## 3. Docker 점검과 운영
```
C:\> docker --version                           & REM Docker 버전
Docker version 29.9.2, build a82e528
C:\> docker info                                & REM 엔진 상태 (리눅스 위에서 도는지)
...
 Kernel Version: 6.18.54.1-microsoft-standard-WSL2
 Operating System: Docker Desktop
 OSType: linux
 Architecture: x86_64
 CPUs: 24
 Total Memory: 15.25GiB
 Docker Root Dir: /var/lib/docker
...
C:\> docker run hello-world                     & REM 시험용 이미지 받아 실행
Hello from Docker!
C:\> docker run -d --name web nginx:alpine      & REM 뒤에서 켜고 이름은 web
C:\> docker ps                                  & REM 켜진 것만
CONTAINER ID   IMAGE          ...   STATUS          PORTS     NAMES
af96bed46b14   nginx:alpine   ...   Up 24 seconds   80/tcp    web
C:\> docker logs web                            & REM web 이 남긴 기록
...
2026/11/03 07:25:21 [notice] 1#1: start worker process 53
C:\> docker stats --no-stream web               & REM CPU·메모리 한 번만
CONTAINER ID   NAME   CPU %   MEM USAGE / LIMIT     MEM %   NET I/O          BLOCK I/O     PIDS
af96bed46b14   web    0.00%   20.87MiB / 15.25GiB   0.13%   1.17kB / 126B    0B / 12.3kB   25
C:\> docker stop web                            & REM 끄기
web
C:\> docker ps                                  & REM 켜진 것 → 없음
CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS   NAMES
C:\> docker ps -a                               & REM 꺼진 것까지 → Exited (0)
CONTAINER ID   IMAGE          ...   STATUS                      NAMES
af96bed46b14   nginx:alpine   ...   Exited (0) 12 seconds ago   web
483722939fe3   hello-world    ...   Exited (0) 12 minutes ago   kind_sanderson
C:\> docker rm web                              & REM 지우기 (끈 뒤라 됨)
web
```

## 4. attach 와 exec
```
C:\> docker run -dit --name box ubuntu bash     & REM ubuntu 를 뒤에서 켜 두기
C:\> docker exec -it box bash                   & REM 새 창으로 들어가기
# exit                                            # 나와도 box 는 켜져 있음
C:\> docker ps                                  & REM Up → 그대로 켜짐
CONTAINER ID   IMAGE    COMMAND   CREATED         STATUS         NAMES
42405af8af70   ubuntu   "bash"    2 minutes ago   Up 2 minutes   box
C:\> docker attach box                          & REM 원래 창에 붙기
# echo "attach"                                   # 안에서 명령
attach
# exit                                            # 나오면 box 가 꺼짐
C:\> docker ps -a                               & REM Exited → 꺼짐 확인
42405af8af70   ubuntu   "bash"   2 minutes ago   Exited (0) 8 seconds ago   box
C:\> docker rm box                              & REM 정리
box
```

## 5. 커스텀 이미지 빌드
```
$ cat Dockerfile                                  # 설명서 두 줄 확인
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
$ docker build -t my-web:1.0 .                    # 설명서대로 이미지 만들기 (. = 지금 폴더)
...
 => [2/2] COPY index.html /usr/share/nginx/html/index.html
 => => naming to docker.io/library/my-web:1.0
$ docker images                                   # my-web:1.0 생김
IMAGE                ID             DISK USAGE   CONTENT SIZE
hello-world:latest   c567b231f656       25.9kB         9.49kB
my-web:1.0           6366b7724e9f       93.6MB         26.3MB
nginx:alpine         785835ea65db       94.5MB         27.2MB
ubuntu:latest        6a06111c3b0a        163MB         45.9MB
```

## 6. 포트 매핑
```
$ docker run -d --name web1 -p 8080:80 my-web:1.0  # 내 8080 → 컨테이너 80
$ docker run -d --name web2 -p 8081:80 my-web:1.0  # 같은 이미지로 하나 더, 8081
$ docker ps                                       # 둘 다 Up
d5d8a5dd27ab   my-web:1.0   ...   Up 6 seconds    0.0.0.0:8081->80/tcp   web2
5221f46682e4   my-web:1.0   ...   Up 40 seconds   0.0.0.0:8080->80/tcp   web1
$ curl http://localhost:8080                      # 터미널로 페이지 열기
<h1>Kim Jongjin workstation</h1>
$ curl http://localhost:8081                      # 8081 도 같은 페이지
<h1>Kim Jongjin workstation</h1>
```
브라우저 주소창으로도 확인: [browser-8080-8081.png](../screenshots/browser-8080-8081.png)

## 7. 바인드 마운트
```
$ cd /c/workstation/site                          # 연결할 내 폴더로
$ echo "<h1>before</h1>" > index.html             # 처음 내용
$ MSYS_NO_PATHCONV=1 docker run -d --name bind -p 8082:80 -v "C:/workstation/site:/usr/share/nginx/html" nginx:alpine  # 내 폴더를 컨테이너 안에 연결
$ curl http://localhost:8082                      # before 가 보임
<h1>before</h1>
$ echo "<h1>after - changed on host</h1>" > index.html  # 내 PC 파일만 고침
$ curl http://localhost:8082                      # 컨테이너도 바로 after
<h1>after - changed on host</h1>
```

## 8. 볼륨
```
$ docker volume create mydata                     # 보관함 만들기
mydata
$ docker volume ls                                # 목록
DRIVER    VOLUME NAME
local     mydata
$ MSYS_NO_PATHCONV=1 docker run -d --name vol1 -v mydata:/data ubuntu sleep infinity  # 보관함 연결해 켜 두기
$ MSYS_NO_PATHCONV=1 docker exec vol1 sh -c "echo saved-in-volume > /data/note.txt"  # 보관함에 글 쓰기
$ MSYS_NO_PATHCONV=1 docker exec vol1 cat /data/note.txt  # 써졌는지 확인
saved-in-volume
$ docker rm -f vol1                               # 컨테이너 강제 삭제
vol1
$ MSYS_NO_PATHCONV=1 docker run --rm -v mydata:/data ubuntu cat /data/note.txt  # 새 컨테이너에서 읽기 → 남아 있음
saved-in-volume
```

## 9. Git 설정
```
$ git --version                                   # Git 버전
git version 2.56.0.windows.4
$ git config --global user.name "011cyon-dot"     # 커밋에 찍힐 이름
$ git config --global user.email "0***@gmail.com"  # 커밋에 찍힐 이메일
$ git config --global init.defaultBranch main     # 새 저장소 기본 가지 = main
$ git config --list                               # 설정 전부 보기
...
init.defaultbranch=master      ← PC 전체(system) 설정
user.name=011cyon-dot
user.email=0***@gmail.com
init.defaultbranch=main        ← 내(global) 설정, 이쪽이 적용됨
```

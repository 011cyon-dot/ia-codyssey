# 터미널 로그 (2026-11-03, 교육장 공용 PC)

실제로 친 명령과 출력. 사용자·컴퓨터 이름이 붙은 줄 앞부분은 `$`(Git Bash), `C:\>`(cmd), `#`(컨테이너 안) 로 줄였다. `ls -la` 의 사용자 이름은 `user` 로 가렸다. 긴 출력은 `...` 로 줄였다.

## 1. 터미널 조작
```
$ cd /c
$ mkdir -p workstation
$ cd workstation
$ pwd
/c/workstation
$ touch memo.txt
$ echo "my first memo" > memo.txt
$ cat memo.txt
my first memo
$ mkdir -p me/docs
$ mv memo.txt me/
$ cd me
$ pwd
/c/workstation/me
$ ls
docs  memo.txt
$ cat memo.txt
my first memo
$ cp memo.txt copy.txt
$ mv copy.txt docs/
$ mv docs/copy.txt docs/backup.txt
$ touch .secret
$ ls -la
total 1
drwxr-xr-x 1 user 1049089  0 Nov  3 15:47 .
drwxr-xr-x 1 user 1049089  0 Nov  3 15:45 ..
-rw-r--r-- 1 user 1049089  0 Nov  3 15:47 .secret
drwxr-xr-x 1 user 1049089  0 Nov  3 15:47 docs
-rw-r--r-- 1 user 1049089 14 Nov  3 15:45 memo.txt
$ rm docs/backup.txt
$ ls -la docs
total 0
drwxr-xr-x 1 user 1049089 0 Nov  3 15:48 .
drwxr-xr-x 1 user 1049089 0 Nov  3 15:47 ..
$ cd ..
$ pwd
/c/workstation
```

## 2. 권한
Git Bash(윈도우 파일)에서는 chmod 를 해도 바뀌지 않았다(트러블슈팅 ④). 그래서 ubuntu 컨테이너 안에서 했다.
```
C:\> docker run -it --rm ubuntu bash
# cd /tmp
# echo "hello" > memo.txt
# ls -l memo.txt
-rw-r--r-- 1 root root 6 Nov  3 07:21 memo.txt
# chmod 600 memo.txt
# ls -l memo.txt
-rw------- 1 root root 6 Nov  3 07:21 memo.txt
# exit
C:\> docker run -it --rm ubuntu bash
# mkdir /tmp/docs
# ls -ld /tmp/docs
drwxr-xr-x 2 root root 4096 Nov  3 07:22 /tmp/docs
# chmod 700 /tmp/docs
# ls -ld /tmp/docs
drwx------ 2 root root 4096 Nov  3 07:22 /tmp/docs
# chmod 755 /tmp/docs
# ls -ld /tmp/docs
drwxr-xr-x 2 root root 4096 Nov  3 07:22 /tmp/docs
# exit
```

## 3. Docker 점검과 운영
```
C:\> docker --version
Docker version 29.9.2, build a82e528
C:\> docker info
...
 Kernel Version: 6.18.54.1-microsoft-standard-WSL2
 Operating System: Docker Desktop
 OSType: linux
 Architecture: x86_64
 CPUs: 24
 Total Memory: 15.25GiB
 Docker Root Dir: /var/lib/docker
...
C:\> docker run hello-world
Hello from Docker!
C:\> docker run -d --name web nginx:alpine
C:\> docker ps
CONTAINER ID   IMAGE          ...   STATUS          PORTS     NAMES
af96bed46b14   nginx:alpine   ...   Up 24 seconds   80/tcp    web
C:\> docker logs web
...
2026/11/03 07:25:21 [notice] 1#1: start worker process 53
C:\> docker stats --no-stream web
CONTAINER ID   NAME   CPU %   MEM USAGE / LIMIT     MEM %   NET I/O          BLOCK I/O     PIDS
af96bed46b14   web    0.00%   20.87MiB / 15.25GiB   0.13%   1.17kB / 126B    0B / 12.3kB   25
C:\> docker stop web
web
C:\> docker ps
CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS   NAMES
C:\> docker ps -a
CONTAINER ID   IMAGE          ...   STATUS                      NAMES
af96bed46b14   nginx:alpine   ...   Exited (0) 12 seconds ago   web
483722939fe3   hello-world    ...   Exited (0) 12 minutes ago   kind_sanderson
C:\> docker rm web
web
```

## 4. attach 와 exec
```
C:\> docker run -dit --name box ubuntu bash
C:\> docker exec -it box bash
# exit
C:\> docker ps
CONTAINER ID   IMAGE    COMMAND   CREATED         STATUS         NAMES
42405af8af70   ubuntu   "bash"    2 minutes ago   Up 2 minutes   box
C:\> docker attach box
# echo "attach"
attach
# exit
C:\> docker ps -a
42405af8af70   ubuntu   "bash"   2 minutes ago   Exited (0) 8 seconds ago   box
C:\> docker rm box
box
```

## 5. 커스텀 이미지 빌드
```
$ cat Dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
$ docker build -t my-web:1.0 .
...
 => [2/2] COPY index.html /usr/share/nginx/html/index.html
 => => naming to docker.io/library/my-web:1.0
$ docker images
IMAGE                ID             DISK USAGE   CONTENT SIZE
hello-world:latest   c567b231f656       25.9kB         9.49kB
my-web:1.0           6366b7724e9f       93.6MB         26.3MB
nginx:alpine         785835ea65db       94.5MB         27.2MB
ubuntu:latest        6a06111c3b0a        163MB         45.9MB
```

## 6. 포트 매핑
```
$ docker run -d --name web1 -p 8080:80 my-web:1.0
$ docker run -d --name web2 -p 8081:80 my-web:1.0
$ docker ps
d5d8a5dd27ab   my-web:1.0   ...   Up 6 seconds    0.0.0.0:8081->80/tcp   web2
5221f46682e4   my-web:1.0   ...   Up 40 seconds   0.0.0.0:8080->80/tcp   web1
$ curl http://localhost:8080
<h1>Kim Jongjin workstation</h1>
$ curl http://localhost:8081
<h1>Kim Jongjin workstation</h1>
```
브라우저 주소창으로도 확인: [browser-8080-8081.png](../screenshots/browser-8080-8081.png)

## 7. 바인드 마운트
```
$ cd /c/workstation/site
$ echo "<h1>before</h1>" > index.html
$ MSYS_NO_PATHCONV=1 docker run -d --name bind -p 8082:80 -v "C:/workstation/site:/usr/share/nginx/html" nginx:alpine
$ curl http://localhost:8082
<h1>before</h1>                      ✏️ 다시 찍은 출력으로 확인
$ echo "<h1>after - changed on host</h1>" > index.html
$ curl http://localhost:8082
<h1>after - changed on host</h1>
```

## 8. 볼륨
```
$ docker volume create mydata
mydata
$ docker volume ls
DRIVER    VOLUME NAME
local     mydata
$ MSYS_NO_PATHCONV=1 docker run -d --name vol1 -v mydata:/data ubuntu sleep infinity
$ MSYS_NO_PATHCONV=1 docker exec vol1 sh -c "echo saved-in-volume > /data/note.txt"
$ MSYS_NO_PATHCONV=1 docker exec vol1 cat /data/note.txt
saved-in-volume
$ docker rm -f vol1
vol1
$ MSYS_NO_PATHCONV=1 docker run --rm -v mydata:/data ubuntu cat /data/note.txt
saved-in-volume
```

## 9. Git 설정
```
$ git --version
git version 2.56.0.windows.4
$ git config --global user.name "011cyon-dot"
$ git config --global user.email "0***@gmail.com"
$ git config --global init.defaultBranch main
$ git config --list
...
init.defaultbranch=master      ← PC 전체(system) 설정
user.name=011cyon-dot
user.email=0***@gmail.com
init.defaultbranch=main        ← 내(global) 설정, 이쪽이 적용됨
```

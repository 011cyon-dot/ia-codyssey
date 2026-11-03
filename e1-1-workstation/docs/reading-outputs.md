# 출력 읽는 법 — 왜 이렇게 나오는가

오늘 실습에서 나온 화면을 하나씩 읽는 법. 명령을 친 것보다 **결과를 설명할 수 있는 것**이 목표다.

## 1. `ls -la`
```
-rw-r--r-- 1 user 1049089 14 Nov 3 15:45 memo.txt
```
- 맨 앞 `-` 는 파일, `d` 는 폴더다.
- `rw-r--r--` 는 권한이다(아래 2번).
- `14` 는 크기(바이트)다. `my first memo` 13글자에 줄바꿈 1을 더한 값이다.
- `.secret` 처럼 점(.)으로 시작하면 숨김 파일이다. `-a` 를 붙여야 보인다.
- `.` 은 지금 폴더, `..` 은 한 칸 위 폴더다. 그래서 `cd ..` 이 위로 간다.

## 2. 권한 숫자
```
rw-  r--  r--
 나  그룹  나머지
4+2   4    4    = 644
```
- r(읽기)=4, w(쓰기)=2, x(실행)=1 을 칸마다 더한다.
- 폴더의 x 는 "안으로 들어갈 수 있다"는 뜻이다.

| 숫자 | 글자 | 뜻 |
|---|---|---|
| 644 | `rw-r--r--` | 나만 고치고, 남은 읽기만 |
| 600 | `rw-------` | 나만 읽고 쓰기 |
| 755 | `rwxr-xr-x` | 나만 고치고, 남은 보기·들어가기 |
| 700 | `rwx------` | 나만 전부 |

## 3. `docker ps -a`
```
CONTAINER ID   IMAGE         STATUS                  PORTS                  NAMES
af96bed46b14   nginx:alpine  Up 24 seconds           0.0.0.0:8080->80/tcp   web
483722939fe3   hello-world   Exited (0) 12 min ago                          kind_sanderson
```
- `Up` 은 켜져 있다는 뜻이고, `Exited (0)` 은 정상으로 끝났다는 뜻이다. 괄호 안 0 은 오류가 없다는 뜻이다.
- `ps` 는 켜진 것만, `ps -a` 는 꺼진 것까지 전부 보여 준다.
- 이름을 안 주면 Docker 가 `kind_sanderson` 처럼 아무 이름이나 붙인다.
- 켜진 컨테이너는 바로 못 지운다. `stop` 한 다음 `rm` 해야 한다.

## 4. 이미지 vs 컨테이너
- **이미지는 설계도**(`docker images`), **컨테이너는 그 설계도로 찍어 낸 실물**(`docker ps`)이다.
- 설계도 하나로 실물을 여러 개 만들 수 있다. 그래서 `my-web:1.0` 하나로 web1, web2 를 동시에 띄웠다.
- 이미지가 없으면 `Unable to find image ... locally` → `Pulling` 이 나온다. Docker Hub 에서 자동으로 받아 오는 것이다.

## 5. 포트 `0.0.0.0:8080->80/tcp`
- 내 컴퓨터의 8080번 문으로 들어오면 컨테이너의 80번 문(nginx)으로 보낸다는 뜻이다.
- 컨테이너는 격리돼 있어서, 이걸 안 하면 브라우저로 들어갈 수 없다.
- 그래서 같은 이미지라도 8080, 8081 처럼 바깥 문만 다르게 해서 여러 개를 띄울 수 있다.
- 앞의 `0.0.0.0` 은 "이 컴퓨터의 모든 네트워크에 문을 연다"는 뜻이다. 방화벽이 막지 않으면 같은 교실의 다른 PC도 `내 IP:8080` 으로 들어올 수 있다. 내 컴퓨터에서만 보려면 `-p 127.0.0.1:8080:80` 처럼 쓴다.

## 6. exec vs attach
| | 들어가는 방식 | `exit` 한 뒤 |
|---|---|---|
| `docker exec -it box bash` | 컨테이너 안에 **새 창**을 열고 들어감 | 컨테이너는 계속 `Up` |
| `docker attach box` | 컨테이너의 **주인 창**(처음 켠 bash)에 붙음 | 컨테이너가 `Exited` |

## 7. Dockerfile 과 빌드
```
FROM nginx:alpine                                  ← 바탕이 되는 이미지
COPY index.html /usr/share/nginx/html/index.html   ← 기본 홈페이지를 내 페이지로 교체
```
- `docker build -t my-web:1.0 .`
  - `-t` 는 이름표(이름:버전)다.
  - 맨 끝 `.` 은 "지금 폴더의 Dockerfile 을 써라"는 뜻이다.
- 빌드 로그의 `[2/2] COPY ...` 는 Dockerfile 두 번째 줄이 실행됐다는 뜻이다.

## 8. 바인드 마운트 vs 볼륨
| | 바인드 마운트 `-v C:/workstation/site:/usr/share/nginx/html` | 볼륨 `-v mydata:/data` |
|---|---|---|
| 연결하는 것 | 내 폴더 | Docker 가 따로 관리하는 저장소 |
| 오늘 결과 | 파일만 고쳤는데 `before` → `after` 로 바로 바뀜 | 컨테이너를 지웠는데 `saved-in-volume` 이 남음 |
| 쓰임 | 개발 중 파일을 고쳐 바로 확인 | DB 처럼 오래 남겨야 하는 데이터 |

- `C:/workstation/site` 는 오늘 쓴 윈도우 경로다. 맥·리눅스에서는 `-v "$(pwd)/site:/usr/share/nginx/html"` 처럼 내 컴퓨터 경로로 바꿔 쓴다.
- 컨테이너는 지우면 안의 파일도 같이 사라진다. `--rm` 뒤 새 컨테이너에 `docs` 가 없던 이유다. 그래서 볼륨이 필요하다.

## 9. Git vs GitHub
- `git commit` 은 **내 컴퓨터**에 기록을 남기는 것이다.
- `git push` 는 그 기록을 **GitHub** 에 올리는 것이다.
- push 가 `rejected` 되면 GitHub 에 내 컴퓨터에 없는 기록이 있다는 뜻이다. `git pull` 로 먼저 받아 합친 뒤 다시 push 한다.
- `nothing to commit` 은 바뀐 게 없다는 뜻이다. 파일을 저장했는지, 맞는 폴더인지 확인한다.
- `git config --list` 에 `init.defaultbranch` 가 두 번 나오면 아래쪽(내 설정)이 적용된다.

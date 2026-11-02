# ia-codyssey
Github과 Codyssey를 연동하기 위해 만들어진 Repository입니다.

## 출석부 (attend.py) — 11-02 실습

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

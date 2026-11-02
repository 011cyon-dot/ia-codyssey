"""스터디 출석부 — 날짜와 이름을 넣으면 출석이 쌓이고, 목록을 볼 수 있다.

외부 라이브러리 없이 파이썬 기본 기능만 쓴다. 윈도우·맥 모두 된다.
출석 기록은 이 파일 옆의 attendance.csv 에 쌓인다(엑셀로도 열린다).

쓰는 법
  python attend.py                      메뉴로 쓰기
  python attend.py add 김종진            오늘 날짜로 출석
  python attend.py add 김종진 2026-11-02 날짜를 정해서 출석
  python attend.py list                 전체 목록
  python attend.py list 2026-11-02      그날 출석만
  python attend.py count                사람별 출석 횟수
(맥에서는 python 대신 python3)
"""
import csv
import datetime as dt
import os
import sys

FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'attendance.csv')
HEADER = ['날짜', '이름']


def load():
    """저장된 출석 기록을 [(날짜, 이름), ...] 로 읽는다. 파일이 없으면 빈 목록."""
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.reader(f))
    return [(r[0], r[1]) for r in rows[1:] if len(r) >= 2]


def save(records):
    with open(FILE, 'w', newline='', encoding='utf-8-sig') as f:   # utf-8-sig: 엑셀에서 한글이 안 깨지게
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerows(sorted(records))


def check_date(text):
    """'2026-11-02' 꼴인지 확인. 비어 있으면 오늘."""
    text = (text or '').strip()
    if not text:
        return dt.date.today().isoformat()
    try:
        return dt.date.fromisoformat(text).isoformat()
    except ValueError:
        raise ValueError(f"날짜는 2026-11-02 처럼 넣어 주세요: '{text}'")


def add(name, date=''):
    name = (name or '').strip()
    if not name:
        raise ValueError('이름을 넣어 주세요.')
    date = check_date(date)
    records = load()
    if (date, name) in records:
        return f'이미 출석했어요: {date} {name}'
    records.append((date, name))
    save(records)
    return f'출석했어요: {date} {name}'


def show(date=''):
    records = load()
    if date:
        date = check_date(date)
        records = [r for r in records if r[0] == date]
    if not records:
        return '출석 기록이 없어요.'
    lines = [f'{d}  {n}' for d, n in sorted(records)]
    return '\n'.join(lines) + f'\n— 모두 {len(records)}건'


def count():
    records = load()
    if not records:
        return '출석 기록이 없어요.'
    by = {}
    for _, n in records:
        by[n] = by.get(n, 0) + 1
    return '\n'.join(f'{n}  {k}회' for n, k in sorted(by.items(), key=lambda x: (-x[1], x[0])))


def menu():
    while True:
        print('\n[출석부] 1) 출석하기  2) 목록 보기  3) 날짜별 보기  4) 사람별 횟수  0) 끝내기')
        pick = input('번호: ').strip()
        try:
            if pick == '1':
                name = input('이름: ')
                date = input('날짜 (그냥 Enter = 오늘): ')
                print(add(name, date))
            elif pick == '2':
                print(show())
            elif pick == '3':
                print(show(input('날짜 (예 2026-11-02): ') or dt.date.today().isoformat()))
            elif pick == '4':
                print(count())
            elif pick == '0':
                print('끝!')
                return
            else:
                print('0~4 중에 골라 주세요.')
        except ValueError as e:
            print(e)


def main(argv):
    try:
        if not argv:
            menu()
        elif argv[0] == 'add' and len(argv) >= 2:
            print(add(argv[1], argv[2] if len(argv) > 2 else ''))
        elif argv[0] == 'list':
            print(show(argv[1] if len(argv) > 1 else ''))
        elif argv[0] == 'count':
            print(count())
        else:
            print(__doc__)
            return 1
    except ValueError as e:
        print(e)
        return 1
    except (KeyboardInterrupt, EOFError):
        print('\n끝!')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

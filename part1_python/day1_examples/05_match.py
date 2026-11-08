"""5. match-case: 값에 따라 갈라지기 (C언어의 switch-case와 비슷하다)
파이썬 3.10 이상에서만 동작한다. (python --version 으로 확인)
실행: python 05_match.py

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. command를 "defend", "run", "dance"로 바꾸면 각각 무엇이 나올까요?
  Q2. "heal"이면 "치료한다"를 출력하는 case를 추가해 보세요.
"""
command = "attack"

match command:
    case "attack":
        print("공격!")
    case "defend":
        print("방어!")
    case "run" | "escape":      # | 로 여러 값을 한 번에 묶을 수 있다
        print("도망친다")
    case _:                     # 나머지 전부 (C언어의 default)
        print("알 수 없는 명령")

# C언어와 다른 점: break가 필요 없다. 맞는 case 하나만 실행하고 끝난다.

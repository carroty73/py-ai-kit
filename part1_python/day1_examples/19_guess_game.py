"""19. 종합: 숫자 맞히기 게임 (변수, if, while, input을 모두 사용)
컴퓨터가 1~20 중 숫자 하나를 정한다. 5번 안에 맞혀 보자.
실행: python 19_guess_game.py

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. 숫자 범위를 1~50으로, 기회를 7번으로 바꿔 보세요. (안내 문구도 같이 고치세요.)
  Q2. 정답을 맞혔을 때 나오는 말을 바꿔 보세요.
"""
import random

answer = random.randint(1, 20)
tries = 5

print("1부터 20 사이의 숫자를 맞혀 보세요! 기회는 5번입니다.")

while tries > 0:
    guess = int(input("숫자 입력: "))
    tries = tries - 1

    if guess == answer:
        print("정답입니다! 축하해요!")
        break
    elif guess < answer:
        print("더 큰 수예요. 남은 기회:", tries)
    else:
        print("더 작은 수예요. 남은 기회:", tries)
else:
    print("아쉽네요. 정답은", answer, "였어요.")

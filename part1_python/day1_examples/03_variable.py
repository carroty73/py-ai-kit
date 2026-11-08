"""3. 변수: 값에 이름표를 붙여 두는 상자
실행: python 03_variable.py

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. attack의 숫자를 바꾸면 남은 체력이 어떻게 달라질까요?
  Q2. hp = hp - attack 줄을 두 번 쓰면 남은 체력은 얼마일까요?
  Q3. mp = 50 변수를 만들어 print로 출력해 보세요.
"""
name = "용사"
hp = 100
attack = 15

print(name)
print(hp)

# 변수는 값을 바꿀 수 있다.
hp = hp - attack
print("공격을 받았다! 남은 체력:", hp)

# 글자와 숫자를 한 줄에 섞어 쓰기
print(name, "의 체력은", hp, "입니다.")

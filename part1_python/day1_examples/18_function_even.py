"""18. 짝수 판별: True나 False를 돌려주는 함수
n % 2 는 n을 2로 나눈 나머지다. 나머지가 0이면 짝수다.
함수 없이 하면 얼마나 불편한지 먼저 보고, 함수로 바꿔 본다.
실행: python 18_function_even.py

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. print(7 % 2)와 print(10 % 2)는 각각 무엇이 나올까요?
  Q2. print(is_even(7))은 무엇이 나올까요?
  Q3. "짝수"를 "짝!"으로 바꾸려면 방법 1은 몇 줄을 고쳐야 할까요? 방법 2는요?
  Q4. 홀수이면 True를 돌려주는 is_odd 함수를 직접 만들어 보세요.
"""
# 방법 1: 함수 없이 무식하게
n = 7
if n % 2 == 0:
    print(n, "짝수")
else:
    print(n, "홀수")

n = 10
if n % 2 == 0:
    print(n, "짝수")
else:
    print(n, "홀수")

n = 3
if n % 2 == 0:
    print(n, "짝수")
else:
    print(n, "홀수")

print()


# 방법 2: 함수로 만든다. 결과는 똑같다.
def is_even(n):
    return n % 2 == 0


for n in [7, 10, 3]:
    if is_even(n):
        print(n, "짝수")
    else:
        print(n, "홀수")

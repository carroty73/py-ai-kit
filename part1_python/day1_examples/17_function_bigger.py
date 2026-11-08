"""17. 큰 수 고르기: if와 return을 함께 쓰는 함수
return을 만나면 함수는 거기서 바로 끝난다.
함수 없이 하면 얼마나 불편한지 먼저 보고, 함수로 바꿔 본다.
실행: python 17_function_bigger.py

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. bigger(5, 5)처럼 두 수가 같으면 무엇이 나올까요?
  Q2. "큰 수는"을 "더 큰 수는"으로 바꾸려면 방법 1은 몇 줄을 고쳐야 할까요? 방법 2는요?
  Q3. 작은 수를 돌려주는 smaller 함수를 직접 만들어 보세요.
  Q4. bigger(bigger(3, 9), 5)는 무엇이 나올까요? 예상한 뒤 확인해 보세요.
"""
# 방법 1: 함수 없이 무식하게 (같은 if를 매번 쓴다)
a, b = 3, 7
if a > b:
    print("큰 수는", a)
else:
    print("큰 수는", b)

a, b = 10, 2
if a > b:
    print("큰 수는", a)
else:
    print("큰 수는", b)

a, b = 8, 9
if a > b:
    print("큰 수는", a)
else:
    print("큰 수는", b)

print()


# 방법 2: 함수로 만든다. 결과는 똑같다.
def bigger(a, b):
    if a > b:
        return a
    return b


print("큰 수는", bigger(3, 7))
print("큰 수는", bigger(10, 2))
print("큰 수는", bigger(8, 9))

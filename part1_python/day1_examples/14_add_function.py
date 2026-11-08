"""14. 두 수를 더하는 함수: 값을 받아서 결과를 돌려준다
함수 없이 하면 얼마나 불편한지 먼저 보고, 함수로 바꿔 본다.
add(a, b)는 두 수를 받아 더한 값을 return으로 돌려준다.
실행: python 14_add_function.py

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. 방법 1에서 "더한 뒤 결과에 10을 더하는" 규칙으로 바꾸려면 몇 줄을 고쳐야 할까요? 방법 2는요?
  Q2. add(3, 4)를 add(10, 20)으로 바꾸면 무엇이 나올까요?
  Q3. return a + b를 return a * b로 바꾸면 add(3, 4)는 무엇이 나올까요?
  Q4. return a + b를 print(a + b)로 바꾸면 result에는 무엇이 들어갈까요? print(result)로 확인해 보세요.
  Q5. 두 수를 빼는 sub 함수를 직접 만들어 보세요.
"""
# 방법 1: 함수 없이 무식하게 (같은 계산을 매번 직접 쓴다)
print(3 + 4)
print(10 + 5)
print(20 + 30)
print(100 + 200)
print(7 + 8)

print()

# 방법 2: 함수로 만들어 두고 이름만 부른다. 결과는 똑같다.
def add(a, b):
    return a + b


print(add(3, 4))
print(add(10, 5))
print(add(20, 30))
print(add(100, 200))
print(add(7, 8))

print()

# 함수의 결과를 변수에 담을 수도 있다.
result = add(3, 4)
print(result)

# 함수의 결과를 다른 함수의 입력으로 쓸 수도 있다.
print(add(add(1, 2), add(3, 4)))

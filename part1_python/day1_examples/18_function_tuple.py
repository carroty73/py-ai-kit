"""18. 값을 둘 돌려주는 함수와 튜플: 바꿀 수 없는 묶음
튜플은 ( ) 로 묶은 값이다. 리스트와 비슷하지만 만든 뒤에는 바꿀 수 없다.
함수가 return 뒤에 값을 둘 쓰면 튜플 하나로 묶어서 돌려준다.
실행: python 18_function_tuple.py

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. point[0]과 point[1]은 각각 무엇이 나올까요?
  Q2. point[0] = 99를 쓰면 어떻게 될까요? 리스트였다면요? 예상한 뒤 확인해 보세요.
  Q3. min_max([5, 2, 8])을 부르면 lo와 hi는 각각 얼마일까요?
  Q4. result = min_max([5, 2, 8])로 받고 print(result)를 하면 무엇이 나올까요?
  Q5. 큰 수와 작은 수의 차이를 돌려주는 gap 함수를 직접 만들어 보세요.
"""
point = (3, 5)                     # 튜플: 가로 3, 세로 5
print(point)
print(point[0], point[1])
# point[0] = 99                    # 주석을 지우고 실행해 보자: 튜플은 바꿀 수 없다.


def min_max(nums):
    return min(nums), max(nums)    # 튜플 하나로 묶어서 돌려준다


lo, hi = min_max([3, 9, 1])        # 두 변수에 나눠 담기
print("가장 작은 수:", lo)
print("가장 큰 수:", hi)

result = min_max([3, 9, 1])        # 나누지 않고 그대로 받으면 튜플이다.
print(result)

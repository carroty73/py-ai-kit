"""13. 리스트: 여러 값을 한 줄로 묶어 두기
실행: python 13_list.py

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. 좋아하는 아이템을 하나 더 append해 보세요.
  Q2. print(items[0])을 print(items[2])로 바꾸면 무엇이 나올까요?
  Q3. print(items[10])을 쓰면 어떻게 될까요? 예상한 뒤 확인해 보세요.
"""
items = ["칼", "방패", "물약"]

print(items)
print(items[0])        # 번호는 0부터 센다. 첫 번째 아이템
print(len(items))      # 개수

items.append("지도")   # 끝에 추가
print(items)

# 리스트와 for를 같이 쓰면 하나씩 꺼내 볼 수 있다.
for item in items:
    print("가방 안에 있는 것:", item)

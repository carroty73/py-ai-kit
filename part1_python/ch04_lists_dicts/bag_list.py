"""리스트: 가방에 물건 넣고 꺼내 보기.
실행: python bag_list.py
"""
items = ["칼", "방패", "물약"]
print(items[0])
items.append("지도")
for item in items:
    print("가방 안에 있는 것:", item)

"""13. 딕셔너리: 이름표를 붙여 두는 서랍장 (리스트는 번호로, 딕셔너리는 이름으로 찾는다)
실행: python 13_dict.py

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. hero["attack"]을 20으로 바꾸면 공격을 받은 뒤 남은 체력은 얼마일까요?
  Q2. print(hero["gold"])를 쓰면 어떻게 될까요? 예상한 뒤 확인해 보세요.
  Q3. print(hero.get("gold", 0))은 무엇이 나올까요? Q2와 무엇이 다를까요?
  Q4. 리스트 ["용사", 100, 15]에서 100이 체력인지 공격력인지 알 수 있을까요? 딕셔너리는요?
  Q5. hero에 "level": 1 항목을 추가해 출력해 보세요.
"""
hero = {"name": "용사", "hp": 100, "attack": 15}

print(hero)
print(hero["hp"])                  # 이름표(키)로 값을 찾는다

hero["hp"] = hero["hp"] - hero["attack"]    # 값 바꾸기
print("공격을 받았다! 남은 체력:", hero["hp"])

hero["mp"] = 50                    # 새 항목 추가
print(hero)

print(hero.get("gold", 0))         # 없는 키는 get으로 물으면 기본값(0)을 돌려준다

# 딕셔너리와 for를 같이 쓰면 이름표를 하나씩 꺼내 볼 수 있다.
for key in hero:
    print(key, ":", hero[key])

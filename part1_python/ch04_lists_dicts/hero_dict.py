"""딕셔너리: 용사의 상태를 이름표(key)로 다루기.
실행: python hero_dict.py
"""
hero = {"name": "용사", "hp": 100, "attack": 15}
hero["hp"] = hero["hp"] - hero["attack"]
hero["mp"] = 50
print(hero.get("gold", 0))   # 없는 key는 기본값 0
print(hero)

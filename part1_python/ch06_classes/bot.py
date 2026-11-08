"""클래스: Bot 두 개는 서로 다른 값을 가진다.
실행: python bot.py
"""
class Bot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.steps = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.steps += 1

a = Bot(0, 0)
b = Bot(5, 5)
a.move(1, 1)
print(a.x, b.x)   # 1 5

"""클래스: 슈팅 게임의 Player (3부 3장에서 이어 쓴다).
실행: python player.py
"""
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lives = 3
        self.score = 0

    def move(self, dx):
        self.x += dx

    def hit(self):
        self.lives -= 1

p = Player(240, 560)
p.move(10)
p.hit()
print("위치", p.x, "목숨", p.lives)   # 위치 250 목숨 2

"""클래스: 치즈를 찾아 한 칸씩 걸어가는 CheeseBot (3부 2장에서 이어 쓴다).
실행: python cheese_bot.py
"""
class CheeseBot:
    def __init__(self, pos, cheese):
        self.pos = pos
        self.cheese = cheese

    def step(self):
        self.pos += 1 if self.cheese > self.pos else -1

    def found(self):
        return self.pos == self.cheese

bot = CheeseBot(2, 7)
while not bot.found():
    bot.step()
    print("현재 위치", bot.pos)
print("치즈를 찾았다!")

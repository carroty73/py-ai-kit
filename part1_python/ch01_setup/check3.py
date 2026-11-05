"""사탕을 먹어서 레이저를 강하게 만든다. (창을 닫으면 끝난다.)
방향키: 이동, 스페이스바(누르고 있기): 레이저
사탕은 위에서 랜덤하게 내려온다. 먹을 때마다 해당 능력이 한 단계 오른다(최대 단계와 값은 check3.json).
  F(노랑): 레이저를 더 자주 쏜다
  R(보라): 레이저가 더 멀리 날아간다
실행: python check3.py
"""
import json
import math
import os
import random
import pygame

# 설정 (check3.json): 최대 단계, 능력별 시작값(base)과 단계마다 변하는 값(step)
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "check3.json"), encoding="utf-8") as f:
    config = json.load(f)
MAX_LEVEL = config["max_level"]
abilities = config["abilities"]
BACKGROUND = tuple(config["background_color"])
SHIP_WIDTH = config["ship"]["outline_width"]
SHIP_COLOR = tuple(config["ship"]["outline_color"])

pygame.init()
screen = pygame.display.set_mode((480, 640))
pygame.display.set_caption("Candy laser")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

CANDY_SIZE = config["candy"]["size"]
CANDY_COLORS = {kind: tuple(c["body"]) for kind, c in config["candy"]["colors"].items()}
STRIPE_COLORS = {kind: tuple(c["stripe"]) for kind, c in config["candy"]["colors"].items()}
CANDY_TILT = math.radians(config["candy"]["tilt_degrees"])
STRIPE_WIDTH = config["candy"]["stripe_width"]


def draw_candy(cx, top, kind):
    """포장 사탕: 가운데 동그라미 + 양옆 삼각형 포장지. (cx: 가운데 가로, top: 맨 위 세로)"""
    color = CANDY_COLORS[kind]
    s = CANDY_SIZE
    cy = top + s // 2
    r = int(s * 0.28)                      # 동그라미 반지름
    h = int(s * 0.24)                      # 포장지 높이의 절반
    cos_t, sin_t = math.cos(CANDY_TILT), math.sin(CANDY_TILT)

    def tilt(dx, dy):
        """사탕 가운데 기준으로 (dx, dy) 점을 기울인 화면 좌표"""
        return (cx + dx * cos_t - dy * sin_t, cy + dx * sin_t + dy * cos_t)

    left = [tilt(-s // 2, -h), tilt(-s // 2, h), tilt(-r, 0)]
    right = [tilt(s // 2, -h), tilt(s // 2, h), tilt(r, 0)]
    pygame.draw.polygon(screen, color, left)
    pygame.draw.polygon(screen, color, right)
    pygame.draw.circle(screen, color, (cx, cy), r)
    # 줄무늬: 포장지와 수직인 줄 하나 (양 끝이 동그라미 밖으로 나가지 않게 r - 1)
    pygame.draw.line(screen, STRIPE_COLORS[kind],tilt(0, -(r - 1)), tilt(0, r - 1), STRIPE_WIDTH)

x = 240            # 우주선 가운데 가로 위치
y = 560            # 우주선 맨 위 세로 위치
lasers = []        # 날아가는 레이저 [가로, 세로, 출발한 세로]
candies = []       # 내려오는 사탕 [가로, 세로, 종류]
level = {"F": 0, "R": 0}    # 먹은 사탕 단계
wait = 0           # 다음 레이저까지 남은 프레임
spawn = 0          # 다음 사탕까지 센 프레임

def value(kind):
    """능력 kind의 현재 단계에 맞는 값 = base + step * 단계 (max가 있으면 상한)"""
    a = abilities[kind]
    v = a["base"] + a["step"] * level[kind]
    if "max" in a:                         # max가 있으면 그 값을 넘지 않는다
        v = min(v, a["max"])
    return v


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 방향키로 움직이기
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= 4
    if keys[pygame.K_RIGHT]:
        x += 4
    if keys[pygame.K_UP]:
        y -= 4
    if keys[pygame.K_DOWN]:
        y += 4
    x = max(24, min(456, x))
    y = max(0, min(597, y))

    # 사탕 단계에 따라 레이저 값이 달라진다
    gap = 60 / value("F")                  # 초당 발사 수 -> 발사 간격(프레임, 60프레임 = 1초)
    speed = 6                              # 레이저 속도(고정)
    reach = value("R")                     # 사정거리

    # 레이저 쏘기 (스페이스바를 누르고 있으면 간격마다 한 발)
    if wait > 0:
        wait -= 1
    if keys[pygame.K_SPACE] and wait <= 0:
        lasers.append([x, y, y])
        wait = gap

    # 레이저 움직이기: 사정거리를 넘으면 사라진다
    for laser in lasers:
        laser[1] -= speed
    lasers = [laser for laser in lasers if laser[2] - laser[1] < reach]

    # 사탕: 90프레임마다 랜덤한 자리에서 랜덤한 종류가 내려온다
    spawn += 1
    if spawn >= 90:
        spawn = 0
        candies.append([random.randint(20, 460), -CANDY_SIZE, random.choice("FR")])

    ship = pygame.Rect(x - 22, y, 44, 43)
    remaining = []
    for candy in candies:
        candy[1] += 2
        box = pygame.Rect(candy[0] - CANDY_SIZE // 2, candy[1], CANDY_SIZE, CANDY_SIZE)
        if ship.colliderect(box):
            level[candy[2]] = min(MAX_LEVEL, level[candy[2]] + 1)     # 먹었다
        elif candy[1] < 640:
            remaining.append(candy)
    candies = remaining

    # 그리기
    screen.fill(BACKGROUND)
    body = [(x, y), (x + 22, y + 43), (x + 6, y + 43), (x, y + 31), (x - 6, y + 43), (x - 22, y + 43)]
    pygame.draw.polygon(screen, BACKGROUND, body)                 # 안쪽: 배경색으로 채움
    pygame.draw.polygon(screen, SHIP_COLOR, body, SHIP_WIDTH)     # 테두리
    for laser in lasers:
        pygame.draw.line(screen, (255, 255, 80), (laser[0], laser[1]), (laser[0], laser[1] + 10), 3)
    for candy in candies:
        draw_candy(candy[0], candy[1], candy[2])
    text = font.render("F " + str(level["F"]) + "   R " + str(level["R"]), True, (255, 255, 255))
    screen.blit(text, (10, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

"""사탕을 먹어서 레이저를 강하게 만든다. (창을 닫으면 끝난다.)
방향키: 이동, 스페이스바(누르고 있기): 레이저
사탕은 위에서 랜덤하게 내려온다. 먹을 때마다 해당 능력이 한 단계 오른다(최대 3단계).
  F(노랑): 레이저를 더 자주 쏜다
  S(파랑): 레이저가 더 빨리 날아간다
  R(보라): 레이저가 더 멀리 날아간다
실행: python check3.py
"""
import os
import random
import pygame

pygame.init()
screen = pygame.display.set_mode((480, 640))
pygame.display.set_caption("Candy laser")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

# 사탕 그림 (images 폴더)
folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
images = {
    "F": pygame.image.load(os.path.join(folder, "candy_yellow.png")).convert_alpha(),
    "S": pygame.image.load(os.path.join(folder, "candy_blue.png")).convert_alpha(),
    "R": pygame.image.load(os.path.join(folder, "candy_purple.png")).convert_alpha(),
}

x = 240            # 우주선 가운데 가로 위치
y = 560            # 우주선 맨 위 세로 위치
lasers = []        # 날아가는 레이저 [가로, 세로, 출발한 세로]
candies = []       # 내려오는 사탕 [가로, 세로, 종류]
level = {"F": 0, "S": 0, "R": 0}    # 먹은 사탕 단계
wait = 0           # 다음 레이저까지 남은 프레임
spawn = 0          # 다음 사탕까지 센 프레임

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
    gap = 24 - 6 * level["F"]              # 발사 간격(프레임): 24 -> 6
    speed = 6 + 3 * level["S"]             # 레이저 속도: 6 -> 15
    reach = 150 + 100 * level["R"]         # 사정거리: 150 -> 450

    # 레이저 쏘기 (스페이스바를 누르고 있으면 간격마다 한 발)
    if wait > 0:
        wait -= 1
    if keys[pygame.K_SPACE] and wait == 0:
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
        candies.append([random.randint(20, 460), -36, random.choice("FSR")])

    ship = pygame.Rect(x - 22, y, 44, 43)
    remaining = []
    for candy in candies:
        candy[1] += 2
        box = pygame.Rect(candy[0] - 18, candy[1], 36, 36)
        if ship.colliderect(box):
            level[candy[2]] = min(3, level[candy[2]] + 1)     # 먹었다
        elif candy[1] < 640:
            remaining.append(candy)
    candies = remaining

    # 그리기
    screen.fill((10, 10, 28))
    body = [(x, y), (x + 22, y + 43), (x + 6, y + 43), (x, y + 31), (x - 6, y + 43), (x - 22, y + 43)]
    pygame.draw.polygon(screen, (255, 255, 255), body)
    for laser in lasers:
        pygame.draw.line(screen, (255, 255, 80), (laser[0], laser[1]), (laser[0], laser[1] + 10), 3)
    for candy in candies:
        screen.blit(images[candy[2]], (candy[0] - 18, candy[1]))
    text = font.render("F " + str(level["F"]) + "   S " + str(level["S"]) + "   R " + str(level["R"]), True, (255, 255, 255))
    screen.blit(text, (10, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

"""방향키로 우주선을 움직이고, 스페이스바로 레이저를 쏜다. (창을 닫으면 끝난다.)
레이저는 짧고 천천히 나간다.
실행: python check2.py
"""
import pygame

pygame.init()
screen = pygame.display.set_mode((480, 640))
pygame.display.set_caption("Laser")
clock = pygame.time.Clock()

x = 240            # 우주선 가운데 가로 위치
y = 560            # 우주선 맨 위 세로 위치
lasers = []        # 날아가는 레이저 목록 [가로, 세로]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            lasers.append([x, y])             # 우주선 맨 위에서 출발

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
    x = max(24, min(456, x))                  # 화면 밖으로 못 나가게
    y = max(0, min(597, y))

    # 레이저: 위로 6칸씩, 화면 밖은 지운다
    for laser in lasers:
        laser[1] -= 6
    lasers = [laser for laser in lasers if laser[1] > -20]

    screen.fill((10, 10, 28))
    body = [(x, y), (x + 22, y + 43), (x + 6, y + 43), (x, y + 31), (x - 6, y + 43), (x - 22, y + 43)]
    pygame.draw.polygon(screen, (255, 255, 255), body)
    for laser in lasers:
        pygame.draw.line(screen, (255, 255, 80), (laser[0], laser[1]), (laser[0], laser[1] + 10), 3)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

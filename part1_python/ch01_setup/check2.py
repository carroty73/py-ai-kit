"""환경 확인용: 설치가 잘 됐는지 보는 아주 간단한 데모.

우주선이 좌우로 저절로 움직이면 파이썬, pygame 설치가 성공한 것이다.
스페이스바를 누르면 레이저가 나간다.
코드는 지금 몰라도 된다. 실행만 해 보자. (창을 닫으면 끝난다.)
실행: python check2.py
"""
import pygame

pygame.init()
screen = pygame.display.set_mode((480, 640))
pygame.display.set_caption("Install check")
clock = pygame.time.Clock()

x = 240
direction = 3
top = 540          # 우주선 맨 위의 세로 위치
lasers = []        # 날아가는 레이저 목록 [가로, 세로]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            lasers.append([x, top])   # 우주선 맨 위에서 출발

    x += direction
    if x < 24 or x > 456:
        direction = -direction

    for laser in lasers:
        laser[1] -= 12            # 위로 12칸씩
    lasers = [laser for laser in lasers if laser[1] > -20]   # 화면 밖은 지운다

    screen.fill((10, 10, 28))
    # 우주선: 48 x 48 칸 안에 들어오는 좌우 대칭 모양 (x가 가운데)
    body = [(x, top), (x + 22, top + 43), (x + 6, top + 43),
            (x, top + 31), (x - 6, top + 43), (x - 22, top + 43)]
    pygame.draw.polygon(screen, (10, 40, 55), body)
    pygame.draw.polygon(screen, (40, 220, 235), body, 2)
    for laser in lasers:
        pygame.draw.line(screen, (255, 255, 80), (laser[0], laser[1]), (laser[0], laser[1] + 18), 3)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

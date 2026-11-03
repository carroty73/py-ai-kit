"""환경 확인용: 설치가 잘 됐는지 보는 아주 간단한 데모.

우주선이 좌우로 저절로 움직이면 파이썬, pygame 설치가 성공한 것이다.
코드는 지금 몰라도 된다. 실행만 해 보자. (창을 닫으면 끝난다.)
실행: python check1.py
"""
import pygame

pygame.init()
screen = pygame.display.set_mode((480, 640))
pygame.display.set_caption("Install check")
clock = pygame.time.Clock()

x = 240
direction = 3

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    x += direction
    if x < 24 or x > 456:
        direction = -direction

    screen.fill((10, 10, 28))
    # 우주선: 48 x 48 칸 안에 들어오는 좌우 대칭 모양 (x가 가운데)
    top = 540
    body = [(x, top), (x + 22, top + 43), (x + 6, top + 43),
            (x, top + 31), (x - 6, top + 43), (x - 22, top + 43)]
    pygame.draw.polygon(screen, (10, 40, 55), body)
    pygame.draw.polygon(screen, (40, 220, 235), body, 2)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

"""데모용: 우주선이 좌우로 왔다갔다만 한다. (창을 닫으면 끝난다.)
실행: python check1.py
"""
import pygame

pygame.init()
screen = pygame.display.set_mode((480, 640))
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
    body = [(x, 540), (x + 22, 583), (x + 6, 583), (x, 571), (x - 6, 583), (x - 22, 583)]
    pygame.draw.polygon(screen, (255, 255, 255), body)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

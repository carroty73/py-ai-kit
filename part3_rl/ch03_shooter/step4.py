"""step4. 도형 그리기: 동그라미, 세모, 네모
창 안에 도형을 그려 본다. 도형은 "어디에, 무슨 색으로, 얼마나 크게"를 정해서 그린다.
도형의 색과 위치와 크기는 모두 숫자이고, 아래 "여기만 바꿔 보세요" 구역에 모아 두었다.
실행: python step4.py

결과: 연두색 창에 빨간 동그라미, 보라색 세모, 파란 네모가 가로로 나란히 나온다.

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. circle_color (255, 100, 100)을 바꿔 보세요. 노란색은 어떻게 만들까요?
  Q2. circle_pos (90, 320)의 숫자를 바꾸면 어디로 갈까요? 두 숫자가 각각 무엇인지 맞혀 보세요.
  Q3. circle_radius 60을 바꾸면 어떻게 될까요?
  Q4. circle_line을 0에서 5로 바꾸면 어떻게 될까요? 20으로 바꾸면요?
  Q5. triangle_points의 점 3개 중 하나의 숫자를 바꾸면 어떻게 될까요? 점을 하나 더 넣으면요?
  Q6. rect (330, 270, 120, 100)의 네 숫자는 각각 무엇일까요? 하나씩 바꿔서 알아내 보세요.
  Q7. 동그라미를 하나 더 그려 보세요. 눈사람을 만들 수 있을까요?
  Q8. screen.fill(bg_color) 줄을 도형을 그리는 줄들 아래로 옮기면 어떻게 될까요? 왜 그럴까요?
"""
import pygame

# ---------- 여기만 바꿔 보세요 ----------
width = 480                  # 창 가로 길이
height = 640                 # 창 세로 길이
bg_color = (150, 230, 80)    # 배경색 (빨강, 초록, 파랑). 각각 0~255. 연두색이다

circle_color = (255, 100, 100)    # 동그라미 색 (빨강)
circle_pos = (90, 320)            # 동그라미 중심 위치 (가로, 세로)
circle_radius = 60                # 동그라미 반지름
circle_line = 0                   # 동그라미 테두리 두께 (0이면 안을 가득 채운다)

triangle_color = (160, 90, 210)                       # 세모 색 (보라)
triangle_points = [(240, 270), (180, 370), (300, 370)]    # 세모 꼭짓점 3개의 위치 (가로, 세로)

rect_color = (100, 100, 255)      # 네모 색 (파랑)
rect = (330, 270, 120, 100)       # 네모 (왼쪽 위 가로, 왼쪽 위 세로, 너비, 높이)

# ---------- 아래는 지금은 몰라도 됩니다 ----------
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shapes")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # X 버튼을 눌렀다
            running = False

    screen.fill(bg_color)                # 먼저 배경을 칠하고, 그 위에 도형을 그린다

    # 동그라미: (화면, 색, 중심 위치(가로, 세로), 반지름, 테두리 두께)
    pygame.draw.circle(screen, circle_color, circle_pos, circle_radius, circle_line)

    # 세모: (화면, 색, 꼭짓점 3개의 위치)
    pygame.draw.polygon(screen, triangle_color, triangle_points)

    # 네모: (화면, 색, (왼쪽 위 가로, 왼쪽 위 세로, 너비, 높이))
    pygame.draw.rect(screen, rect_color, rect)

    pygame.display.flip()                # 그린 것을 화면에 보여 주기
    clock.tick(60)                       # 1초에 60번만 돈다

pygame.quit()

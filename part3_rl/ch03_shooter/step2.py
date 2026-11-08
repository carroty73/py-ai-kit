"""step2. 반복 확인: 창이 닫힐 때까지 계속 돈다
step1의 빈 창 한가운데에 흐른 시간을 123.45 sec처럼 보여 준다.
시간이 계속 올라가는 것은 컴퓨터가 같은 일을 계속 반복하고 있다는 뜻이다. 그 반복이 게임 루프다.
실행: python step2.py

결과: 까만 창 한가운데에 흰 글자로 0.01 sec, 0.02 sec ... 123.45 sec 처럼 시간이 계속 올라간다.
      실행한 창(터미널)에도 같은 글자가 계속 나온다. 창을 닫으면 끝난다.

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. (480, 640)의 숫자를 바꾸면 창 모양이 어떻게 달라질까요? 글자는 여전히 가운데에 있을까요?
  Q2. while running: 을 while False: 로 바꾸면 어떻게 될까요?
  Q3. running = False를 지우면(주석 처리하면) X 버튼을 눌러도 닫히지 않습니다. 왜 그럴까요?
  Q4. 한 바퀴가 10ms(0.01초)이면 1초에 몇 번 돌까요? 소수점 둘째 자리가 계속 바뀌는 이유는 무엇일까요?
  Q5. clock.tick(100)의 100을 2로 바꾸면 시간이 어떻게 올라갈까요? 60으로 바꾸면요?
      (60이면 한 바퀴가 약 16ms다. 게임은 1초에 60번 돈다.)
  Q6. {seconds:.2f}의 2를 1로 바꾸면 소수점이 몇 자리까지 나올까요?
  Q7. 글자 크기 90과 글자 색 (255, 255, 255)를 바꿔 보세요.
"""
import pygame

pygame.init()
screen = pygame.display.set_mode((480, 640))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 90)        # 글꼴 (기본 글꼴, 크기 90). 기본 글꼴은 영어와 숫자만 나온다

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # X 버튼을 눌렀다
            running = False

    seconds = pygame.time.get_ticks() / 1000    # 프로그램을 켠 뒤 흐른 시간(초). 1000으로 나누면 초가 된다
    message = f"{seconds:.2f} sec"       # 123.45 sec 처럼 소수점 둘째 자리까지 글자로 만든다
    print(message)                       # 터미널에도 보여 준다

    screen.fill((0, 0, 0))               # 창을 까맣게 지우고
    text = font.render(message, True, (255, 255, 255))      # 글자를 그림처럼 만든다
    screen.blit(text, text.get_rect(center=(240, 320)))     # 창의 한가운데(가로 240, 세로 320)에 붙인다
    pygame.display.flip()                # 그린 것을 화면에 보여 준다

    clock.tick(100)                      # 1초에 100번만 돈다 (한 바퀴가 10ms)

pygame.quit()

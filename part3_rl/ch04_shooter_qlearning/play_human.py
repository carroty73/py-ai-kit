"""1. 사람이 하는 갤러그. 오른쪽에 숫자판(dx, dy, px, action)이 나오고, 플레이 기록을 파일로 저장한다.
조작: 좌우 방향키(또는 A, D), 스페이스바 발사, 게임 오버 후 R로 재시작, ESC로 종료.
저장: 이 폴더의 my_results.csv, my_actions.csv, highscore.txt
실행: python play_human.py
"""
import galaga

galaga.RECORD = True
galaga.main(show_panel=True)

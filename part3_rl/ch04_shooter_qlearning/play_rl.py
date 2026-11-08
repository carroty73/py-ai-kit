"""3. 강화학습 봇이 하는 갤러그. 스스로 시행착오를 거쳐 배운 Q-러닝 봇이 대신 움직인다.
Q-표: rl_runs/run50k/q_best.npy  (인자로 다른 파일을 줄 수 있다)
기록은 저장하지 않는다. 게임 오버가 되면 창이 닫힌다. ESC로도 끝낼 수 있다.
실행: python play_rl.py [Q-표 파일]
필요: pip install pygame numpy
"""
import inspect
import os
import sys

import numpy as np

import galaga

HERE = os.path.dirname(os.path.abspath(__file__))
from rl_env import GalagaEnv

q_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "rl_runs", "run50k", "q_best.npy")
q_table = np.load(q_file)
helper = GalagaEnv()
memory = {"action": 2}


def decide(dx, dy, px):
    """게임 루프의 지금 상황을 읽어 학습할 때처럼 3프레임마다 한 번 결정하고, 그 사이에는 같은 행동을 유지한다."""
    loc = inspect.currentframe().f_back.f_locals
    if loc["frame"] % 3 == 0:
        helper.px = loc["px"]
        helper.enemies = [[e["x"], e["y"], e["hp"], e["speed"], e["kind"]] for e in loc["enemies"]]
        helper.bullets = [list(b) for b in loc["bullets"]]
        row = q_table[helper.state()]
        memory["action"] = int(np.flatnonzero(row == row.max())[0])
    a = memory["action"]
    # 행동 번호: 이동 = a % 3 (0 왼쪽, 1 오른쪽, 2 가만히), 발사 = a // 3
    return a % 3 == 0, a % 3 == 1, a // 3 == 1


galaga.RECORD = False
galaga.main(bot=decide, show_panel=True)

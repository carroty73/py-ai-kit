"""2. 모방학습 봇이 하는 갤러그. 사람의 플레이 기록으로 배운 AI(결정 트리)가 대신 움직인다.
모델: my_imitation.joblib (train_imitation.py가 내 기록으로 만든다). 없으면 ../day3/teacher_model.joblib을 쓴다.
기록은 저장하지 않는다. 게임 오버가 되면 창이 닫힌다. ESC로도 끝낼 수 있다.
실행: python play_imitation.py
필요: pip install pygame scikit-learn joblib
"""
import os

import joblib

import galaga

HERE = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(HERE, "my_imitation.joblib")
shoot_range = 20     # 적과 가로로 이만큼 이내면 쏜다

if os.path.exists(my_file):
    saved = joblib.load(my_file)
    model, cfg = saved["model"], saved["cfg"]
    print("내 모델을 씁니다:", cfg)
else:
    model = joblib.load(os.path.join(HERE, "..", "day3", "teacher_model.joblib"))
    cfg = dict(use_px=True, stay="drop", dead=15, hold=1)
    print("my_imitation.joblib이 없어서 강사 모델을 씁니다.")

mem = {"n": 0, "move": "stay"}


def decide(dx, dy, px):
    shoot = abs(dx) < shoot_range
    if mem["n"] % cfg["hold"] == 0:      # hold 번에 한 번만 새로 고르고, 나머지는 같은 행동을 유지한다
        if cfg["stay"] == "drop" and abs(dx) <= cfg["dead"]:
            mem["move"] = "stay"         # 적 바로 밑이면 선다 (규칙)
        else:
            mem["move"] = model.predict([[dx, dy, px] if cfg["use_px"] else [dx, dy]])[0]
    mem["n"] += 1
    return mem["move"] == "left", mem["move"] == "right", shoot


galaga.RECORD = False
galaga.main(bot=decide, show_panel=True)

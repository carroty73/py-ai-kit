"""step10. 모델 만들기 3: 내 AI를 질문 나무 그림으로 보고, 파일로 저장한다 (5단계)
기록 전체로 AI(결정 트리)를 학습시킨다. 학습이 끝난 AI는 "질문 나무"다.
  "dx가 -41보다 작은가? -> 예 -> dy가 ...보다 큰가? -> ..." 식으로 질문을 따라 내려가 left 또는 right를 답한다.
그 질문 나무를 그림으로 보여 주고, 내 AI를 my_model.joblib 파일 하나로 저장한다. 이 파일이 "내 AI 모델"이다.
파일만 있으면 학습을 다시 하지 않아도 언제든 같은 AI를 쓸 수 있다. 다음 단계에서 이 파일로 내 봇을 만든다.
기록이 없으면 sample_actions.csv(강사가 준 연습 기록)를 쓴다.
(필요한 도구: pip install pandas scikit-learn matplotlib joblib)
실행: python step10_save.py

결과: 질문 나무 그림 창이 뜨고, 터미널에 저장 완료와 파일 크기가 나온다. 폴더에 my_model.joblib과 my_tree.png가 생긴다.

퀴즈: 먼저 결과를 예상한 뒤, 코드를 바꿔 실행해서 확인해 보세요.
  Q1. 질문 나무의 맨 위 질문은 무엇인가요? 가장 중요한 질문이라고 생각하나요?
  Q2. 나무 끝(잎)의 색은 무엇을 뜻할까요? 색이 진할수록 어떤 뜻일까요?
  Q3. max_depth를 2로 바꾸면 나무가 어떻게 달라질까요? 파일 크기는요?
  Q4. 이 파일을 친구에게 보내면 친구 컴퓨터에서도 똑같이 동작할까요?
"""
import os

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree

# ---------- 여기만 바꿔 보세요 ----------
data_file = "my_actions.csv"         # 내 기록. 없으면 sample_actions.csv를 쓴다
max_depth = 4                        # step9에서 가장 좋았던 깊이로 바꿔 보자
# ---------- 아래는 지금은 몰라도 됩니다 ----------

folder = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(folder, data_file)
if not os.path.exists(path):
    path = os.path.join(folder, "sample_actions.csv")
    print("내 기록이 없어서 sample_actions.csv를 씁니다.")

df = pd.read_csv(path, dtype={"id": str}, on_bad_lines="skip")
moves = df[df["action"] != "stay"]
X = moves[["dx", "dy", "px"]].values
y = moves["action"].values

model = DecisionTreeClassifier(max_depth=max_depth, random_state=0)
model.fit(X, y)

model_path = os.path.join(folder, "my_model.joblib")
joblib.dump(model, model_path)                       # 저장: 이 파일이 "내 AI 모델"이다
print("저장 완료: my_model.joblib")
print("파일 크기:", os.path.getsize(model_path), "바이트")

fig, chart = plt.subplots(figsize=(14, 6))
plot_tree(model, feature_names=["dx", "dy", "px"], class_names=list(model.classes_),
          filled=True, rounded=True, fontsize=7, ax=chart)
chart.set_title("My AI = a tree of questions (orange: left, blue: right)")
fig.tight_layout()
fig.savefig(os.path.join(folder, "my_tree.png"))
plt.show()

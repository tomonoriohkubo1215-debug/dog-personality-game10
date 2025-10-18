# dog_game_streamlit_tuned.py
import streamlit as st
import random

st.set_page_config(page_title="犬の価値観ゲーム", layout="centered")
st.title("🐶 犬の価値観ゲーム")
st.write("質問に答えて、あなたの犬タイプを見つけましょう！")

dogs = ["シベリアンハスキー", "ラブラドールレトリバー", "ジャーマンシェパード",
        "ボーダーコリー", "ゴールデンレトリバー", "柴犬",
        "ジャックラッセルテリア", "キャバリアキングチャールズスパニエル",
        "スタンダードプードル", "ビーグル"]

questions = [
    {"text":"1. 新しいことに挑戦するのは好き？",
     "〇":["ジャックラッセルテリア","シベリアンハスキー","ボーダーコリー"],
     "△":["ゴールデンレトリバー","ジャーマンシェパード", "ビーグル"],
     "×":["ラブラドールレトリバー","柴犬","スタンダードプードル","キャバリアキングチャールズスパニエル",]},
    {"text":"2. 友達と遊ぶのは好き？",
     "〇":["ゴールデンレトリバー","ラブラドールレトリバー","シベリアンハスキー","ビーグル" ],
     "△":["ジャックラッセルテリア","ボーダーコリー","キャバリアキングチャールズスパニエル"],
     "×":["柴犬","スタンダードプードル","ジャーマンシェパード"]},
    {"text":"3. なんでも計画してから行動する？",
     "〇":["ジャーマンシェパード","スタンダードプードル","シベリアンハスキー","柴犬"],
     "△":[ "ボーダーコリー","ゴールデンレトリバー", ],
     "×":["ジャックラッセルテリア","ラブラドールレトリバー", "キャバリアキングチャールズスパニエル","ビーグル"]},
    {"text":"4. 困った友達を助けたい？",
     "〇":["ゴールデンレトリバー","ラブラドールレトリバー","キャバリアキングチャールズスパニエル"],
     "△":["ボーダーコリー","スタンダードプードル", "ビーグル"],
     "×":["ジャックラッセルテリア","柴犬","シベリアンハスキー","ジャーマンシェパード"]},
    {"text":"5. じっくり考えてから答えを出す？",
     "〇":["ジャーマンシェパード","柴犬","スタンダードプードル"],
     "△":["キャバリアキングチャールズスパニエル","ラブラドールレトリバー","ジャックラッセルテリア"],
     "×":["シベリアンハスキー","ボーダーコリー","ゴールデンレトリバー","ビーグル"]}
]

# 〇/△/× の基本点（差をはっきりつける）
base_points = {"〇": 4, "△": 2, "×": 1}

# 質問ごとの「補正点」マップ（その質問で特に優先したい犬に加点）
# 例: Q1ではシベリアンハスキーを強めにしたい → +3
question_bonus = {
    0: { "ジャックラッセルテリア": 3, "ボーダーコリー": 2,"シベリアンハスキー":1},
    1: {"ゴールデンレトリバー": 1.5, "ラブラドールレトリバー": 1, "ビーグル":2},
    2: {"ジャーマンシェパード": 1.5, "スタンダードプードル": 2},
    3: {"ラブラドールレトリバー": 1.5, "キャバリアキングチャールズスパニエル":2.5},
    4: {"柴犬": 2, "ジャーマンシェパード":0.5, "ビーグル":0.5, }
}

# 同点時の優先順位リスト（左が高優先）
tiebreak_priority = ["シベリアンハスキー","ラブラドールレトリバー","ジャーマンシェパード",
                     "ゴールデンレトリバー","ボーダーコリー","柴犬","ジャックラッセルテリア",
                     "キャバリアキングチャールズスパニエル","スタンダードプードル","ビーグル"]

# session_stateで回答管理
if "answers" not in st.session_state:
    st.session_state.answers = ["〇"]*len(questions)  # デフォルトを〇にしておく

for i, q in enumerate(questions):
    st.session_state.answers[i] = st.radio(q["text"], ("〇", "△", "×"), key=f"q{i}")

if st.button("犬タイプを判定する"):
    scores = {dog:0 for dog in dogs}
    # 各質問に対する基本点+補正点を加算
    for i, (q, ans) in enumerate(zip(questions, st.session_state.answers)):
        for dog in q[ans]:
            scores[dog] += base_points[ans]
        # 補正点を加える（その質問に関して特に出してあげたい犬）
        bonus_map = question_bonus.get(i, {})
        for dog, b in bonus_map.items():
            scores[dog] += b

    # スコア結果を表示（確認用）
    st.write("=== スコア一覧（内部確認用） ===")
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for d, s in sorted_scores:
        st.write(f"{d}: {s}")

    # 判定（同点は優先リストで決定）
    max_score = sorted_scores[0][1]
    top_dogs = [d for d, s in sorted_scores if s == max_score]
    if len(top_dogs) > 1:
        # 優先リスト順で最初に出現する犬を選ぶ（決定的にする）
        for p in tiebreak_priority:
            if p in top_dogs:
                result = p
                break
    else:
        result = top_dogs[0]

    st.success(f"🎉 判定された犬タイプ: {result}")

# 注意書きセット
st.markdown("---")  # 区切り線

st.warning("⚠️ 注意: このアプリはサンプル用です。結果は参考程度にご利用ください。")

# クレジット
st.markdown(
    "<p style='font-size:12px;color:gray;text-align:right'>produced by 学生団体Yippee</p>",
    unsafe_allow_html=True
)

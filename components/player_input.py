# components/player_input.py
import streamlit as st

TURN_KEY = "input_turn"   # 何ターン目の入力かを覚えておくカウンタ


class PlayerInput:
    """ユーザーの入力欄 + 送信ボタンを担当"""

    def __init__(self, base_key: str = "user_input") -> None:
        self.base_key = base_key  # 実際のキーは base_key + "_0", "_1"... みたいになる

    def render(self) -> str:
        """入力欄を表示して、送信されたテキストを返す（なければ空文字）"""

        # ターン番号の初期化
        if TURN_KEY not in st.session_state:
            st.session_state[TURN_KEY] = 0

        turn = st.session_state[TURN_KEY]

        # このターン専用のキーを作る
        text_key = f"{self.base_key}_{turn}"
        button_key = f"send_button_{turn}"

        # 入力欄
        user_input = st.text_area(
            "あなたの発言を入力:",
            key=text_key,
            height=160,
        )

        # 送信ボタン
        send_clicked = st.button("送信", key=button_key)

        if send_clicked:
            text = user_input.strip()
            if text:
                # 次のターン用にカウンタを進める
                st.session_state[TURN_KEY] = turn + 1
                return text

        # 送信されていない / 空文字のとき
        return ""

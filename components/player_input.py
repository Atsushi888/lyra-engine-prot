# components/player_input.py
import streamlit as st


class PlayerInput:
    """ユーザーの入力欄＋送信処理を担当"""

    def __init__(self, key_input: str = "user_input_box", key_button: str = "send_btn"):
        self.key_input = key_input
        self.key_button = key_button

    def render(self) -> str:
        """入力欄を描画して、送信ボタンが押されたときだけ文字列を返す"""

        user_input = st.text_area(
            "あなたの発言を入力:",
            value="",
            height=160,          # お好みで高さ調整
            key=self.key_input,
        )
        send_clicked = st.button("送信", key=self.key_button)

        if send_clicked:
            text = user_input.strip()
            if text:
                # ★ ここでは session_state をいじらない
                return text

        return ""

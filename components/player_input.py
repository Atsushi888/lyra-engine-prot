# components/player_input.py
import streamlit as st

class PlayerInput:
    """ユーザーの入力欄＋送信処理を担当"""

    def __init__(self, key_input="user_input_box", key_button="send_btn"):
        self.key_input = key_input
        self.key_button = key_button

    def render(self) -> str:
        """入力欄を描画して、送信時に文字列を返す"""
        user_input = st.text_input("あなたの発言を入力:", "", key=self.key_input)
        send_clicked = st.button("送信", key=self.key_button)

        if send_clicked and user_input.strip():
            content = user_input.strip()
            # 入力欄クリア
            st.session_state[self.key_input] = ""
            return content
        return ""

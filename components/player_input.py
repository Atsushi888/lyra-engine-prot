# components/player_input.py

from typing import Optional
import streamlit as st


class PlayerInput:
    # 入力欄用のセッションキー
    KEY = "player_input_text"

    def __init__(self) -> None:
        pass

    def render(self) -> str:
        """
        入力欄と「送信」ボタンを描画し、
        送信されたときだけテキストを返す。
        送信されていなければ "" を返す。
        """
        user_text: str = st.text_area(
            "あなたの発言を入力：",   # ← ここにラベルを書いてしまう
            key=self.KEY,
            height=160,
        )

        send = st.button("送信", type="primary")

        if send:
            text_to_send = (user_text or "").strip()
            if not text_to_send:
                return ""
            return text_to_send

        return ""

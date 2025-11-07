# components/player_input.py

from typing import Optional
import streamlit as st


class PlayerInput:
    # テキストエリアに使うキー名
    TEXT_KEY = "player_input_text"

    def __init__(self) -> None:
        # ここでは TEXT_KEY をいじらない。
        # （Streamlit が自分で初期化するので任せておく）
        pass

    def render(self) -> str:
        """
        入力欄と「送信」ボタンを描画し、
        送信されたときだけそのテキストを返す。
        送信されていなければ "" を返す。
        """

        st.write("あなたの発言を入力:")

        # テキストエリア本体（state 管理は Streamlit に任せる）
        user_text: str = st.text_area(
            label="",
            key=self.TEXT_KEY,
            height=160,
        )

        # 送信ボタン
        send = st.button("送信", type="primary")

        if send:
            text_to_send = (user_text or "").strip()
            if not text_to_send:
                # 空なら何もしない
                return ""

            # ★ ここでは TEXT_KEY を触らない ★
            #   （触るとまた同じエラーになるため）
            #   入力欄クリアは、あとで安全なやり方に差し替える。

            return text_to_send

        # 送信されていないとき
        return ""

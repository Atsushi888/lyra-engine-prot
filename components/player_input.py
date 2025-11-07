# components/player_input.py
import streamlit as st

TEXT_KEY = "user_input_box"
FORM_KEY = "user_input_form"


class PlayerInput:
    """ユーザーの入力欄＋送信ボタン担当"""

    def render(self) -> str:
        """
        入力欄と「送信」ボタンを描画し、
        ボタンが押されたときだけ確定テキストを返す。
        それ以外は空文字を返す。
        """

        # ここでは session_state に触らない
        # （ストリームリット側が自動で作るのに任せる）

        with st.form(key=FORM_KEY):
            user_input = st.text_area(
                "あなたの発言を入力:",
                key=TEXT_KEY,
                height=160,
            )
            submitted = st.form_submit_button("送信")

        if not submitted:
            return ""

        text = (user_input or "").strip()
        if not text:
            return ""

        # 入力欄をクリアしたいが、ここでの書き込みが環境によっては
        # StreamlitAPIException を出すことがあるので保険をかける
        try:
            st.session_state[TEXT_KEY] = ""
        except Exception:
            # 失敗したら「クリアされない」だけでよしとする
            pass

        return text

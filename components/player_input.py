# components/player_input.py
import streamlit as st


# セッションキーとフォームキーは固定文字列にしてしまう
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

        # セッションにキーがなければ初期化
        if TEXT_KEY not in st.session_state:
            st.session_state[TEXT_KEY] = ""

        # フォームでまとめて描画
        with st.form(key=FORM_KEY):
            user_input = st.text_area(
                "あなたの発言を入力:",
                key=TEXT_KEY,
                height=160,  # 高さはお好みで調整OK
            )
            submitted = st.form_submit_button("送信")

        # ボタンが押されたときだけ判定
        if submitted:
            text = (user_input or "").strip()
            if text:
                # 入力欄をクリア
                st.session_state[TEXT_KEY] = ""
                return text

        # 送信されてない / 空文字のとき
        return ""

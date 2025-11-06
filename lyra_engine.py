# lyra_engine.py
import os
import streamlit as st
from personas import get_persona
from components import PreflightChecker, DebugPanel, ChatLog


st.set_page_config(page_title="Lyra Engine – フローリア", layout="wide")
st.write("✅ Lyra Engine 起動テスト：ここまでは通ってます。")


class LyraEngine:
    MAX_LOG = 500
    DISPLAY_LIMIT = 20000

    def __init__(self):
        persona = get_persona("floria_ja")
        self.system_prompt = persona.system_prompt
        self.starter_hint = persona.starter_hint
        self.partner_name = persona.name

        # APIキー
        self.openai_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))
        self.openrouter_key = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))

        if not self.openai_key:
            st.error("OPENAI_API_KEY が未設定です。")
            st.stop()

        os.environ["OPENAI_API_KEY"] = self.openai_key
        if self.openrouter_key:
            os.environ["OPENROUTER_API_KEY"] = self.openrouter_key

        # UIコンポーネント生成
        self.preflight = PreflightChecker(self.openai_key, self.openrouter_key)
        self.debug_panel = DebugPanel()
        self.chat_log = ChatLog(self.partner_name, self.DISPLAY_LIMIT)

    def render(self):
        """アプリの描画をまとめて行う"""
        st.write("🛫 PreflightChecker.render() 呼び出し前")
        self.preflight.render()
        st.write("🛬 PreflightChecker.render() 呼び出し後")

        with st.sidebar:
            self.debug_panel.render()

        self.chat_log.render()


# === ここがエントリーポイント ===
if __name__ == "__main__":
    engine = LyraEngine()
    engine.render()

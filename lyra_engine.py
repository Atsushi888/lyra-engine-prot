# lyra_engine.py — Lyra Engine Prototype (Streamlit Edition, GPT-4o + Hermes fallback)
# 2025-11-07 build with PreflightChecker + DebugPanel integration

import os
import json
import html
import time
import streamlit as st
from typing import Any, Dict, List, Tuple

from personas import get_persona
from llm_router import call_with_fallback


# ==========================================================
# PreflightChecker：APIキー有効性診断クラス
# ==========================================================
class PreflightChecker:
    """OpenAI / OpenRouter キーの有効性を診断"""

    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY", "")

    def check_openai(self) -> bool:
        return bool(self.openai_key and self.openai_key.startswith("sk-"))

    def check_openrouter(self) -> bool:
        return bool(self.openrouter_key and self.openrouter_key.startswith("sk-or-"))

    def run_all(self) -> Dict[str, bool]:
        return {
            "openai": self.check_openai(),
            "openrouter": self.check_openrouter(),
        }

    def render(self):
        results = self.run_all()
        with st.expander("🔍 起動前診断 (Preflight)", expanded=True):
            if results["openai"]:
                st.success("✅ OPENAI: OpenAI APIキーは有効です。")
            else:
                st.error("❌ OPENAI: OpenAI APIキーが未設定か無効です。")

            if results["openrouter"]:
                st.success("✅ OPENROUTER: OpenRouter キー有効（Hermes 利用可）。")
            else:
                st.warning("⚠️ OPENROUTER: キーが設定されていません。Hermesフォールバック不可。")

        return results


# ==========================================================
# DebugPanel：デバッグ出力表示クラス
# ==========================================================
class DebugPanel:
    """LLM呼び出しメタ情報の可視化ヘルパ"""
    def __init__(self, state_key: str = "_last_call_meta"):
        self.state_key = state_key

    def set_meta(self, meta: dict) -> None:
        if meta:
            st.session_state[self.state_key] = meta

    def clear(self) -> None:
        st.session_state.pop(self.state_key, None)

    def render(self) -> None:
        show_dbg = st.checkbox("🧠 デバッグを表示", False)
        if not show_dbg:
            return
        if self.state_key not in st.session_state:
            st.info("まだ LLM 呼び出し情報はありません。")
            return
        st.markdown("###### 最後の呼び出し情報")
        st.json(st.session_state[self.state_key])


# ==========================================================
# LyraEngine：アプリ本体
# ==========================================================
class LyraEngine:
    def __init__(self, persona_id: str = "floria_ja"):
        self.persona = get_persona(persona_id)
        self.preflight = PreflightChecker()
        self.debug_panel = DebugPanel()

        # 会話用設定
        self.temperature = 0.7
        self.max_tokens = 800
        self.wrap_width = 80

        # APIキー診断
        self.results = self.preflight.run_all()

        # セッション初期化
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "system", "content": self.persona.system_prompt}]
        if "user_input" not in st.session_state:
            st.session_state["user_input"] = ""

    # ======================================================
    # 会話送信ロジック
    # ======================================================
    def send_message(self, user_text: str):
        if not user_text.strip():
            return

        # 履歴に追加
        st.session_state["messages"].append({"role": "user", "content": user_text})

        # コンテキスト整形
        base = st.session_state["messages"]
        convo = [base[0]] + base[-60:]

        # LLM呼び出し
        with st.spinner(f"{self.persona.name}が考えています…"):
            reply, meta = call_with_fallback(
                convo,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

        # メタデータ保存
        self.debug_panel.set_meta(meta)

        if not reply.strip():
            reply = "（返答の生成に失敗しました…）"

        st.session_state["messages"].append({"role": "assistant", "content": reply})

    # ======================================================
    # UIレンダリング群
    # ======================================================
    def render_header(self):
        st.set_page_config(page_title="Lyra Engine — フローリア", layout="wide")
        st.title("❄️ Lyra Engine — フローリア")
        st.caption("Streamlit Edition · Powered by GPT-4o + Hermes")

    def render_preflight(self):
        self.preflight.render()

    def render_settings(self):
        with st.expander("⚙️ 接続設定", expanded=False):
            c1, c2, c3 = st.columns(3)
            self.temperature = c1.slider("temperature", 0.0, 1.5, 0.70, 0.05)
            self.max_tokens = c2.slider("max_tokens（1レス上限）", 64, 4096, 800, 16)
            self.wrap_width = c3.slider("折り返し幅", 20, 100, 80, 1)
        st.markdown(f"<style>.chat-bubble{{max-width:min(90vw,{self.wrap_width}ch);}}</style>", unsafe_allow_html=True)

    def render_chat(self):
        st.subheader("💬 会話ログ")
        dialog = [m for m in st.session_state["messages"] if m["role"] in ("user", "assistant")]
        for m in dialog:
            role = "あなた" if m["role"] == "user" else self.persona.name
            raw = m["content"].strip()
            txt = html.escape(raw[:20000])  # safety
            color = "#f4f6fb" if m["role"] == "user" else "#eaf7ff"
            st.markdown(
                f"<div style='background:{color};border-radius:.6rem;padding:.7rem 1rem;margin:.3rem 0;'>"
                f"<b>{role}：</b><br>{txt}</div>",
                unsafe_allow_html=True,
            )

    def render_input(self):
        st.markdown("---")
        user_text = st.text_area("あなたの言葉（複数行OK）", key="user_input", height=160)
        if st.button("送信", type="primary"):
            self.send_message(user_text)
            st.session_state["user_input"] = ""
            st.rerun()

    # ======================================================
    # 実行エントリポイント
    # ======================================================
    def run(self):
        self.render_header()
        self.render_preflight()
        self.render_settings()
        self.render_chat()
        self.debug_panel.render()  # デバッグ出力をここで描画
        self.render_input()


# ==========================================================
# Streamlit 実行エントリ
# ==========================================================
if __name__ == "__main__":
    engine = LyraEngine("floria_ja")
    engine.run()

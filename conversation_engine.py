# conversation_engine.py — LLM 呼び出しを統括する会話エンジン層

from typing import Any, Dict, List, Tuple

from llm_router import call_with_fallback


class LLMConversation:
    """
    system プロンプト（フローリア人格）と LLM 呼び出しをまとめた会話エンジン。
    まずは GPT-4o に対して、
    「フローリアの system_prompt ＋ 直近のユーザー本文」
    だけを投げるシンプル構成にする。
    """

    def __init__(
        self,
        system_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 800,
    ) -> None:
        self.system_prompt = system_prompt
        self.temperature = float(temperature)
        self.max_tokens = int(max_tokens)

        # 必要最小限のスタイルヒントだけ足す
        self.style_hint = (
            "あなたは上記の system プロンプトで定義されたフローリアとして振る舞います。\n"
            "ユーザーは物語の本文（地の文と会話文）を日本語で入力します。\n"
            "直前のユーザーの本文をよく読み、その続きとして自然につながる文章を、日本語で2〜4文だけ出力してください。\n"
            "見出しや箇条書き、英語のタグ（onstage:, onscreen: など）は使わず、素の文章だけを書いてください。"
        )

    # ===== 実際に GPT-4o に渡す messages を組み立てる =====
    def build_messages(self, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        今は「フローリア人格（system）＋直近の user メッセージ」だけを LLM に渡す。
        """

        # 1) system（フローリア人格＋スタイルヒント）
        system_content = self.system_prompt
        if self.style_hint:
            system_content += "\n\n" + self.style_hint

        messages: List[Dict[str, str]] = [
            {"role": "system", "content": system_content}
        ]

        # 2) history から「最後の user メッセージ」だけ拾う
        last_user_content = None
        for m in reversed(history):
            if m.get("role") == "user":
                last_user_content = m.get("content", "")
                break

        if last_user_content:
            messages.append(
                {"role": "user", "content": last_user_content}
            )
        else:
            # 念のため、user がまだいない場合（通常は起こらない）
            messages.append(
                {
                    "role": "user",
                    "content": "（ユーザーはまだ何も話していませんが、"
                               "フローリアとして軽く自己紹介してください）",
                }
            )

        return messages

    # ===== GPT-4o に実際に投げる部分 =====
    def generate_reply(
        self,
        history: List[Dict[str, str]],
    ) -> Tuple[str, Dict[str, Any]]:
        messages = self.build_messages(history)

        text, meta = call_with_fallback(
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        # デバッグ用：何を投げたかを meta に埋め込んでおく
        meta = dict(meta)
        meta["prompt_messages"] = messages
        meta["prompt_preview"] = "\n\n".join(
            f"[{m['role']}] {m['content'][:200]}"
            for m in messages
        )

        return text, meta

# llm_router.py — GPT-4o 専用シンプルルーター

import os
from typing import Any, Dict, List, Tuple

from openai import OpenAI


# ====== 環境変数 ======
# ※ import 時の値は「初期値」として持つが、
#    実際の呼び出しでは毎回 os.getenv(...) を見る。
OPENAI_API_KEY_INITIAL = os.getenv("OPENAI_API_KEY")

# メイン側（GPT系）のモデル名
MAIN_MODEL = os.getenv("OPENAI_MAIN_MODEL", "gpt-4o")


# ====== GPT系（メイン） ======
def _call_gpt(
    messages: List[Dict[str, str]],
    temperature: float,
    max_tokens: int,
) -> Tuple[str, Dict[str, Any]]:
    """
    OpenAI GPT 系モデル（デフォルト gpt-4o）に対する単発呼び出し。
    Hermes / OpenRouter などは一切使わない。
    """

    # 呼び出し時点での環境変数を見る
    api_key = os.getenv("OPENAI_API_KEY") or OPENAI_API_KEY_INITIAL
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY が設定されていません。")

    client_openai = OpenAI(api_key=api_key)

    resp = client_openai.chat.completions.create(
        model=MAIN_MODEL,
        messages=messages,
        temperature=float(temperature),
        max_tokens=int(max_tokens),
    )

    text = resp.choices[0].message.content or ""

    usage: Dict[str, Any] = {}
    if getattr(resp, "usage", None) is not None:
        usage = {
            "prompt_tokens": getattr(resp.usage, "prompt_tokens", None),
            "completion_tokens": getattr(resp.usage, "completion_tokens", None),
            "total_tokens": getattr(resp.usage, "total_tokens", None),
        }

    return text, usage


# ====== 公開インターフェース ======
def call_with_fallback(
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: int = 800,
) -> Tuple[str, Dict[str, Any]]:
    """
    以前は GPT → Hermes のフォールバックだったが、
    今は GPT-4o 単体のみを呼び出す。
    """
    meta: Dict[str, Any] = {}

    try:
        text, usage = _call_gpt(messages, temperature, max_tokens)
        meta["route"] = "gpt"
        meta["model_main"] = MAIN_MODEL
        meta["usage_main"] = usage
        return text, meta
    except Exception as e:
        meta["route"] = "error"
        meta["gpt_error"] = str(e)
        return "", meta

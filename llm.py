import os
from anthropic import Anthropic

from config import CLAUDE_MODEL


def load_claude_client() -> Anthropic:
    return Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def ask_claude(client: Anthropic, conversation_history: list, prompt: str) -> str:
    conversation_history.append({"role": "user", "content": prompt})

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=200,
        messages=conversation_history,
    )

    reply_text = next(
        (block.text for block in response.content if block.type == "text"), ""
    )
    conversation_history.append({"role": "assistant", "content": reply_text})
    return reply_text
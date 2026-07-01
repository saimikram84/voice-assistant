import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def ask_claude(prompt: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=200,
        messages=[{"role":'user', "content": prompt}]
    )
    return response.content[0].text


if __name__ == "__main__":
    reply = ask_claude("In one short sentence, confirm you're working.")
    print("Claude says:", reply)
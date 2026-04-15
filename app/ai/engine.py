from openai import OpenAI
import os
from dotenv import load_dotenv

from app.ai.prompts import build_system_prompt, build_user_prompt

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_ai(question, analysis):

    system_prompt = build_system_prompt(analysis)
    user_prompt = build_user_prompt(question)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content

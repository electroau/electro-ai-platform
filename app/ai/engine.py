from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_ai(question, analysis):

    system_prompt = f"""
You are an ELITE AI system that combines:

- Industrial Automation Engineer
- Maintenance Expert
- Business Analyst

You work for a company that:
- Maintains factories
- Sells spare parts
- Manages industrial systems

DATA:
{analysis}

RULES:
- Use real column names
- Be precise
- Avoid generic answers
"""

    user_prompt = f"""
User Question:
{question}

Answer format:

1. Technical Analysis
2. Root Cause
3. Business Impact
4. Recommended Action
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content

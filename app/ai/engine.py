from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_ai(question, analysis):

    prompt = f"""
You are an expert industrial engineer and business analyst.

Analyze the following company data:

{analysis}

User question:
{question}

Instructions:
- Be specific
- Use column names
- Give real insights
- Suggest actions

Answer format:

1. Problem Analysis
2. Root Cause
3. Business Impact
4. Recommended Action
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

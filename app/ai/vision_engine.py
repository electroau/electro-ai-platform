from typing import Dict
import base64
import os
from openai import OpenAI


class VisionEngine:
    """
    Industrial Vision Engine (Production Ready)

    - Real AI vision analysis
    - Industrial-focused reasoning
    - Safe fallback (no crash)
    """

    def __init__(self):
        self.client = OpenAI()

    # =========================
    # Encode Image
    # =========================
    def encode_image(self, file_path: str) -> str:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    # =========================
    # Analyze Image 🔥
    # =========================
    def analyze(self, image_path: str) -> Dict:

        # 🔒 Safety check
        if not image_path or not os.path.exists(image_path):
            return {
                "image_path": image_path,
                "analysis": "Image not found"
            }

        try:
            base64_image = self.encode_image(image_path)

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """
You are a SENIOR INDUSTRIAL ENGINEER.

Analyze the image as a REAL industrial system.

Focus on:
- Equipment type
- Indicators (LEDs, alarms)
- System state (running / stopped / fault)
- Abnormal conditions

DO NOT describe casually.
Think like a field engineer diagnosing a real system.

Return clear technical analysis.
"""
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Analyze this industrial system image"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ]
            )

            return {
                "image_path": image_path,
                "analysis": response.choices[0].message.content
            }

        except Exception as e:
            # 🔥 لا يكسر النظام
            return {
                "image_path": image_path,
                "analysis": "Vision analysis failed",
                "error": str(e)
            }

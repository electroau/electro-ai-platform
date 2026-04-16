from typing import Dict
import base64
import os
from openai import OpenAI


class VisionEngine:
    """
    Industrial Vision Engine

    Features:
    - Real AI vision analysis
    - Industrial-focused reasoning
    - Safe fallback if API fails
    - Ready for system integration
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

        if not image_path or not os.path.exists(image_path):
            return {
                "error": "Image not found",
                "analysis": None
            }

        try:
            base64_image = self.encode_image(image_path)

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """
You are a SENIOR INDUSTRIAL ENGINEER with expertise in:

- PLC systems
- HMI panels
- SCADA systems
- Industrial equipment
- Electrical & mechanical systems

Analyze the image as a REAL industrial system.

Focus on:
- Equipment type
- Indicators (LEDs, alarms)
- System state (running / stopped / fault)
- Abnormal conditions

DO NOT describe the image casually.
Think like a field engineer diagnosing a real system.

Return structured analysis.
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

            result_text = response.choices[0].message.content

            return {
                "image_path": image_path,
                "analysis": result_text
            }

        except Exception as e:
            # 🔥 مهم جداً: لا نكسر النظام
            return {
                "image_path": image_path,
                "analysis": "Vision analysis failed",
                "error": str(e)
            }

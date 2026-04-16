from typing import Dict

from app.ai.engines.troubleshooting_engine import TroubleshootingEngine
from app.ai.engines.analysis_engine import AnalysisEngine
from app.ai.engines.qa_engine import QAEngine


class AIRouter:

    def __init__(self):
        self.troubleshooting_engine = TroubleshootingEngine()
        self.analysis_engine = AnalysisEngine()
        self.qa_engine = QAEngine()

    # =========================
    # Smart Intent Detection 🔥
    # =========================
    def detect_intent(self, question: str, context: Dict = None) -> str:
        q = (question or "").lower()
        context = context or {}

        equipment = context.get("equipment")
        analysis = context.get("analysis")

        # =========================
        # 1. Troubleshooting Detection
        # =========================
        troubleshooting_keywords = [
            "error", "alarm", "fault", "not working",
            "fail", "trip", "issue", "problem"
        ]

        if any(word in q for word in troubleshooting_keywords):
            return "troubleshooting"

        # وجود معدة + مشكلة ضمنية → Troubleshooting
        if equipment and any(word in q for word in ["low", "high", "not", "delay"]):
            return "troubleshooting"

        # =========================
        # 2. Analysis Detection
        # =========================
        analysis_keywords = [
            "analyze", "analysis", "data", "report",
            "trend", "pattern"
        ]

        if any(word in q for word in analysis_keywords):
            return "analysis"

        # وجود ملف مرفوع + سؤال → Analysis
        if analysis:
            return "analysis"

        # =========================
        # 3. Business / QA Detection
        # =========================
        business_keywords = [
            "price", "cost", "profit", "sales",
            "stock", "inventory", "buy", "sell"
        ]

        if any(word in q for word in business_keywords):
            return "qa"

        # =========================
        # 4. Default
        # =========================
        return "qa"

    # =========================
    # Routing 🔥
    # =========================
    def route(self, question: str, context: Dict):

        intent = self.detect_intent(question, context)

        # =========================
        # Engine Execution
        # =========================
        if intent == "troubleshooting":
            return self.troubleshooting_engine.run(question, context)

        elif intent == "analysis":
            return self.analysis_engine.run(question, context)

        else:
            return self.qa_engine.run(question, context)

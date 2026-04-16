from app.ai.engines.troubleshooting_engine import TroubleshootingEngine
from app.ai.engines.analysis_engine import AnalysisEngine
from app.ai.engines.qa_engine import QAEngine


class AIRouter:

    def __init__(self):
        self.troubleshooting_engine = TroubleshootingEngine()
        self.analysis_engine = AnalysisEngine()
        self.qa_engine = QAEngine()

    def detect_intent(self, question: str):

        q = question.lower()

        if any(word in q for word in [
            "error", "alarm", "fault", "not working",
            "fail", "trip", "issue", "problem"
        ]):
            return "troubleshooting"

        if any(word in q for word in [
            "analyze", "analysis", "trend", "pattern",
            "data", "report", "insight"
        ]):
            return "analysis"

        return "qa"

    def route(self, question, analysis):

        intent = self.detect_intent(question)

        if intent == "troubleshooting":
            return self.troubleshooting_engine.run(question, analysis)

        elif intent == "analysis":
            return self.analysis_engine.run(question, analysis)

        else:
            return self.qa_engine.run(question, analysis)

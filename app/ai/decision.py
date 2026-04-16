class DecisionEngine:

    def analyze(self, ai_response: str, question: str = ""):
        """
        Intelligent decision engine:
        - Context-aware (يفهم السؤال)
        - Safe (لا يكسر النظام)
        - Expandable (قابل للتطوير)
        """

        # 🔒 Safety checks
        if not ai_response or not isinstance(ai_response, str):
            return []

        decisions = []

        text = ai_response.lower()
        q = (question or "").lower()

        # =========================
        # 1. Ignore analysis-type questions
        # =========================
        if any(word in q for word in [
            "what", "summary", "note", "analyze",
            "analysis", "report", "describe"
        ]):
            return []

        # =========================
        # 2. Detect problem context
        # =========================
        problem_keywords = [
            "error", "alarm", "fault", "not working",
            "fail", "trip", "issue", "problem"
        ]

        is_problem = any(word in q for word in problem_keywords)

        if not is_problem:
            return []

        # =========================
        # 3. Equipment-based decisions
        # =========================

        # 🔧 Pump issues
        if "pump" in text and any(k in text for k in ["trip", "fault", "fail"]):
            decisions.append("Create URGENT work order for pump inspection")

        # 🔧 Valve issues
        if "valve" in text and any(k in text for k in ["fault", "fail", "not open", "not close"]):
            decisions.append("Check valve actuator and position feedback")

        # 🔧 Pressure issues
        if "pressure" in text and any(k in text for k in ["high", "low"]):
            decisions.append("Inspect pressure control system immediately")

        # =========================
        # 4. Fallback (Smart default)
        # =========================
        if not decisions:
            decisions.append("Perform general system diagnostic check")

        return decisions

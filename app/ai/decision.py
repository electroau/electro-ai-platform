class DecisionEngine:

    def analyze(self, ai_response: str):

        decisions = []

        text = ai_response.lower()

        if "pump tripped" in text:
            decisions.append("Create URGENT work order for pump inspection")

        if "valve fault" in text:
            decisions.append("Check valve actuator and position feedback")

        if "high pressure" in text:
            decisions.append("Inspect pressure control system immediately")

        return decisions

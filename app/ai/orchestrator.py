class AIOrchestrator:

    def __init__(self, router, decision_engine, action_executor):
        self.router = router
        self.decision_engine = decision_engine
        self.action_executor = action_executor

    def run(self, question, analysis):

        # 🧠 AI يفهم السؤال
        response = self.router.route(question, analysis)

        # 🧠 AI يقرر (إذا يحتاج)
        decisions = self.decision_engine.analyze(response)

        # ⚙️ AI ينفذ (إذا فيه قرارات)
        actions = self.action_executor.execute(decisions)

        return {
            "response": response,
            "decisions": decisions,
            "actions": actions
        }

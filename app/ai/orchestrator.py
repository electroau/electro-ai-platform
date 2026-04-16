from app.ai.system_builder import SystemContextBuilder


class AIOrchestrator:

    def __init__(self, router, decision_engine, action_executor):
        self.router = router
        self.decision_engine = decision_engine
        self.action_executor = action_executor
        self.system_builder = SystemContextBuilder()

    def run(self, question: str, context: dict):

        # 🔥 Universal System Context
        system_context = self.system_builder.build(question, context)

        full_context = {
            **context,
            "system": system_context
        }

        response = self.router.route(question, full_context)

        decisions = self.decision_engine.analyze(
            ai_response=response,
            question=question,
            context=full_context
        )

        actions = self.action_executor.execute(decisions)

        return {
            "response": response,
            "decisions": decisions,
            "actions": actions,
            "system_context": system_context
        }

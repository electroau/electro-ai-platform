class AIOrchestrator:

    def __init__(self, router, decision_engine, action_executor):
        self.router = router
        self.decision_engine = decision_engine
        self.action_executor = action_executor

    def run(self, question: str, context: dict):

        # =========================
        # Extract Context 🔥
        # =========================
        client = context.get("client")
        equipment = context.get("equipment")
        history = context.get("history", [])
        analysis = context.get("analysis", {})

        # =========================
        # Build AI Input Context 🧠
        # =========================
        ai_context = {
            "question": question,
            "client": client,
            "equipment": equipment,
            "history": history,
            "analysis": analysis
        }

        # =========================
        # Step 1: AI Understanding
        # =========================
        response = self.router.route(question, ai_context)

        # =========================
        # Step 2: Decision Engine
        # =========================
        decisions = self.decision_engine.analyze(
            ai_response=response,
            question=question,
            context=ai_context
        )

        # =========================
        # Step 3: Action Execution
        # =========================
        actions = self.action_executor.execute(decisions)

        # =========================
        # Step 4: Build Final Output 🔥
        # =========================
        result = {
            "response": response,
            "decisions": decisions,
            "actions": actions,
            "context_used": {
                "client": client.get("name") if client else None,
                "equipment": equipment.get("name") if equipment else None,
                "history_count": len(history)
            }
        }

        return result

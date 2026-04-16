from app.ai.system_builder import SystemContextBuilder
from app.ai.knowledge_retriever import KnowledgeRetriever


class AIOrchestrator:

    def __init__(self, router, decision_engine, action_executor):
        self.router = router
        self.decision_engine = decision_engine
        self.action_executor = action_executor
        self.system_builder = SystemContextBuilder()
        self.knowledge_retriever = KnowledgeRetriever()

    def run(self, question: str, context: dict):

        # =========================
        # 1. Build System Context
        # =========================
        system_context = self.system_builder.build(question, context)

        # =========================
        # 2. Extract Model 🔥
        # =========================
        model = self.knowledge_retriever.extract_model(question)

        external_knowledge = {}
        if model:
            external_knowledge = self.knowledge_retriever.retrieve(model)

        # =========================
        # 3. Merge Context
        # =========================
        full_context = {
            **context,
            "system": system_context,
            "external_knowledge": external_knowledge
        }

        # =========================
        # 4. AI Response
        # =========================
        response = self.router.route(question, full_context)

        # =========================
        # 5. Decisions
        # =========================
        decisions = self.decision_engine.analyze(
            ai_response=response,
            question=question,
            context=full_context
        )

        # =========================
        # 6. Actions
        # =========================
        actions = self.action_executor.execute(decisions)

        return {
            "response": response,
            "decisions": decisions,
            "actions": actions,
            "system_context": system_context,
            "external_knowledge": external_knowledge
        }

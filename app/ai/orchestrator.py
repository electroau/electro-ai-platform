from app.ai.system_builder import SystemContextBuilder
from app.ai.knowledge_retriever import KnowledgeRetriever
from app.ai.semantic_rag import SemanticRAG
from app.ai.vision_engine import VisionEngine


class AIOrchestrator:

    def __init__(self, router, decision_engine, action_executor):
        self.router = router
        self.decision_engine = decision_engine
        self.action_executor = action_executor

        self.system_builder = SystemContextBuilder()
        self.knowledge_retriever = KnowledgeRetriever()
        self.rag = SemanticRAG()
        self.vision = VisionEngine()

    def run(self, question: str, context: dict):

        system_context = self.system_builder.build(question, context)

        # 🔥 Vision (إذا فيه صورة)
        image_path = context.get("image_path")
        image_analysis = {}

        if image_path:
            image_analysis = self.vision.analyze(image_path)

        model = self.knowledge_retriever.extract_model(question)

        external_knowledge = {}
        if model:
            external_knowledge = self.knowledge_retriever.retrieve(model)

        rag_results = self.rag.search(question)

        full_context = {
            **context,
            "system": system_context,
            "external_knowledge": external_knowledge,
            "rag": rag_results,
            "vision": image_analysis
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
            "vision": image_analysis
        }

from utils.preprocessing import TextPreprocessor
from utils.vector_store import VectorStore
from utils.retriever import Retriever

from engine.intent_manager import IntentManager
from engine.entity_extractor import EntityExtractor
from engine.knowledge_manager import KnowledgeManager
from engine.knowledge_resolver import KnowledgeResolver
from engine.response_manager import ResponseManager

from logs.logger import ConversationLogger


class Chatbot:

    def __init__(self):

        self.preprocessor = TextPreprocessor()

        self.vector_store = VectorStore()
        self.vector_store.load()

        self.retriever = Retriever(
            self.vector_store
        )

        self.intent_manager = IntentManager()

        self.entity_extractor = EntityExtractor()

        self.knowledge_manager = KnowledgeManager()

        self.knowledge_resolver = KnowledgeResolver(
            self.knowledge_manager
        )

        self.response_manager = ResponseManager()

        self.logger = ConversationLogger()

    def reply(self, message):

        # ==========================================
        # 1. PREPROCESSING
        # ==========================================

        clean_text = self.preprocessor.clean(message)

        # ==========================================
        # 2. ENTITY DETECTION AWAL
        # ==========================================

        detected_entities = self.entity_extractor.extract(
            clean_text
        )

        print("\n===== ENTITY DETECTED =====")
        print(detected_entities)
        print("===========================\n")

        # ==========================================
        # 3. RETRIEVAL
        # ==========================================

        best, score, top_results = self.retriever.search(

            question=clean_text,

            entities=detected_entities

        )

        print("\n===== TOP RESULTS =====")

        for item in top_results:

            print(
                item["intent"],
                "|",
                round(item["score"], 4),
                "|",
                item["pattern"]
            )

        print("=======================\n")

        # ==========================================
        # 4. BONUS SCORE JIKA ENTITY DITEMUKAN
        # ==========================================

        if detected_entities:

            score += 0.05

            if score > 1.0:
                score = 1.0

        # ==========================================
        # 5. THRESHOLD ADAPTIF
        # ==========================================

        original_threshold = self.intent_manager.threshold

        if detected_entities:
            self.intent_manager.threshold = 0.65
        else:
            self.intent_manager.threshold = 0.70

        # ==========================================
        # 6. DECISION
        # ==========================================

        decision = self.intent_manager.decide(

            top_results,

            detected_entities

        )

        # kembalikan threshold
        self.intent_manager.threshold = original_threshold

        # ==========================================
        # UNKNOWN
        # ==========================================

        if decision["status"] == "unknown":

            response = self.response_manager.unknown(
                score
            )

            self.logger.log({

                "question": message,

                "clean_text": clean_text,

                "intent": "unknown",

                "category": "",

                "entities": detected_entities

            })

            return response

        # ==========================================
        # CLARIFICATION
        # ==========================================

        if decision["status"] == "clarification":

            response = self.response_manager.clarification(

                decision["options"],

                score

            )

            self.logger.log({

                "question": message,

                "clean_text": clean_text,

                "intent": "clarification",

                "category": "",

                "entities": detected_entities

            })

            return response

        # ==========================================
        # 7. INTENT TERPILIH
        # ==========================================

        intent = decision["intent"]

        # ==========================================
        # 8. ENTITY FINAL
        # ==========================================

        required_entities = intent.get(
            "entities",
            []
        )

        entities = self.entity_extractor.extract(

            clean_text,

            required_entities

        )

        print("Intent  :", intent["intent"])
        print("Entities:", entities)

        # ==========================================
        # 9. KNOWLEDGE RESOLVER
        # ==========================================

        knowledge = self.knowledge_resolver.resolve(

            intent,

            entities

        )

        # ==========================================
        # 10. RESPONSE
        # ==========================================

        response = self.response_manager.generate(

            intent_data=intent,

            entities=entities,

            score=score,

            knowledge=knowledge

        )

        # ==========================================
        # 11. LOG
        # ==========================================

        self.logger.log({

            "question": message,

            "clean_text": clean_text,

            "intent": response["intent"],

            "category": response["category"],

            "entities": response["entities"]

        })

        return response
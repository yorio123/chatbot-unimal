from utils.loader import load_knowledge_base
from utils.vector_store import VectorStore

knowledge = load_knowledge_base()

vector_store = VectorStore()

vector_store.build(knowledge)

print("\nSelesai membangun Vector Index.")
import json

def load_knowledge_base(path="knowledge_base.json"):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
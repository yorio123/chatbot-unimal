import os
import pickle
import numpy as np

from models.embedding_model import EmbeddingModel


class VectorStore:

    def __init__(self):

        self.embedding_model = EmbeddingModel()

        self.embeddings = None
        self.metadata = None

    def build(self, knowledge):

        patterns = []
        metadata = []

        for item in knowledge:

            for pattern in item["patterns"]:

                patterns.append(pattern)

                metadata.append({

                    "id": len(metadata),

                    "intent": item["intent"],

                    "category": item.get("category", ""),

                    "responses": item["responses"],

                    "pattern": pattern,

                    "entities": item.get("entities", []),

                    "knowledge_source": item.get(
                        "knowledge_source",
                        None
                    )

                })

        print(f"\nMengubah {len(patterns)} pattern menjadi embedding...")

        embeddings = self.embedding_model.encode(patterns)
        print("\n===== CEK INDEX =====")
        for i in range(20):
            print(
                metadata[i]["intent"],
                "|",
                metadata[i]["pattern"]
            )

        print("=====================\n")

        os.makedirs("cache", exist_ok=True)

        np.save(
            "cache/embeddings.npy",
            embeddings
        )

        with open(
            "cache/metadata.pkl",
            "wb"
        ) as f:

            pickle.dump(metadata, f)

        print("Vector Index berhasil disimpan.")

    def load(self):

        self.embeddings = np.load(
            "cache/embeddings.npy"
        )

        with open(
            "cache/metadata.pkl",
            "rb"
        ) as f:

            self.metadata = pickle.load(f)

        print("Vector Index berhasil dimuat.")
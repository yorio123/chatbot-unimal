from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class Retriever:

    def __init__(
        self,
        vector_store,
        threshold=0.70,
        entity_bonus=0.08
    ):

        self.vector_store = vector_store
        self.threshold = threshold
        self.entity_bonus = entity_bonus

    def search(
        self,
        question,
        entities=None,
        top_k=3
    ):

        # ==========================================
        # Encode Question
        # ==========================================

        question_embedding = (
            self.vector_store.embedding_model.encode(
                question
            )
        )

        scores = cosine_similarity(

            question_embedding,

            self.vector_store.embeddings

        )[0]

        print("\n===== ENTITY DETECTED =====")
        print(entities)
        print("===========================\n")

        # ==========================================
        # Entity-aware Re-ranking
        # ==========================================

        if entities:

            entity_dictionary = getattr(
                self.vector_store,
                "entities",
                {}
            )

            for i, item in enumerate(self.vector_store.metadata):

                pattern = item["pattern"].lower()

                intent_entities = item.get(
                    "entities",
                    []
                )

                bonus = 0.0

                matched = 0
                total = 0

                for entity_name, values in entities.items():

                    # --------------------------------------
                    # Intent tidak memakai entity ini
                    # --------------------------------------

                    if entity_name not in intent_entities:
                        continue

                    entity_source = entity_dictionary.get(
                        entity_name,
                        {}
                    )

                    for value in values:

                        total += 1

                        synonyms = entity_source.get(
                            value,
                            [value.replace("_", " ")]
                        )

                        found = False

                        for synonym in synonyms:

                            if synonym.lower() in pattern:

                                found = True
                                break

                        if found:

                            matched += 1
                            bonus += self.entity_bonus

                # --------------------------------------
                # Semua entity cocok
                # --------------------------------------

                if total > 0 and matched == total:

                    bonus += 0.10

                # --------------------------------------
                # Lebih dari satu entity cocok
                # --------------------------------------

                if matched >= 2:

                    bonus += 0.05

                # --------------------------------------
                # Maksimum skor 1.0
                # --------------------------------------

                if bonus > 0:

                    scores[i] = min(

                        scores[i] + bonus,

                        1.0

                    )

                    print(

                        f"BONUS +{bonus:.2f}",

                        "|",

                        item["intent"],

                        "|",

                        item["pattern"]

                    )

        # ==========================================
        # DEBUG TOP 10
        # ==========================================

        top10 = np.argsort(scores)[::-1][:10]

        print("\n===== DEBUG TOP 10 =====")

        for idx in top10:

            item = self.vector_store.metadata[idx]

            print(

                round(scores[idx], 4),

                "|",

                item["intent"],

                "|",

                item["pattern"]

            )

        print("=========================\n")

        # ==========================================
        # TOP K
        # ==========================================

        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []

        for idx in top_indices:

            item = self.vector_store.metadata[idx].copy()

            item["score"] = float(scores[idx])

            results.append(item)

        if not results:

            return None, 0.0, []

        best = results[0]

        if best["score"] < self.threshold:

            return None, best["score"], results

        return best, best["score"], results
    
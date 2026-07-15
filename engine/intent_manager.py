class IntentManager:

    def __init__(
        self,
        threshold=0.70,
        ambiguity_gap=0.01
    ):

        self.threshold = threshold
        self.ambiguity_gap = ambiguity_gap

    def decide(
        self,
        top_results,
        entities=None
    ):

        if entities is None:
            entities = {}

        # ==========================================
        # Tidak ada kandidat
        # ==========================================

        if not top_results:

            return {
                "status": "unknown"
            }

        best = top_results[0]

        # ==========================================
        # Threshold minimum
        # ==========================================

        if best["score"] < self.threshold:

            return {
                "status": "unknown"
            }

        # ==========================================
        # Jika ada entity,
        # jangan terlalu mudah clarification
        # ==========================================

        entity_count = sum(
            len(v)
            for v in entities.values()
        )

        if len(top_results) >= 2:

            second = top_results[1]

            score_gap = (
                best["score"]
                -
                second["score"]
            )

            # --------------------------------------
            # Tidak ada entity
            # --------------------------------------

            if entity_count == 0:

                if (
                    best["intent"] != second["intent"]
                    and score_gap < self.ambiguity_gap
                    and second["score"] >= 0.90
                ):

                    return {

                        "status": "clarification",

                        "options": [
                            best,
                            second
                        ]
                    }

            # --------------------------------------
            # Ada entity
            # Misal:
            # wr1
            # email
            # informatika
            # fkip
            # dll
            #
            # Langsung percaya intent terbaik.
            # --------------------------------------

            else:

                return {

                    "status": "success",

                    "intent": best
                }

        # ==========================================
        # Berhasil
        # ==========================================

        return {

            "status": "success",

            "intent": best
        }
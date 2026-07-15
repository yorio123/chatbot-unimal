import random


class ResponseManager:

    def generate(
        self,
        intent_data,
        entities=None,
        score=0.0,
        knowledge=None
    ):

        if entities is None:
            entities = {}

        responses = intent_data.get(
            "responses",
            [
                "Maaf, saya tidak memiliki jawaban."
            ]
        )

        final_response = random.choice(responses)

        # ==========================================
        # Tambahkan Knowledge
        # ==========================================

        if knowledge:

            knowledge_type = knowledge.get("type")

            # ======================================
            # ATTRIBUTE
            # ======================================

            if knowledge_type == "attribute":

                label = knowledge.get("label", "")
                value = knowledge.get("value")

                final_response += "\n\n"

                if label:
                    final_response += f"{label}\n"

                # ------------------------------
                # STRING
                # ------------------------------

                if isinstance(value, str):

                    final_response += value

                # ------------------------------
                # LIST
                # ------------------------------

                elif isinstance(value, list):

                    for i, item in enumerate(value, start=1):

                        final_response += (
                            f"{i}. {item}\n"
                        )

                # ------------------------------
                # DICTIONARY
                # ------------------------------

                elif isinstance(value, dict):

                    for k, v in value.items():

                        final_response += (
                            f"{k} : {v}\n"
                        )

                # ------------------------------
                # Lainnya
                # ------------------------------

                else:

                    final_response += str(value)

            # ======================================
            # OBJECT
            # ======================================

            elif knowledge_type == "object":

                obj = knowledge["data"]

                for item in obj.values():

                    # label-value
                    if (
                        isinstance(item, dict)
                        and
                        "label" in item
                        and
                        "value" in item
                    ):

                        value = item["value"]

                        final_response += (
                            f"\n\n{item['label']}\n"
                        )

                        if isinstance(value, list):

                            for i, x in enumerate(
                                value,
                                start=1
                            ):

                                final_response += (
                                    f"{i}. {x}\n"
                                )

                        elif isinstance(value, dict):

                            for k, v in value.items():

                                final_response += (
                                    f"{k} : {v}\n"
                                )

                        else:

                            final_response += (
                                f"{value}"
                            )

            # ======================================
            # SUMMARY
            # ======================================

            elif knowledge_type == "summary":

                data = knowledge["data"]

                if (
                    isinstance(data, dict)
                    and
                    "summary" in data
                ):

                    summary = data["summary"]

                    if (
                        isinstance(summary, dict)
                        and
                        "label" in summary
                        and
                        "value" in summary
                    ):

                        final_response += (
                            f"\n\n{summary['label']}\n"
                            f"{summary['value']}"
                        )

        return {

            "success": True,

            "intent": intent_data["intent"],

            "category": intent_data.get(
                "category",
                ""
            ),

            "score": float(score),

            "entities": entities,

            "response": final_response

        }

    # ==========================================
    # UNKNOWN
    # ==========================================

    def unknown(
        self,
        score=0.0
    ):

        responses = [

            "Maaf, saya belum memahami pertanyaan tersebut.",

            "Mohon maaf, saya belum memiliki informasi mengenai pertanyaan tersebut.",

            "Saya belum dapat menemukan jawaban yang sesuai. Silakan gunakan pertanyaan lain.",

            "Maaf, saya belum memahami maksud pertanyaan Anda."

        ]

        return {

            "success": False,

            "intent": "unknown",

            "category": "",

            "score": float(score),

            "entities": {},

            "response": random.choice(
                responses
            )

        }

    # ==========================================
    # CLARIFICATION
    # ==========================================

    def clarification(
        self,
        options,
        score=0.0
    ):

        responses = [

            "Pertanyaan Anda masih ambigu. Apakah yang Anda maksud salah satu dari berikut?",

            "Saya menemukan beberapa kemungkinan maksud dari pertanyaan Anda. Silakan pilih salah satunya.",

            "Mohon diperjelas, apakah yang Anda maksud salah satu dari pilihan berikut?",

            "Saya belum yakin dengan maksud pertanyaan Anda. Mungkin yang Anda maksud adalah salah satu berikut."

        ]

        return {

            "success": False,

            "intent": "clarification",

            "category": "",

            "score": float(score),

            "entities": {},

            "options": options,

            "response": random.choice(
                responses
            )

        }
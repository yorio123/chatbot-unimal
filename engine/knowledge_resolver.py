class KnowledgeResolver:

    def __init__(self, knowledge_manager):

        self.knowledge_manager = knowledge_manager

    def resolve(

        self,

        intent_data,

        entities

    ):

        # ==========================================
        # Ambil knowledge source
        # ==========================================

        knowledge_source = intent_data.get(
            "knowledge_source"
        )

        if not knowledge_source:
            return None

        # ==========================================
        # Ambil seluruh knowledge
        # ==========================================

        knowledge = self.knowledge_manager.get_all(
            knowledge_source
        )

        if knowledge is None:
            return None

        # ==========================================
        # Entity yang dibutuhkan intent
        # ==========================================

        required_entities = intent_data.get(
            "entities",
            []
        )

        # ==========================================
        # Intent tidak membutuhkan entity
        # ==========================================

        if len(required_entities) == 0:

            return {

                "type": "summary",

                "data": knowledge

            }

        # ==========================================
        # Entity pertama
        # ==========================================

        primary_entity = required_entities[0]

        primary_values = entities.get(

            primary_entity,

            []

        )

        # ==========================================
        # Entity utama tidak ditemukan
        # ==========================================

        if len(primary_values) == 0:

            summary = knowledge.get("summary")

            if summary:

                return {

                    "type": "summary",

                    "data": summary

                }

            return None

        # ==========================================
        # Ambil object berdasarkan entity
        # ==========================================

        key = primary_values[0]

        obj = self.knowledge_manager.get(

            knowledge_source,

            key

        )

        if obj is None:
            return None

        # ==========================================
        # Intent hanya memakai satu entity
        # Contoh:
        # kampus_kontak
        # ==========================================

        if len(required_entities) < 2:

            return {

                "type": "object",

                "key": key,

                "data": obj

            }

        # ==========================================
        # Entity kedua (atribut)
        # ==========================================

        attribute_entity = required_entities[1]

        attribute_values = entities.get(

            attribute_entity,

            []

        )

        # ==========================================
        # Tidak meminta atribut tertentu
        # ==========================================

        if len(attribute_values) == 0:

            return {

                "type": "object",

                "key": key,

                "data": obj

            }

        # ==========================================
        # Validasi object
        # ==========================================

        if not isinstance(obj, dict):
            return None

        attribute = attribute_values[0]

        value = obj.get(attribute)

        # ==========================================
        # Attribute tidak ditemukan
        # ==========================================

        if value is None:

            return {

                "type": "object",

                "key": key,

                "data": obj

            }

        # ==========================================
        # Jika value berbentuk object
        # (label + value)
        # ==========================================

        if isinstance(value, dict):

            return {

                "type": "attribute",

                "key": key,

                "attribute": attribute,

                "label": value.get("label", attribute),

                "value": value.get("value")

            }

        # ==========================================
        # Jika value berupa list
        # ==========================================

        if isinstance(value, list):

            return {

                "type": "attribute",

                "key": key,

                "attribute": attribute,

                "label": attribute.replace("_", " ").title(),

                "value": value

            }

        # ==========================================
        # Jika value berupa string/int
        # ==========================================

        return {

            "type": "attribute",

            "key": key,

            "attribute": attribute,

            "label": attribute.replace("_", " ").title(),

            "value": value

        }
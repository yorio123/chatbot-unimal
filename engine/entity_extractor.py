import json
import os
import re


class EntityExtractor:

    def __init__(self):

        path = "knowledge/entities.json"

        if not os.path.exists(path):
            self.entities = {}
            return

        try:

            with open(path, encoding="utf-8") as f:
                self.entities = json.load(f)

        except (json.JSONDecodeError, OSError):

            self.entities = {}

        # ==========================================
        # Mapping Prodi -> Fakultas
        # Digunakan untuk menghindari konflik entity
        # ==========================================

        self.prodi_fakultas = {

            # Fakultas Teknik
            "teknik_informatika": "teknik",
            "teknik_mesin": "teknik",
            "sistem_informasi": "teknik",
            "teknik_elektro": "teknik",
            "teknik_industri": "teknik",
            "teknik_kimia": "teknik",
            "teknik_material": "teknik",
            "teknik_logistik": "teknik",
            "teknik_sipil": "teknik",
            "teknik_arsitektur": "teknik",
            "magister_teknologi_informasi": "teknik",
            "magister_teknik_energi_terbarukan": "teknik",
            "magister_teknik_sipil": "teknik",

            # Fakultas Ekonomi
            "manajemen": "ekonomi",
            "akuntansi": "ekonomi",
            "ekonomi_pembangunan": "ekonomi",
            "ekonomi_syariah": "ekonomi",
            "kewirausahaan": "ekonomi",
            "kesekretariatan": "ekonomi",
            "magister_ilmu_manajemen": "ekonomi",
            "magister_ilmu_akuntansi": "ekonomi",
            "magister_ekonomi_pembangunan": "ekonomi",

            # FISIP
            "sosiologi": "fisip",
            "ilmu_politik": "fisip",
            "ilmu_komunikasi": "fisip",
            "antropologi": "fisip",
            "administrasi_publik": "fisip",
            "administrasi_bisnis": "fisip",
            "magister_administrasi_publik": "fisip",
            "magister_ilmu_komunikasi": "fisip",
            "magister_sosiologi": "fisip",

            # Hukum
            "ilmu_hukum": "hukum",
            "magister_ilmu_hukum": "hukum",
            "doktor_ilmu_hukum": "hukum",

            # Pertanian
            "agroekoteknologi": "pertanian",
            "agribisnis": "pertanian",
            "ilmu_kelautan": "pertanian",
            "akuakultur": "pertanian",
            "magister_agribisnis": "pertanian",
            "magister_agroekoteknologi": "pertanian",

            # FKIP
            "pendidikan_matematika": "fkip",
            "pendidikan_bahasa_indonesia": "fkip",
            "pendidikan_fisika": "fkip",
            "pendidikan_kimia": "fkip",
            "vokasional_teknik_mesin": "fkip",

            # Kedokteran
            "pendidikan_dokter": "kedokteran",
            "profesi_dokter": "kedokteran",
            "keperawatan": "kedokteran",

            # Psikologi
            "psikologi": "kedokteran"

        }

    def extract(
        self,
        text,
        required_entities=None
    ):

        text = text.lower()

        result = {}

        required_entities = (
            required_entities
            or
            self.entities.keys()
        )

        # ==================================================
        # Proses setiap kategori entity
        # ==================================================

        for entity_name in required_entities:

            entity_data = self.entities.get(
                entity_name,
                {}
            )

            found_values = []

            working_text = text

            synonym_list = []

            for entity_value, synonyms in entity_data.items():

                for synonym in synonyms:

                    synonym_list.append(
                        (
                            synonym.lower(),
                            entity_value
                        )
                    )

            synonym_list.sort(
                key=lambda x: len(x[0]),
                reverse=True
            )

            for synonym, entity_value in synonym_list:

                pattern = (
                    r"\b"
                    + re.escape(synonym)
                    + r"\b"
                )

                match = re.search(
                    pattern,
                    working_text
                )

                if match:

                    if entity_value not in found_values:
                        found_values.append(
                            entity_value
                        )

                    start, end = match.span()

                    working_text = (

                        working_text[:start]

                        + " "

                        + working_text[end:]

                    )

            if found_values:

                result[entity_name] = found_values

        # ==================================================
        # POST PROCESSING
        # Hindari konflik Prodi vs Fakultas
        # ==================================================

        if (
            "prodi" in result
            and
            "fakultas" in result
        ):

            prodi = result["prodi"][0]

            fakultas = result["fakultas"][0]

            expected = self.prodi_fakultas.get(prodi)

            if expected == fakultas:

                result.pop("fakultas")

        return result
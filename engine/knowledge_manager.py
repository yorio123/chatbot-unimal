import json
import os


class KnowledgeManager:

    def __init__(self):

        self.base_path = "knowledge"

        self.cache = {}

    def load(self, file_name):

        # Gunakan cache agar file tidak dibaca berulang kali
        if file_name in self.cache:
            return self.cache[file_name]

        path = os.path.join(
            self.base_path,
            f"{file_name}.json"
        )

        if not os.path.exists(path):
            return None

        with open(
            path,
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        self.cache[file_name] = data
import json
import os


class KnowledgeManager:

    def __init__(self):

        self.base_path = "knowledge"

        self.cache = {}

    def load(self, file_name):

        if file_name in self.cache:
            return self.cache[file_name]

        path = os.path.join(
            self.base_path,
            f"{file_name}.json"
        )

        if not os.path.exists(path):
            return None

        with open(
            path,
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        self.cache[file_name] = data

        return data

    def get(self, file_name, key=None):

        data = self.load(file_name)

        if data is None:
            return None

        if key is None:
            return data

        return data.get(key)

    # ==========================================
    # Ambil seluruh isi file knowledge
    # ==========================================

    def get_all(self, file_name):

        return self.load(file_name)
        return data

    def get(self, file_name, key=None):

        data = self.load(file_name)

        if data is None:
            return None

        if key is None:
            return data

        return data.get(key)
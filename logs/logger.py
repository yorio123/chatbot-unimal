import json
import os
from datetime import datetime


class ConversationLogger:

    def __init__(self):

        os.makedirs("logs", exist_ok=True)

        self.file = "logs/conversations.jsonl"

    def log(self, data):

        record = {

            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            **data

        }

        with open(
            self.file,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                )
            )

            f.write("\n")
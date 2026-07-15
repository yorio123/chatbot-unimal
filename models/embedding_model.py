import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel


class EmbeddingModel:

    def __init__(self):

        print("=" * 40)
        print("Memuat Model IndoBERT...")
        print("=" * 40)

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            "indobenchmark/indobert-base-p1"
        )

        self.model = AutoModel.from_pretrained(
            "indobenchmark/indobert-base-p1"
        )

        self.model.to(self.device)
        self.model.eval()

        print("Model berhasil dimuat.\n")

    def mean_pooling(self, model_output, attention_mask):

        token_embeddings = model_output.last_hidden_state

        input_mask_expanded = attention_mask.unsqueeze(-1).expand(
            token_embeddings.size()
        ).float()

        return torch.sum(
            token_embeddings * input_mask_expanded,
            dim=1
        ) / torch.clamp(
            input_mask_expanded.sum(dim=1),
            min=1e-9
        )

    def encode(self, texts):

        if isinstance(texts, str):
            texts = [texts]

        encoded_input = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )

        encoded_input = {
            key: value.to(self.device)
            for key, value in encoded_input.items()
        }

        with torch.no_grad():
            model_output = self.model(**encoded_input)

        sentence_embeddings = self.mean_pooling(
            model_output,
            encoded_input["attention_mask"]
        )

        sentence_embeddings = F.normalize(
            sentence_embeddings,
            p=2,
            dim=1
        )

        return sentence_embeddings.cpu().numpy()
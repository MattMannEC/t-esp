from sentence_transformers import SentenceTransformer
from typing import List
class CustomEmbeddings:
    def __init__(self, model):
        self.model = SentenceTransformer(
            model, trust_remote_code=True, local_files_only=True
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.model.encode(t).tolist() for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]
from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:

    def get_embeddings(self):

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        return embeddings  
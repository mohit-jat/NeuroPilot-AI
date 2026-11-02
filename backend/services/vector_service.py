from langchain_chroma import Chroma


class VectorService:

    def create_vector_store(self, chunks, embeddings):

        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="./vector_db"
        )

        return vector_store
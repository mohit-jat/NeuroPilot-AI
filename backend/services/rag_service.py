
import hashlib

from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from backend.services.document_service import DocumentService
from backend.services.text_splitter import TextSplitterService
from backend.services.embedding_service import EmbeddingService
from backend.services.retriever_service import RetrieverService

from backend.core.llm import get_llm


class RAGService:

    def __init__(self):

        self.document_service = DocumentService()
        self.splitter_service = TextSplitterService()
        self.embedding_service = EmbeddingService()
        self.retriever_service = RetrieverService()

        self.vector_store = None

    # Create or reuse vector database
    def get_vector_store(self):

        if self.vector_store is None:

            embeddings = self.embedding_service.get_embeddings()

            self.vector_store = Chroma(
                collection_name="neuropilot_documents",
                embedding_function=embeddings,
                persist_directory="./vector_db"
            )

        return self.vector_store

    async def ask_document(self, file_path, question):

        # Step 1: Create file hash
        with open(file_path, "rb") as file:
            file_hash = hashlib.sha256(file.read()).hexdigest()

        # Step 2: Load document
        documents = self.document_service.load_document(file_path)

        if not documents:
            return "Unable to read this document."

        # Step 3: Get vector database
        vector_store = self.get_vector_store()

        # Step 4: Check whether document is already stored
        stored_data = vector_store.get(
            where={"file_hash": file_hash}
        )

        # Step 5: Store only if document is new
        if not stored_data["ids"]:

            chunks = self.splitter_service.split_documents(
                documents
            )

            for chunk in chunks:
                chunk.metadata["file_hash"] = file_hash

            vector_store.add_documents(chunks)

        # Step 6: Create retriever
        retriever = vector_store.as_retriever(
            search_kwargs={
                "k": 3,
                "filter": {
                    "file_hash": file_hash
                }
            }
        )

        # Step 7: Search relevant content
        relevant_docs = retriever.invoke(question)

        context = "\n".join(
            [doc.page_content for doc in relevant_docs]
        )

        # Step 8: Get LLM
        llm = get_llm()

        if llm is None:
            return (
                "OpenAI API key is pending. "
                "Relevant document content was retrieved."
            )

        # Step 9: Create prompt
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "Answer using only the following document context:\n{context}"
            ),
            (
                "human",
                "{question}"
            )
        ])

        # Step 10: Create chain
        chain = prompt | llm | StrOutputParser()

        # Step 11: Generate answer
        response = await chain.ainvoke({
            "context": context,
            "question": question
        })

        return response

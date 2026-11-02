from langchain_community.document_loaders import PyPDFLoader, TextLoader


class DocumentService:

    def load_document(self, file_path):

        if file_path.endswith(".pdf"):

            loader = PyPDFLoader(file_path)

        elif file_path.endswith(".txt"):

            loader = TextLoader(file_path, encoding="utf-8")

        else:

            return []

        documents = loader.load()

        return documents

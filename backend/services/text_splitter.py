from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextSplitterService:

    def split_documents(self, documents):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(documents)

        return chunks
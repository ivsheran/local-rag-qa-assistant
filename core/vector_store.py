from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


class VectorStore:
    def __init__(self, config):
        self.collection_name = "rag_knowledge_base"
        self.persist_directory = config.chroma_path
        self.embeddings = OllamaEmbeddings(
            model=config.embedding_model,
            base_url=config.ollama_base_url
        )
        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

    def upsert(self, chunks):
        non_empty = [chunk for chunk in chunks if chunk.page_content.strip()]
        if not non_empty:
            return
        texts = [chunk.page_content for chunk in non_empty]
        metadatas = [chunk.metadata for chunk in non_empty]
        self.vector_store.add_texts(texts=texts, metadatas=metadatas)

    def similarity_search(self, query, top_k):
        return self.vector_store.similarity_search(query, k=top_k)

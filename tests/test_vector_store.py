import unittest
import os
import shutil
from core.config_loader import ConfigLoader
from core.vector_store import VectorStore
from langchain_core.documents import Document

class TestVectorStore(unittest.TestCase):
    def setUp(self):
        self.config = ConfigLoader()
        self.config.chroma_path = "./chroma_db_test"
        self.vector_store = VectorStore(self.config)
    
    def create_dummy_document(self, text):
        return Document(page_content=text, metadata={"file_name": "test.docx"})
    
    def test_upsert_and_similarity_search(self):
        # Create and upsert dummy documents
        doc1 = self.create_dummy_document("This is a test document about Python programming.")
        doc2 = self.create_dummy_document("This document discusses machine learning techniques.")
        self.vector_store.upsert([doc1, doc2])

        # Perform similarity search
        results = self.vector_store.similarity_search("What is Python?", top_k=3)
        self.assertTrue(len(results) > 0)
        self.assertIn("Python programming", results[0].page_content)
    
    def tearDown(self):
        if os.path.exists("./chroma_db_test"):
            shutil.rmtree("./chroma_db_test")

if __name__ == '__main__':
    unittest.main()

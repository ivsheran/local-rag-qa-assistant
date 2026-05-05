import unittest
import os 
from core.config_loader import ConfigLoader
from core.vector_store import VectorStore
from core.rag_chain import RAGChain

class TestRAGChain(unittest.TestCase):
    def setUp(self):
        self.config = ConfigLoader()
        self.vector_store = VectorStore(self.config)
        self.rag_chain = RAGChain(self.config, self.vector_store)

    def test_build_chain(self):
        model=self.config.default_model
        chain = self.rag_chain.build_chain(model)
        self.assertIsNotNone(chain)
        self.assertTrue(hasattr(chain, "invoke"))

if __name__ == '__main__':
    unittest.main()

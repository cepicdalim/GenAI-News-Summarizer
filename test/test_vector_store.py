import unittest
from unittest.mock import MagicMock, patch
from src.lib.logger import Logger
from src.lib.vector_store import VectorStore  # Update with your actual module name


class TestVectorStore(unittest.TestCase):
    def setUp(self):
        self.mock_logger = MagicMock(spec=Logger)
        self.vector_store = VectorStore(logger=self.mock_logger)

    @patch("langchain_community.vectorstores.FAISS.load_local")
    @patch("langchain_huggingface.HuggingFaceEmbeddings")
    def test_search_articles(self, MockEmbeddings, MockFAISS):
        mock_faiss_instance = MagicMock()
        MockFAISS.return_value = mock_faiss_instance

        mock_doc = MagicMock()
        mock_doc.metadata = {
            "title": "Test Title",
            "content": "Test Content",
            "summary": "Test Summary",
            "topics": "Test Topics",
            "url": "http://example.com"
        }
        mock_doc.page_content = "Test Content"
        mock_faiss_instance.similarity_search.return_value = [mock_doc]

        MockFAISS.load_local.return_value = mock_faiss_instance
        self.vector_store.vector_db = mock_faiss_instance  # Assign mock db

        result = self.vector_store.search_articles("test query")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Test Title")
        self.assertEqual(result[0]["content"], "Test Content")
        self.assertEqual(result[0]["summary"], "Test Summary")
        self.assertEqual(result[0]["topics"], "Test Topics")
        self.assertEqual(result[0]["url"], "http://example.com")

        mock_faiss_instance.similarity_search.assert_called_once_with("test query", k=3)

    @patch("langchain_community.vectorstores.FAISS.from_texts")
    @patch("langchain_huggingface.HuggingFaceEmbeddings")
    def test_store_article(self, _, MockFAISS):
        mock_faiss_instance = MagicMock()
        MockFAISS.return_value = mock_faiss_instance
        MockFAISS.from_texts.return_value = mock_faiss_instance

        article = {
            "title": "Sample Title",
            "content": "Sample Content",
            "url": "http://example.com"
        }
        summary = "Sample Summary"
        topics = "Sample Topics"

        self.vector_store.store_article(article, summary, topics)
        mock_faiss_instance.save_local.assert_called_once_with(self.vector_store.db_path)

    @patch("langchain_community.vectorstores.FAISS.add_texts")
    @patch("langchain_huggingface.HuggingFaceEmbeddings")
    def test_upsert_article(self, _, MockFAISS):
        mock_faiss_instance = MagicMock()
        MockFAISS.return_value = mock_faiss_instance
        MockFAISS.add_texts.return_value = mock_faiss_instance
        self.vector_store.vector_db = mock_faiss_instance  # Assign mock db

        article = {
            "title": "Sample Title",
            "content": "Sample Content",
            "url": "http://example.com"
        }
        summary = "Sample Summary"
        topics = "Sample Topics"
        
        self.vector_store.store_article(article, summary, topics)
        mock_faiss_instance.add_texts.assert_called_once()
        mock_faiss_instance.save_local.assert_called_once_with(self.vector_store.db_path)


if __name__ == "__main__":
    unittest.main()

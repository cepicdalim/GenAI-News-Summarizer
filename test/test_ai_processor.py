import unittest
from unittest.mock import MagicMock
from src.lib.ai_processor import AIProcessor

class TestAIProcessor(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock()
        self.processor = AIProcessor(
            api_key="dummy_key",
            azure_endpoint="dummy_endpoint",
            api_version="dummy_version",
            openai_model="dummy_model",
            embedding_model="dummy_embedding",
            logger=self.logger
        )

    def test_summarize_and_extract_topics(self):
        article = {"content": "This is a test article about AI and machine learning."}
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Summary: Test summary\nTopics: AI, Machine Learning"))
        ]
        self.processor.client.chat.completions.create = MagicMock(return_value=mock_response)

        result = self.processor.summarize_and_extract_topics(article)
        self.assertIn("Summary: Test summary", result)
        self.assertIn("Topics: AI, Machine Learning", result)

    def test_get_text_embedding(self):
        mock_response = MagicMock()
        mock_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3])]
        self.processor.client.embeddings.create = MagicMock(return_value=mock_response)

        embeddings = self.processor.get_text_embedding("Test content")
        self.assertEqual(embeddings, [0.1, 0.2, 0.3])

if __name__ == "__main__":
    unittest.main()

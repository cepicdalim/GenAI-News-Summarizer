import unittest
from src.lib.text_processor import TextProcessor

class TestTextProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = TextProcessor()

    def test_preprocess_removes_stopwords_and_punctuation(self):
        article = {
            "url": "http://example.com",
            "title": "Test Article",
            "content": "This is a test article. It contains stopwords and punctuation!"
        }
        result = self.processor.preprocess(article)
        self.assertEqual(result["url"], article["url"])
        self.assertEqual(result["title"], article["title"])
        self.assertEqual(result["content"], "test article contains stopwords punctuation")

    def test_preprocess_handles_empty_content(self):
        article = {
            "url": "http://example.com",
            "title": "Empty Content",
            "content": ""
        }
        result = self.processor.preprocess(article)
        self.assertEqual(result["url"], article["url"])
        self.assertEqual(result["title"], article["title"])
        self.assertEqual(result["content"], "")

    def test_preprocess_handles_non_ascii_characters(self):
        article = {
            "url": "http://example.com",
            "title": "Non-ASCII Content",
            "content": "Café müde! Überprüfung."
        }
        result = self.processor.preprocess(article)
        self.assertEqual(result["url"], article["url"])
        self.assertEqual(result["title"], article["title"])
        self.assertEqual(result["content"], "Café müde Überprüfung")

if __name__ == "__main__":
    unittest.main()
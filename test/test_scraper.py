import unittest
from unittest import mock
from unittest.mock import MagicMock, patch
from src.lib.scraper import NewsScraper

class TestScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = NewsScraper()

    @patch("requests.get")
    def test_fetch_article(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><h1>Test Title</h1><p>Test content</p></body></html>"
        mock_get.return_value = mock_response

        article = self.scraper.fetch_article("http://example.com")
        self.assertEqual(article["content"], "Test content")
        self.assertEqual(article["title"], "Test Title")
        self.assertEqual(article["url"], "http://example.com")
        #called with any header
        mock_get.assert_called_once_with("http://example.com", headers=mock.ANY)

    @patch("requests.get")
    def test_fetch_article_invalid_url(self, mock_get):
        mock_get.side_effect = Exception("Invalid URL")
        with self.assertRaises(Exception) as context:
            self.scraper.fetch_article("invalid-url")
        self.assertEqual(str(context.exception), "Invalid URL")

    @patch("requests.get")
    def test_fetch_article_network_error(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        with self.assertRaises(Exception) as context:
            self.scraper.fetch_article("http://example.com")
        self.assertEqual(str(context.exception), "Network error")

    @patch("requests.get")
    def test_fetch_article_empty_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = ""
        mock_get.return_value = mock_response

        article = self.scraper.fetch_article("http://example.com")
        self.assertEqual(article, {"title": None, "content": '', "url": "http://example.com"})

    @patch("requests.get")
    def test_fetch_article_non_200_status(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_response.raise_for_status.side_effect = Exception("Failed to fetch article: 404")

        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.scraper.fetch_article("http://example.com")
        self.assertEqual(str(context.exception), "Failed to fetch article: 404")

if __name__ == "__main__":
    unittest.main()

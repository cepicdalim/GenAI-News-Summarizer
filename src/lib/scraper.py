import requests
from bs4 import BeautifulSoup
from typing import Dict

class NewsScraper:
    """Fetches news articles from URLs."""
    HEADERS = {"User-Agent": "Mozilla/5.0"}

    def fetch_article(self, url: str) -> Dict[str, str]:
        """Fetches article content from a given URL."""
        response = requests.get(url, headers=self.HEADERS)
        response.raise_for_status()  # Raises exception for bad status codes
        
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text if soup.find('title') else soup.find('h1').text if soup.find('h1') else None

        paragraphs = [p.get_text() for p in soup.find_all(['p', 'span', 'h2', 'h3', 'h4', 'h5', 'h6']) if p.get_text()]
        content = '\n'.join(paragraphs)
        
        return {"url": url, "title": title, "content": content}
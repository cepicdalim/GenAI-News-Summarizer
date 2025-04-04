import spacy
import re
from typing import Dict

class TextProcessor:
    """Preprocesses text using spaCy for LLM-friendly output."""
    def __init__(self, model: str = "en_core_web_sm"):
        self.model = model
        self.nlp = None

    def _load_model(self):
        if self.nlp is None:
            self.nlp = spacy.load(self.model)

    def _clean_raw_text(self, text: str) -> str:
        # Remove emails, URLs, and excess whitespace
        text = re.sub(r"\S+@\S+\.\S+", "", text)  # remove emails
        text = re.sub(r"http\S+|www\S+", "", text)  # remove URLs
        text = re.sub(r"\s+", " ", text)  # normalize whitespace
        return text.strip()

    def preprocess(self, article: Dict[str, str]) -> Dict[str, str]:
        """Cleans and normalizes article content for OpenAI API."""
        self._load_model()
        
        raw_content = self._clean_raw_text(article["content"])
        doc = self.nlp(raw_content)

        # Filter tokens: remove stopwords, punct, and empty tokens
        cleaned_tokens = [
            token.text
            for token in doc
            if not token.is_stop and not token.is_punct and token.text.strip()
        ]
        
        cleaned_content = " ".join(cleaned_tokens)

        return {
            "url": article["url"],
            "title": article["title"],
            "content": cleaned_content
        }

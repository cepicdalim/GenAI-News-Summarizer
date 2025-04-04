from openai import AzureOpenAI
from typing import List, Dict
from lib.logger import Logger

class AIProcessor:
    """Manages AI-based summarization and embeddings."""
    def __init__(self, api_key: str, azure_endpoint: str, api_version: str, 
                 openai_model: str, embedding_model: str, logger: Logger):
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )
        self.openai_model = openai_model
        self.embedding_model = embedding_model
        self.logger = logger

    def summarize_and_extract_topics(self, article: Dict[str, str]) -> str:
        """Generates a summary and extracts topics from the article."""
        prompt = f"""
        Summarize the following article and extract key topics. Format your response exactly as follows:
        
        Summary: <Provide a concise summary of the article in 1-2 sentences>
        Topics: <List 3-5 key topics as a comma-separated list>
        
        Article content:
        {article['content']}
        """
        self.logger.debug("Generating summary and extracting topics...")
        response = self.client.chat.completions.create(
            model=self.openai_model,
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content

    def get_text_embedding(self, text: str) -> List[float]:
        """Generates embeddings for the given text."""
        self.logger.debug("Generating text embedding...")
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        self.logger.debug("Embedding generated.")
        return response.data[0].embedding
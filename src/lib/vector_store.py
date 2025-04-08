import threading
from lib.logger import Logger
from typing import List, Dict
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

class VectorStore:
    """Manages storage and retrieval of articles, summaries, and topics in a FAISS vector database."""
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", db_path: str = "news_vector_db", logger: Logger = None):
        self.db_path = db_path
        self.logger = logger
        self.vector_db = None
        self.model_name = model_name
        self.model_on_ready = threading.Event()
        threading.Thread(target=self.load_models, daemon=True).start()

    def load_models(self):
        self.embedder = HuggingFaceEmbeddings(model_name=self.model_name, cache_folder="./cached_models")
        self.model_on_ready.set()

    def store_article(self, article: Dict[str, str], summary: str, topics: str) -> None:
        self.model_on_ready.wait()  
        """Stores the article, summary, and topics in the vector database with metadata."""
        # Combine all text for embedding (to capture meaning across all fields)
        
        self.logger.debug("Storing article, summary, and topics in vector database...")
        # Create metadata to store separately
        metadata = {
            "url": article["url"],
            "title": article["title"],
            "summary": summary,
            "topics": topics
        }
        self._upsert(article["content"], metadata)

        self.logger.debug("Article, summary, and topics successfully stored in vector database.")

    def search_articles(self, query: str, k: int = 3) -> List[Dict[str, str]]:
        """Searches for articles and returns their content, summary, and topics."""
        self.model_on_ready.wait()  
        if(self.vector_db is None):
            self.vector_db = FAISS.load_local(self.db_path, embeddings=self.embedder, allow_dangerous_deserialization=True)
        
        docs = self.vector_db.similarity_search(query, k=k)
        # Return a list of dictionaries with all metadata
        return [
            {
                "title": doc.metadata["title"],
                "content": doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content,
                "summary": doc.metadata["summary"],
                "topics": doc.metadata["topics"],
                "url": doc.metadata["url"]
            }
            for doc in docs
        ]
    
    def _upsert(self, combined_text: str, metadata: Dict[str, str]) -> None:
        if self.vector_db is None:
            self.vector_db = FAISS.from_texts(
                texts=[combined_text],
                embedding=self.embedder,
                metadatas=[metadata]
            )
        else:
            self.vector_db.add_texts([combined_text], metadatas=[metadata], embedding=self.embedder)
        
        self.vector_db.save_local(self.db_path)
import os
from lib.ai_processor import AIProcessor
from lib.vector_store import VectorStore
from lib.app import NewsApp
from lib.logger import Logger
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

    # Load environment variables
    api_key = os.getenv("API_KEY")
    azure_endpoint = os.getenv("AZURE_ENDPOINT")
    api_version = os.getenv("API_VERSION")
    openai_model = os.getenv("OPENAI_MODEL")
    embedding_model = os.getenv("EMBEDDING_MODEL")
    db_path = os.getenv("DB_PATH")

    if not all([api_key, azure_endpoint, api_version, openai_model, embedding_model, db_path]):
        raise ValueError("Please set all required environment variables.")

    # Initialize components
    logger = Logger()
    ai_processor = AIProcessor(api_key, azure_endpoint, api_version, openai_model, embedding_model, logger)
    vector_store = VectorStore(model_name="all-MiniLM-L6-v2", db_path=db_path, logger=logger)
    app = NewsApp(ai_processor, vector_store, logger)

    # Run the app
    app.run()
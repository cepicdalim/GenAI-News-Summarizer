from lib.logger import Logger
from lib.scraper import NewsScraper
from lib.text_processor import TextProcessor
from lib.ai_processor import AIProcessor
from lib.vector_store import VectorStore

class NewsApp:
    """Main application for scraping, processing, and searching news articles."""
    def __init__(self, ai_processor: AIProcessor, vector_store: VectorStore, logger: Logger):
        self.scraper = NewsScraper()
        self.text_processor = TextProcessor()
        self.ai_processor = ai_processor
        self.vector_store = vector_store
        self.logger = logger

    def run(self) -> None:
        """Runs the application with user interaction."""
        self.logger.info("Welcome to AI-Powered News Analyzer!")
        
        while True:
            self.logger.info("1. Scrape and analyze article(s)")
            self.logger.info("3. Search for articles in the database")
            
            choice = input("Choose an option (1/2) or 'q' to quit: ").strip()
            if choice  == "q":
                self.logger.info("Exiting the application.")
                return
            elif choice == "1":
                self._scrape_and_analyze()
            elif choice == "2":
                self._search_articles()
            else:
                self.logger.error("Invalid choice. Please try again.")

    def _scrape_and_analyze(self) -> None:
        """Scrapes an article, processes it, generates summary/topics, and stores it."""
        urls = self._get_urls()

        if not urls:
            self.logger.error("No valid URLs provided.")
            return
        
        for url in urls:
            try:
                self.logger.debug(f"\nFetching article from {url}...")
                # Scrape the article
                article = self.scraper.fetch_article(url)
                cleaned_article = self.text_processor.preprocess(article)
                
                # Generate summary and topics
                summary_and_topics = self.ai_processor.summarize_and_extract_topics(cleaned_article)
                # Assuming the response is a string with summary and topics separated (adjust parsing as needed)
                summary, topics = self._parse_summary_and_topics(summary_and_topics)
                
                self.logger.debug(f"Summary: {summary}")
                self.logger.debug(f"Topics: {topics}")
                
                self.logger.debug("\nSaving article to vector database...")
                self.vector_store.store_article(article, summary, topics)
                self.logger.debug("Article successfully saved!")
            except Exception as e:
                self.logger.error(f"Error: {e}")

    def _search_articles(self) -> None:
        """Searches for articles based on a user query."""
        query = input("Enter a search query: ").strip()
        self.logger.debug("\nSearching articles...")
        results = self.vector_store.search_articles(query, 1)
        if not results or len(results) == 0:
            self.logger.error("No articles found.")
        
        result = results[0]
        self.logger._log(f"Title: {result['title']}", "green")
        self.logger._log(f"URL: {result['url']}", "magenta")
        self.logger._log(f"Topics: {result['topics']}", "blue")
        self.logger.add_seperator()
        self.logger._log(f"Content:\n {result['content']}", "white")
        self.logger.add_seperator()
        self.logger._log(f"Summary:\n {result['summary']}", "yellow")

    def _parse_summary_and_topics(self, text: str) -> tuple[str, str]:
        """Parses the summary and topics from the AI response."""
        # Adjust this based on the actual format of your AI response
        # Assuming it’s something like "Summary: <text>\nTopics: <text>"
        lines = text.split("\n")
        summary = next((line.split(": ", 1)[1] for line in lines if line.startswith("Summary:")), "No summary")
        topics = next((line.split(": ", 1)[1] for line in lines if line.startswith("Topics:")), "No topics")
        return summary, topics
    
    def _get_urls(self) -> list[str]:
        url_str = input("Enter the URL of the article (or multiple URLs separated by commas): ").split(",")
        urls = [url.strip() for url in url_str]

        for url in urls:
            if not url.startswith("http") and not url.startswith("https"):
                self.logger.error(f"Invalid URL: {url}. Please enter a valid URL.")
                return []
        if not urls:
            self.logger.error("URL cannot be empty.")
            return []
        return urls
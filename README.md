# GenAI News Summarizer

## Overview

This project is a Python-based application that utilizes Generative AI (GenAI) to extract news articles from provided URLs, generate summaries, and identify topics. The application leverages the OpenAI API for text generation and the Spacy library for natural language processing tasks.

## Project Structure

```
GenAI-News-Summarizer/
├── src/
│   ├── main.py
│   ├── (.env) <-- put your environment variables here
│   ├── /lib/
│   │   ├── __init__.py
│   │   ├── ai_processor.py
│   │   ├── app.py
│   │   ├── logger.py
│   │   ├── scraper.py
│   │   ├── text_processor.py
│   │   └── vector_store.py
└── /tests/
│   ├── test_ai_processor.py
│   ├── test_app.py
│   ├── test_logger.py
│   ├── test_scraper.py
│   ├── test_text_processor.py
│   └── test_vector_store.py
├── requirements.txt
├── README.md
├── Dockerfile
├── .dockerignore
└── .gitignore
```

## Prerequisites

- Python 3.8.0 or higher _(3.12.0 recommended)_
- Spacy Model
- OpenAI API key

## Installation

### Clone the repository

### Install dependencies

```bash
pip install -r requirements.txt
```

### Download Spacy model

```bash
python -m spacy download en_core_web_sm
```

# Running the Application

## Set Environment Variables

Set the following environment variables in your terminal or IDE in your `.env` file inside of `src/` directory:

### /src/.env

```bash
AZURE_ENDPOINT=<your_azure_endpoint> (https://<your_azure_endpoint>.openai.azure.com/)
API_VERSION=<your_api_version> (ex. '2024-02-01')
API_KEY=<your_openai_api_key>
OPENAI_MODEL=<your_model> (ex. 'gpt-4o-mini-2024-07-18')
EMBEDDING_MODEL=<your_embedding_model> (ex. 'text-embedding-3-small-1')
DB_PATH=<your_db_path> (news_vector_db)
```

## Run

### CLI

```bash
python src/main.py
```

### Docker

```bash
docker build -t genai-news-summarizer .
docker run -it genai-news-summarizer
```

#### Hints

- To reduce startup time, you can run the application once to download the Spacy model and tokenizer model before building the Docker image. Docker image will include "cached_models" folder to avoid downloading the models again.

# Tests

This project includes unit tests for each module to ensure the functionality of the application. The tests are located in the `tests` directory and can be run using the `unittest` framework.

## Run All Tests

To run all tests, navigate to the root directory of the project and execute the following command:

```bash
PYTHONPATH=src python -m unittest
```

## Run Specific Test

To run a specific test, navigate to the `tests` directory and execute the following command:

```bash
PYTHONPATH=src python -m unittest test_<module_name>.py
```

## Workflows

<div style="display: flex; justify-content: space-around; align-items: baseline;">
  <div style="text-align: center;">
    <p><strong>Scraping Workflow</strong></p>
    <img src="images/scraping-workflow.svg" alt="Scraping Workflow" style="width: 80%; border: 1px solid #ddd; border-radius: 8px; padding: 5px;">
  </div>
  <div style="text-align: center;">
    <p><strong>Search Workflow</strong></p>
    <img src="images/search-workflow.svg" alt="Search Workflow" style="width: 80%; border: 1px solid #ddd; border-radius: 8px; padding: 5px;">
  </div>
</div>

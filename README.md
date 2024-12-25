# Daily Job Digest

An automated job scraping tool that collects and filters job postings from multiple sources including Indeed and Hacker News.

## Features

- Multi-source job scraping (Indeed, Hacker News)
- Configurable job filters
- Asynchronous operation
- Database storage for job listings

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the root directory with:
   ```
   GOOGLE_API_KEY=your_google_api_key
   CSE_ID=your_custom_search_engine_id
   ```

2. Configure scrapers in `config.py`:
   ```python
   SCRAPERS = [
       {
           "type": "indeed",
           "search_term": "python developer",
           "location": "New York",
           "country": "us",
           "prompts": ["remote", "python", "aws"]
       },
       {
           "type": "hackernews",
           "prompts": ["remote", "startup", "senior"]
       }
   ]
   ```

## Usage

Run the scraper:

```bash
python -m job_scraper.main
```

## Sources

- Indeed Jobs
- Hacker News "Who is hiring?" threads

## Requirements

- Python 3.7+
- Google Custom Search API credentials (for Hacker News scraping)
- Database (SQLite by default)

## License

MIT
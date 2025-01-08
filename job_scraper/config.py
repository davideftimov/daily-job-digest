import os

# LLM Configuration
LLM_CONFIG = {
    "model": "gemini-2.0-flash-exp",
    "api_key": os.environ.get("GEMINI_API_KEY"),
    "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/"
}

# Blocked companies - add companies you want to exclude
BLOCKED_COMPANIES = [
    "Company Name 1",
    "Company Name 2"
]

# Define your prompts
PROMPTS = {
    "language": {
        "text": """Given the job offer your task is to check if the offer fulfills the following criterium:
                  -The job offer is written in English
                  Respond only with 'YES' or 'NO'.""",
        "required": True
    },
    "experience": {
        "text": """Given the job offer your task is to check if the offer fulfills the following criterium:
                  -The job is for entry to mid level candidates
                  Respond only with 'YES' or 'NO'.""",
        "required": False
    }
}

# Scraper configurations
SCRAPERS = [
    {
        "type": "linkedin",
        "search_term": "software engineer -senior -internship",
        "location": "City, Country",
        "prompts": ["language", "experience"]
    },
    {
        "type": "indeed",
        "search_term": "software engineer -senior -internship",
        "location": "City, Country",
        "country": "Country",
        "prompts": ["language", "experience"]
    },
    {
        "type": "hackernews",
        "prompts": ["experience"]
    },
]
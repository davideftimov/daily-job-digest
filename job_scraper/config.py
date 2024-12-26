import os

# LLM Configuration
LLM_CONFIG = {
    "model": "gemini-2.0-flash-exp",
    "api_key": os.environ.get("GEMINI_API_KEY"),
    "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/"
}

# Define your prompts
PROMPTS = {
    "location": {
        "text": """Given the job offer your task is to check if the offer fulfills the following criterium:
                  -The job is REMOTE(Global or in an European country), Hybrid(in an European country) or On-site(in an European country)
                  Respond only with 'YES' or 'NO'.""",
        "required": True
    },
    "language": {
        "text": """Given the job offer your task is to check if the offer fulfills the following criterium:
                  -The job offer is written in English
                  Respond only with 'YES' or 'NO'.""",
        "required": True
    },
    "job_type": {
        "text": """Given the job offer your task is to check if the offer fulfills the following criterium:
                  -The job offer is for a software developer (engineer) position
                  Respond only with 'YES' or 'NO'.""",
        "required": False
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
        "type": "indeed",
        "search_term": "software engineer -senior -internship",
        "location": "Berlin, Germany",
        "country": "Germany",
        "prompts": ["language", "job_type", "experience"]
    },
    {
        "type": "indeed",
        "search_term": "software engineer -senior -internship",
        "location": "Amsterdam, Netherlands",
        "country": "Netherlands",
        "prompts": ["language", "job_type", "experience"]
    },
    {
        "type": "indeed",
        "search_term": "ingénieur logiciel -senior -stage",
        "location": "Paris, France",
        "country": "France",
        "prompts": ["job_type", "experience"]
    },
    {
        "type": "indeed",
        "search_term": "ingénieur logiciel -senior -stage",
        "location": "Nice, France",
        "country": "France",
        "prompts": ["job_type", "experience"]
    },
    {
        "type": "indeed",
        "search_term": "software engineer -senior -internship",
        "location": "Geneva, Switzerland",
        "country": "Switzerland",
        "prompts": ["job_type", "experience"]
    },
    # {
    #     "type": "hackernews",
    #     "prompts": ["location", "language", "job_type", "experience"]
    # }
]
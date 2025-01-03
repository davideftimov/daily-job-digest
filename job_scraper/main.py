import asyncio
import os
from dotenv import load_dotenv
from .config import SCRAPERS

from .database_manager import DatabaseManager
from .job_filter import JobFilter
from job_scraper.scrapers.hn_scraper import HackerNewsJobScraper
from job_scraper.scrapers.indeed_scraper import IndeedScraper

class JobScraperOrchestrator:
    def __init__(self):
        load_dotenv()
        self.db_manager = DatabaseManager()
        self.job_filter = JobFilter()
        self.scrapers = []
        
        for config in SCRAPERS:
            prompts = config["prompts"]
            filter_instance = JobFilter(prompts)
            
            if config["type"] == "indeed":
                self.scrapers.append(
                    IndeedScraper(
                        db_manager=self.db_manager,
                        job_filter=filter_instance,
                        filter_id=id(prompts),
                        search_term=config["search_term"],
                        location=config["location"],
                        country=config["country"]
                    )
                )
            elif config["type"] == "hackernews":
                self.scrapers.append(
                    HackerNewsJobScraper(
                        google_api_key=os.getenv('GOOGLE_API_KEY'),
                        cse_id=os.getenv('CSE_ID'),
                        db_manager=self.db_manager,
                        job_filter=filter_instance,
                        filter_id=id(prompts)
                    )
                )

    async def run(self):
        for scraper in self.scrapers:
            await scraper.run()

if __name__ == "__main__":
    orchestrator = JobScraperOrchestrator()
    asyncio.run(orchestrator.run())
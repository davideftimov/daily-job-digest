import asyncio
import os
from dotenv import load_dotenv

from .database_manager import DatabaseManager
from .job_filter import JobFilter
from job_scraper.scrapers.hn_scraper import HackerNewsJobScraper
from job_scraper.scrapers.indeed_scraper import IndeedScraper

class JobScraperOrchestrator:
    def __init__(self):
        load_dotenv()
        self.db_manager = DatabaseManager()
        self.job_filter = JobFilter()
        self.scrapers = [
            HackerNewsJobScraper(
                google_api_key=os.getenv('GOOGLE_API_KEY'),
                cse_id=os.getenv('CSE_ID'),
                db_manager=self.db_manager,
                job_filter=self.job_filter
            ),
            IndeedScraper(
                db_manager=self.db_manager,
                job_filter=self.job_filter,
                search_term='software engineer -senior',
                location='Berlin, Germany',
                country='Germany'
            ),
            IndeedScraper(
                db_manager=self.db_manager,
                job_filter=self.job_filter,
                search_term='software engineer -senior',
                location='Amsterdam, Netherlands',
                country='Netherlands'
            ),
            IndeedScraper(
                db_manager=self.db_manager,
                job_filter=self.job_filter,
                search_term='software engineer -senior',
                location='Geneva, Switzerland',
                country='Switzerland'
            ),
            IndeedScraper(
                db_manager=self.db_manager,
                job_filter=self.job_filter,
                search_term='ingénieur logiciel -senior',
                location='Paris, France',
                country='France'
            ),
            IndeedScraper(
                db_manager=self.db_manager,
                job_filter=self.job_filter,
                search_term='ingénieur logiciel -senior',
                location='Nice, France',
                country='France'
            ),
        ]

    async def run(self):
        for scraper in self.scrapers:
            await scraper.run()

if __name__ == "__main__":
    orchestrator = JobScraperOrchestrator()
    asyncio.run(orchestrator.run())
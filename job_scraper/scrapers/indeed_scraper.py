from typing import List, Dict, Any
import pandas as pd
from jobspy import scrape_jobs
from job_scraper.scrapers.base_scraper import JobScraper
from job_scraper.database_manager import DatabaseManager
from job_scraper.job_filter import JobFilter

class IndeedScraper(JobScraper):
    def __init__(self, db_manager: DatabaseManager, job_filter: JobFilter, search_term: str, location: str, country: str):
        self.db_manager = db_manager
        self.job_filter = job_filter
        self.search_term = search_term
        self.location = location
        self.country = country
        self.source = "indeed"
        
    async def fetch_jobs(self) -> pd.DataFrame:
        jobs = scrape_jobs(
            site_name=["indeed"],
            search_term=self.search_term,
            location=self.location,
            results_wanted=40,
            hours_old=58,
            country_indeed=self.country,
            # description_format='html',
        )
        print(f"Found {len(jobs)} jobs on Indeed for location: {self.location}")
        return jobs

    async def process_jobs(self, jobs: pd.DataFrame):
        
        for _, job in jobs.iterrows():
            job_id = hash(job['job_url'])  # Create a unique ID from the URL
            description = job.get('description', '')
            filter_result = self.job_filter.filter_job(description, language_filter=True)

            self.db_manager.save_comment(
                job_id,
                int(pd.Timestamp(job.get('date_posted')).timestamp()),
                description,
                filter_result,
                self.source,
                job['job_url'],
                title=job.get('title', None),
                location=job.get('location', None),
            )

    async def run(self):
        try:
            jobs = await self.fetch_jobs()
            if not jobs.empty:
                await self.process_jobs(jobs)
        except Exception as e:
            print(f"Error in Indeed scraper: {e}")
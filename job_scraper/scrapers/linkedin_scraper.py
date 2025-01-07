from typing import List, Dict, Any
import pandas as pd
from jobspy import scrape_jobs
from job_scraper.scrapers.base_scraper import JobScraper
from job_scraper.database_manager import DatabaseManager, Job
from job_scraper.job_filter import JobFilter
from datetime import datetime

class LinkedinScraper(JobScraper):
    def __init__(self, db_manager: DatabaseManager, job_filter: JobFilter, filter_id: int, search_term: str, location: str, language_filter: bool = True):
        self.db_manager = db_manager
        self.job_filter = job_filter
        self.filter_id = filter_id
        self.search_term = search_term
        self.location = location
        self.source = "linkedin"
        self.language_filter = language_filter
        
    async def fetch_jobs(self) -> pd.DataFrame:
        jobs = scrape_jobs(
            site_name=["linkedin"],
            search_term=self.search_term,
            location=self.location,
            results_wanted=100,
            hours_old=24,
            linkedin_fetch_description=True,
        )
        print(f"Found {len(jobs)} jobs on Linkedin for location: {self.location}")
        return jobs

    async def process_jobs(self, jobs: pd.DataFrame):
        for _, job in jobs.iterrows():
            description = job.get('description', 'what')
            
            filter_result = self.job_filter.filter_job(description, self.filter_id)

            time_posted = job.get('date_posted')
            if not time_posted or pd.isna(time_posted):
                time = int(datetime.now().timestamp())
            else:
                time=int(pd.Timestamp(time_posted, tz='UTC').timestamp())

            job = Job(
                id=job['id'], 
                time=time,
                time_scraped=int(datetime.now().timestamp()),
                text=description, 
                filter=filter_result, 
                source=self.source, 
                url=job.get('job_url', None), 
                title=job.get('title', None), 
                location=job.get('location', None),
                company=job.get('company', None))
            
            self.db_manager.save_job(job)

    async def run(self):
        try:
            jobs = await self.fetch_jobs()
            if not jobs.empty:
                await self.process_jobs(jobs)
        except Exception as e:
            print(f"Error in Linkedin scraper: {e}")
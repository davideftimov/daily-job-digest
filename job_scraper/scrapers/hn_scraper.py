import httpx
import re
from datetime import datetime, timedelta
import pytz
import calendar
from typing import Optional, List, Dict

from job_scraper.scrapers.base_scraper import JobScraper
from job_scraper.database_manager import DatabaseManager, Job
from job_scraper.job_filter import JobFilter

class HackerNewsJobScraper(JobScraper):
    def __init__(self, google_api_key: str, cse_id: str, db_manager: DatabaseManager, job_filter: JobFilter, filter_id: int):
        self.google_api_key = google_api_key
        self.cse_id = cse_id
        self.db_manager = db_manager
        self.job_filter = job_filter
        self.filter_id = filter_id
        self.source = "hackernews"

    def get_who_is_hiring_query(self) -> str:
        # Set timezone to Eastern Time
        eastern = pytz.timezone('US/Eastern')
        now = datetime.now(eastern)

        # Find the first weekday of the current month
        first_day = datetime(now.year, now.month, 1, tzinfo=eastern)
        first_weekday = first_day
        while first_weekday.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            first_weekday += timedelta(days=1)
        
        # Set time to 11 AM
        first_weekday_11am = first_weekday.replace(hour=11, minute=0, second=0, microsecond=0)

        # Determine if the current time is after the posting time
        if now >= first_weekday_11am:
            target_month = now.month
            target_year = now.year
        else:
            if now.month == 1:
                target_month = 12
                target_year = now.year - 1
            else:
                target_month = now.month - 1
                target_year = now.year

        month_name = calendar.month_name[target_month]
        return f'Ask HN: Who is Hiring? "{month_name} {target_year}"'

    async def google_search(self, query: str) -> List[Dict]:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "key": self.google_api_key,
            "cx": self.cse_id,
            "num": 1
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            return response.json().get('items', []) if response.status_code == 200 else []

    async def fetch_latest_who_is_hiring(self) -> Optional[int]:
        query = self.get_who_is_hiring_query()
        print(f"Searching for: {query}")
        search_results = await self.google_search(query)
        print(search_results)
        
        if search_results:
            url = search_results[0].get('link')
            if url:
                match = re.search(r"item\?id=(\d+)", url)
                return int(match.group(1)) if match else None
        return None

    async def fetch_item_data(self, item_id: int) -> Dict:
        url = f'https://hacker-news.firebaseio.com/v0/item/{item_id}.json'
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    async def fetch_jobs(self, post_id: int):
        post_data = await self.fetch_item_data(post_id)

        if post_data.get("kids"):
            return post_data["kids"]
        return []

    async def process_jobs(self, jobs: List[int]):
        max_id = self.db_manager.get_max_hn_id()

        for kid_id in jobs:
            if kid_id > max_id:
                kid_data = await self.fetch_item_data(kid_id)
                if 'text' in kid_data:
                    text = kid_data.get('text', 'No text available')
                    if self.is_company_blocked(text):
                        continue
                        
                    filter_result = self.job_filter.filter_job(text, self.filter_id)
                    self.db_manager.save_job(Job(
                        id = f"hn-{kid_id}",
                        time = kid_data['time'],
                        time_scraped = int(datetime.now().timestamp()),
                        text = kid_data.get('text', 'No text available'),
                        filter = filter_result,
                        source = self.source,
                        url = "https://news.ycombinator.com/item?id=" + str(kid_id),
                        hn_id = kid_id,
                    ))

    async def run(self):
        try:
            post_id = await self.fetch_latest_who_is_hiring()
            if post_id:
                jobs = await self.fetch_jobs(post_id)
                if jobs:
                    await self.process_jobs(jobs)
        except Exception as e:
            print(f"Error in HackerNews scraper: {e}")
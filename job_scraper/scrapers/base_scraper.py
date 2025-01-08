from abc import ABC, abstractmethod
from typing import Any, List

class JobScraper(ABC):
    def is_company_blocked(self, company: str) -> bool:
        """Check if company is in blocked list"""
        from job_scraper.config import BLOCKED_COMPANIES
        if not company:
            return False
        return any(blocked.lower() in company.lower() for blocked in BLOCKED_COMPANIES)

    @abstractmethod
    async def fetch_jobs(self) -> List[Any]:
        """Fetch jobs from the source"""
        pass

    @abstractmethod
    async def process_jobs(self, jobs: List[Any]):
        """Process and store the fetched jobs"""
        pass

    @abstractmethod
    async def run(self):
        """Main method to run the scraper"""
        pass
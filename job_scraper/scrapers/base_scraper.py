from abc import ABC, abstractmethod
from typing import Any, List

class JobScraper(ABC):
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
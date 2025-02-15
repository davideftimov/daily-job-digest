from typing import List, Tuple, Dict, Optional
from openai import OpenAI
from .config import LLM_CONFIG, PROMPTS
import time
from collections import deque
from datetime import datetime, timedelta
import logging

class JobFilter:
    _instance: Optional['JobFilter'] = None
    _initialized: bool = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, prompt_names: Optional[List[str]] = None):
        if not self._initialized:
            self.client = OpenAI(
                api_key=LLM_CONFIG["api_key"],
                base_url=LLM_CONFIG["base_url"]
            )
            self.prompts_by_scraper: Dict[str, List[tuple]] = {}
            self.requests_timestamps = deque(maxlen=15)
            self.rate_limit = 15
            self.time_window = 61
            self.logger = logging.getLogger("job_scraper.filter")
            self._initialized = True
            
        if prompt_names is not None:
            scraper_id = id(prompt_names)  # Use the list's id as a unique identifier
            self.prompts_by_scraper[scraper_id] = [
                (name, PROMPTS[name]["text"], PROMPTS[name]["required"]) 
                for name in prompt_names if name in PROMPTS
            ]
            
    def get_prompts(self, scraper_id: int) -> List[tuple]:
        return self.prompts_by_scraper.get(scraper_id, [])

    def _wait_for_rate_limit(self):
        now = datetime.now()
        if len(self.requests_timestamps) >= self.rate_limit:
            oldest_request = self.requests_timestamps[0]
            time_since_oldest = (now - oldest_request).total_seconds()
            
            if time_since_oldest < self.time_window:
                sleep_time = self.time_window - time_since_oldest
                time.sleep(sleep_time)
                self.requests_timestamps.popleft()

        self.requests_timestamps.append(now)

    def _retry_with_backoff(self, operation, max_retries=50, delay=5):
        """Execute operation with exponential backoff retry strategy."""
        total_delay = 0
        
        for attempt in range(max_retries):
            try:
                return operation()
            except Exception as e:
                if not hasattr(e, 'status_code') or e.status_code not in [429, 500]:
                    raise e
                
                self.logger.warning(
                    f"Attempt {attempt + 1}/{max_retries}: "
                    f"Received error {e.status_code}, retrying in {delay} seconds..."
                )
                
                time.sleep(delay)
                total_delay += delay
                delay *= 2
        
        raise Exception(f"Failed after {max_retries} attempts")

    def _check_criteria(self, prompt: str, comment_text: str) -> bool:
        try:
            def make_request():
                self._wait_for_rate_limit()
                completion = self.client.chat.completions.create(
                    model=LLM_CONFIG["model"],
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": comment_text}
                    ],
                )
                return 'yes' in completion.choices[0].message.content.lower()

            return self._retry_with_backoff(make_request)
            
        except Exception as e:
            self.logger.error(f"Error in criteria check: {e}", exc_info=True)
            return False

    def filter_job(self, comment_text: str, scraper_id: int) -> bool:
        try:
            prompts = self.get_prompts(scraper_id)
            for prompt_name, prompt_text, required in prompts:
                result = self._check_criteria(prompt_text, comment_text)
                self.logger.debug(f"{prompt_name}: {result}")
                
                if not result:
                    return False
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing comment: {e}", exc_info=True)
            return False
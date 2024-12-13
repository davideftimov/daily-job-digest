from openai import OpenAI
from .config import MODEL_NAME, PROMPT_LOC, PROMPT_EXP

class JobFilter:
    def __init__(self):
        self.client = OpenAI()

    def filter_job(self, comment_text: str, location_filter: bool = False) -> bool:
        try:
            response = True
            if location_filter:
                completion_loc = self.client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": PROMPT_LOC},
                        {"role": "user", "content": comment_text}
                    ],
                )
                response = response and 'yes' in completion_loc.choices[0].message.content.lower()
                print(f"Location: {response}")
            
            completion_exp = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": PROMPT_EXP},
                    {"role": "user", "content": comment_text}
                ],
            )
            
            response = response and 'yes' in completion_exp.choices[0].message.content.lower()
            print(f"Experience: {response}")
            return response
        except Exception as e:
            print(f"Error processing comment: {e}")
            return False
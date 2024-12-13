# config.py
MODEL_NAME = "gpt-4o-mini"

PROMPT_LOC = """Given the job offer your task is to check if the offer fulfills the following criterium:
-The job is REMOTE(Global or in an European country), Hybrid(in an European country) or On-site(in an European country)

Respond only with 'YES' or 'NO'."""

PROMPT_EXP = """Given the job offer your task is to check if the offer fulfills the following criterium:
-The job is for entry to mid level candidates

Respond only with 'YES' or 'NO'."""
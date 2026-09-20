import asyncio

from celery import Celery

from agent import argus_agent
from load import load_user_prompt

app = Celery("argus", broker="redis://localhost:6379/0")


@app.task
def run_agent(urls: list[str], user_prompt: str = ""):
    if not user_prompt:
        user_prompt = load_user_prompt()

    asyncio.run(argus_agent(urls, user_prompt))

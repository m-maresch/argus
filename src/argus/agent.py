import logging

from dotenv import load_dotenv

from browse import browse
from extract import extract
from telegram import send_telegram_message

load_dotenv()


async def argus_agent(urls, user_prompt):
    logging.info(f"Running argus agent with urls='{urls}', user_prompt='{user_prompt}'")
    for url in urls:
        result = await browse(url, user_prompt)
        logging.info(f"Result: {result}")

        if result:
            extracted = extract(user_prompt, result)
            logging.info(f"Extracted: {extracted}")

            send_telegram_message(result)

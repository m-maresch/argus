# Argus

An autonomous webpage monitoring agent.

## Overview

Argus is an intelligent web scraping and data extraction system that leverages an autonomous browsing agent and LLM-powered data extraction to collect structured information (records) from websites. It processes URLs asynchronously via a distributed task queue, stores results in Redis, and notifies users via Telegram.

## Features

- **Autonomous Web Browsing**: Agent navigates websites based on natural language instructions
- **Intelligent Data Extraction**: LLM-driven extraction of records
- **Dynamic Schema**: Infers data fields from user prompts (no predefined schemas needed)
- **Async Task Queue**: Celery-based distributed task processing
- **Retrieval**: Redis-backed data store for record retrieval
- **Telegram Notifications**: Real-time results delivered via Telegram
- **Safety First**: Read-only mode, CAPTCHA detection, and anti-bot protection

## Architecture

```
User (submit.sh)
         ↓
   Redis Broker
  (Celery Queue)
         ↓
   Worker Process
         ↓
      agent
         ↓
      browse ──→ Browser Agent ──→ Web Content
         ↓                            ↓
      extract ──→ Gemini AI ──→ Structured Data
         ↓                            ↓
      upsert ──→ Redis Storage ─────→ Records
         ↓
      Telegram ─────────────────────→ Notification
```

## Prerequisites

- Python 3.14+
- Docker
- Google Generative AI API key
- Telegram Bot token and chat ID (optional, for notifications)

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/m-maresch/argus
cd argus
```

2. **Create a virtual environment**:
```bash
python -m venv .
source bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Start Redis** (using Docker):
```bash
docker-compose up -d
```

## Configuration

Create a `.env` file in the project root:

```env
# Google Generative AI
GOOGLE_API_KEY=your_google_api_key_here

# Telegram (optional)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

## Usage

### 1. Start the Worker

```bash
./start-argus.sh
```

This starts the Celery worker that processes queued tasks. This should run continuously on your server.

### 2. Define Your Prompt

Copy the prompt template to `prompt.md`, then update `prompt.md` with the instructions for your data collection:

```bash
cp prompt-template.md prompt.md
```

For example:

```markdown
1. Search for rental apartments in: Brooklyn, NY with rent under $3000
2. Collect the title, price, bedrooms, bathrooms, and location of up to 5 apartments matching the criteria. If no matching apartments are found, then stop here.
3. Based on the collected apartments, extract 1 record per apartment consisting of title, price, bedrooms, bathrooms, and location
```

### 3. Submit URLs for Scraping

```bash
./submit.sh "https://example-rental-listings.com/brooklyn"
```

This queues the URL for processing by the worker.

### 4. Retrieve Results

```bash
./list-records.sh "https://example-rental-listings.com/brooklyn"
```

Example output:
```json
{
  "apt_001": {
    "id": "apt_001",
    "title": "Modern 2BR in Williamsburg",
    "price": "$2,500/month",
    "bedrooms": "2",
    "bathrooms": "1.5",
    "location": "Williamsburg, Brooklyn"
  },
  "apt_002": {
    "id": "apt_002",
    "title": "Spacious 3BR Loft",
    "price": "$2,950/month",
    "bedrooms": "3",
    "bathrooms": "2",
    "location": "Park Slope, Brooklyn"
  }
}
```

## Deployment

Argus is designed to run on a server with scheduled job submissions via cron. Once deployed, the workflow is:

1. **Schedule `submit.sh`** with cron to periodically submit URLs for scraping
2. **Worker runs continuously** listening for jobs on the queue
3. **Get results** via Telegram notifications or by querying with `list-records.sh`

## How It Works

1. **User submits URL** via `submit.sh` → Celery enqueues task
2. **Worker picks up task**
3. **Agent executes**:
   - **Browse**: Autonomous agent navigates the URL using natural language prompt
   - **Extract**: LLM parses browser results and extracts records
   - **Store**: Extracted records are saved to Redis with URL-based keys. Records are identified by their `id` field; IDs no longer present in a later result are removed.
   - **Notify**: Telegram is notified only when the set of record IDs for a URL changes. Changes to other fields on an existing record do not trigger a notification.
4. **User can retrieve data** via `list-records.sh`

### Change Detection

Argus compares the IDs of the newly extracted records with the IDs already stored for the URL:

- A newly discovered ID triggers a Telegram notification.
- A previously stored ID that disappears triggers a Telegram notification and is removed from Redis.
- Changes to fields such as price, title, or location do not trigger a Telegram notification.

## Safety & Compliance

- **Read-Only Mode**: Strictly prevents form submissions, account creation, or modifications
- **Scope Containment**: Agent stays on target domain only
- **Security**: Handles CAPTCHAs, login walls, and anti-bot measures gracefully
- **Cookie Management**: Automatically handles cookie banners

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google Generative AI API key | Yes |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token for notifications | No |
| `TELEGRAM_CHAT_ID` | Telegram chat ID for notifications | No |

## License

This project is licensed under the MIT License. See the `LICENSE.txt` file for details. Third-party library notices are documented in `THIRD-PARTY-NOTICES.txt`.

## Acknowledgments

This project was developed with the assistance of Google Gemini 3 and GitHub Copilot.

## Dependencies

Thanks to everyone contributing to any of the following projects:

- browser-use
- langchain
- langchain-google-genai
- Celery
- redis-py
- python-dotenv
- Pydantic
- Requests

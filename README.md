# AI News Assistant

AI News Assistant is a backend application built with FastAPI and LangGraph that allows users to interact with an AI assistant through a Telegram bot. The assistant can create and manage articles using tool calling and store them in a PostgreSQL database.

## Features

* AI-powered article generation
* Telegram bot interface
* Tool calling with LangGraph
* Create articles
* Retrieve an article by ID
* Retrieve all articles
* JWT authentication and authorization
* PostgreSQL database
* Async SQLAlchemy ORM
* Docker support
* Pydantic validation
* Repository and Service layers

## Tech Stack

* Python 3.13
* FastAPI
* PostgreSQL
* SQLAlchemy 2.0
* Pydantic v2
* LangGraph
* LangChain
* OpenAI
* Aiogram
* Docker
* JWT

## Project Structure

```text
app/
├── ai/
├── api/
├── db/
├── repositories/
├── services/
├── schemas/
└── main.py

bot/
└── main.py
```

## Installation

Clone the repository:

```bash
git clone <repository_url>
cd AINewsAssistant
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and configure:

```env
DATABASE_URL=
OPENAI_API_KEY=
SECRET_KEY=
TELEGRAM_TOKEN=
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Run the Telegram bot:

```bash
python -m bot.main
```

## Example Commands

Create an article:

```text
Create an article about artificial intelligence
```

Show an article:

```text
Show article with id 12
```

Show all articles:

```text
Show all articles
```

## Architecture

The project follows a layered architecture:

```text
Telegram Bot
      ↓
FastAPI
      ↓
LangGraph Agent
      ↓
Tools
      ↓
Services
      ↓
Repositories
      ↓
PostgreSQL
```

## Future Improvements

* Article status management
* Conversation memory
* Streaming responses
* RAG integration
* Role-based permissions

## License

MIT

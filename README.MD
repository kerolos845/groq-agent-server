# Groq Agent Server

A production-ready REST API for a research AI agent powered by Groq and Tavily.

## Features

- AI agent with tool-calling capability
- Real-time web search via Tavily
- FastAPI REST API with auto-generated Swagger docs
- Dockerized for easy deployment
- Input validation with Pydantic
- Structured logging
- Health check endpoint

## Tech Stack

- Python 3.13
- FastAPI
- Groq (LLM inference)
- Tavily (web search)
- Pydantic (validation)
- Docker

## How It Works

The agent receives a question, decides whether it needs to search the web, executes the search, and returns a synthesized answer. The loop continues until the LLM produces a final response.

## Getting Started

### Prerequisites

- Python 3.13+
- Groq API key from console.groq.com
- Tavily API key from tavily.com

### Local Setup

Clone the repository and install dependencies:

pip install -r requirements.txt

Create a .env file with your API keys:

GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here

Run the server:

uvicorn main:app --reload

Open http://localhost:8000/docs for the interactive API documentation.

### Docker Setup

Build the image:

docker build -t groq-agent-server .

Run the container:

docker run --env-file .env -p 8000:8000 groq-agent-server

## API Endpoints

### GET /health

Returns server status.

### POST /ask

Send a question to the agent.

Request body:

{
  "question": "What is the latest news about AI?"
}

Response:

{
  "answer": "...",
  "question": "What is the latest news about AI?"
}

## Project Structure

groq-agent-server/
- agent.py            # Agent logic with tool-calling loop
- main.py             # FastAPI server
- requirements.txt    # Python dependencies
- Dockerfile          # Docker configuration
- .env                # API keys (not committed)
- .gitignore          # Git ignore rules
- .dockerignore       # Docker ignore rules

## License

MIT

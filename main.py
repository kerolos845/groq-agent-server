import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agent import run_agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="The question to ask the agent"
    )


class AnswerResponse(BaseModel):
    answer: str
    question: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Server starting up...")
    yield
    logger.info("Server shutting down...")


app = FastAPI(
    title="Groq Agent Server",
    description="A research agent API powered by Groq and Tavily",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
async def ask_agent(request: QuestionRequest):
    logger.info(f"Received question: {request.question}")

    try:
        answer = run_agent(request.question)
        logger.info("Agent responded successfully")
        return AnswerResponse(answer=answer, question=request.question)

    except Exception as e:
        logger.error(f"Agent error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Agent failed: {str(e)}"
        )

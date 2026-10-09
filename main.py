import asyncio
import os

from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from contextlib import asynccontextmanager
from keshav_AI import KeshavAIBot
import uvicorn

bot = KeshavAIBot(headless=True)
bot_lock = asyncio.Lock()

API_KEY = os.environ.get("KESHAV_API_KEY")


async def verify_api_key(x_api_key: str | None = Header(default=None)):
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Server misconfigured: KESHAV_API_KEY is not set",
        )
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Keshav AI...")
    await bot.start()
    print("Keshav AI is ready!")
    yield
    await bot.close()
    print("Keshav AI stopped.")


app = FastAPI(
    title="Keshav AI",
    description="Keshav AI API",
    version="1.0",
    lifespan=lifespan
)


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str


@app.post(
    "/ask",
    response_model=AnswerResponse,
    dependencies=[Depends(verify_api_key)],
)
async def ask_question(request: QuestionRequest):
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        async with bot_lock:
            answer = await bot.ask(request.question)
        return {"answer": answer}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def home():
    return {
        "message": "Welcome to Keshav AI API",
        "endpoint": "POST /ask",
        "example": {
            "question": "What is an LLM?"
        }
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)

from fastapi import FastAPI, HTTPException
#  from uuid import UUID, uuid4
from pydantic import BaseModel
from typing import Optional
app = FastAPI()


class Task(BaseModel):
    programming_language: str
    question: str
    answer: str
    notes: Optional[str] = ""


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
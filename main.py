from fastapi import FastAPI, HTTPException
import request
from models import Challenge

app = FastAPI()


@app.post("/feedback/grade", response_model=int)
def get_grade(challenge: Challenge) -> int:
    pass


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
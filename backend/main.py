# main.py
# FastAPI routes. Only passes requests to the controller.
# Run (inside backend/): uvicorn main:app --reload

from typing import List
from fastapi import FastAPI

from controller import Controller

app = FastAPI(title="Ludo")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

game = Controller()  # one game at a time

class NewGame(BaseModel):
    mode: Literal["single", "multi"]
    players: int
    humans: int = 1
    names: List[str] = []

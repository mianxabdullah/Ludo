# main.py
# FastAPI routes. Only passes requests to the controller.
# Run (inside backend/): uvicorn main:app --reload

from pathlib import Path
from typing import List, Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from controller import Controller, GameError

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

class Move(BaseModel):
    piece: int

def run(action, *args):
    try:
        return action(*args)
    except GameError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/state")
def get_state():
    return game.snapshot()


# main.py
# FastAPI routes. Only passes requests to the controller.
# Run (inside backend/): uvicorn main:app --reload

from fastapi import FastAPI

app = FastAPI(title="Ludo")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
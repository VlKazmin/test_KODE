from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from typing import List

import os
import asyncio
import json

app = FastAPI()
DATA_FILE = "notes.json"


class Note(BaseModel):
    title: str
    content: str


def initial_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)


async def read_data():
    async with asyncio.Lock():
        with open(DATA_FILE, "r") as f:
            return json.load(f)


async def write_data(data):
    async with asyncio.Lock():
        with open(DATA_FILE, "r") as f:
            return json.dump(data, f, indent=4)
        
@app.post("/notes", response_model=Note)
async def add_note(note):
    notes = await read_data()
    notes.append(note.dict()) # note.dict()
    await write_data(notes)
    return note  # зачем?

@app.get("/notes", response_model=list[Note])
async def get_notes():
    return await read_data()

initial_data_file()



        


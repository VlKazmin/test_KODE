from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteResponse(BaseModel):
    id: int
    owner: str
    title: str
    content: str

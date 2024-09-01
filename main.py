from typing import Dict, List

from fastapi import Depends, FastAPI, status
from pyaspeller import YandexSpeller

from file_operations.local_file import (
    initial_notes_file,
    read_data,
    write_data,
)
from auth.authorization import get_current_user, initial_users_file
from models.models import NoteCreate, NoteResponse

app = FastAPI()
speller = YandexSpeller()


@app.post(
    "/notes",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_note(
    note: NoteCreate,
    current_user: str = Depends(get_current_user),
) -> Dict[str, any]:
    """
    Добавляет новую заметку.

    Args:
        note (NoteCreate): Объект `NoteCreate` с заголовком и
        содержимым заметки.
        current_user (str, optional): Имя текущего пользователя.

    Returns:
        Dict[str, any]: Возвращает добавленную заметку
        в формате `NoteResponse`.
    """

    notes = await read_data()
    note_id = len(notes) + 1
    new_note = {
        "id": note_id,
        "owner": current_user,
        "title": speller.spelled(note.title),
        "content": speller.spelled(note.content),
    }

    notes.append(new_note)
    await write_data(notes)
    return new_note


@app.get("/notes", response_model=List[NoteResponse])
async def get_notes(
    current_user: str = Depends(get_current_user),
) -> List[Dict[str, any]]:
    """
    Получает список заметок текущего пользователя.

    Args:
        current_user (str, optional): Имя текущего пользователя.

    Returns:
        List[Dict[str, any]]: Возвращает список заметок
        в формате `NoteResponse`.

    """

    notes = await read_data()
    user_notes = [note for note in notes if note["owner"] == current_user]
    return user_notes


initial_notes_file()
initial_users_file()

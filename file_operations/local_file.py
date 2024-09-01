import json
import os

from typing import Dict, List

import aiofiles

DATA_FILE = "data/notes.json"


def initial_notes_file() -> None:
    """
    Инициализация файла notes.json.
    """

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False)


async def read_data() -> List[Dict[str, str]]:
    """
    Чтение данных из файла notes.json.

    Returns:
        List[Dict[str, str]]: Список словарей.
        Если файл не найден возвращается пустой список.
    """

    try:
        async with aiofiles.open(DATA_FILE, "r", encoding="utf-8") as f:
            data = await f.read()
            return json.loads(data)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


async def write_data(data: List[Dict[str, str]]) -> None:
    """
    Запись данных в файл notes.json.

    Args:
        data (List[Dict[str, str]]): Список словарей, представляющих заметки.
    """

    async with aiofiles.open(DATA_FILE, "w", encoding="utf-8") as f:
        await f.write(json.dumps(data, indent=4, ensure_ascii=False))

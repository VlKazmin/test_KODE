import os
import json
from typing import List, Dict

import aiofiles
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

USERS_FILE = "data/users.json"


def initial_users_file() -> None:
    """
    Инициализация файла users.json.
    """

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False)


async def load_users() -> List[Dict[str, str]]:
    """
    Чтение пользователей из файла 'users.json'.

    Эта функция открывает файл users.json и считывает содеримое.

    Возвращает:
        Список словарей.
    """

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False)

    async with aiofiles.open(USERS_FILE, "r", encoding="utf-8") as file:
        content = await file.read()
        return json.loads(content)


async def authenticate_user(credentials: HTTPBasicCredentials) -> str:
    """
    Аутентификация пользователя на основе предоставленных учетных данных.

    Args:
        credentials (HTTPBasicCredentials): Ввведенные пользователем
        имя пользователя и пароль.

    Raises:
        HTTPException: Исключение поднимается, если аутентификация не удалась.

    Returns:
        str: Имя пользователя (username) в случае успешной аутентификации.
    """

    users = await load_users()
    for user in users:
        if (
            user["username"] == credentials.username
            and user["password"] == credentials.password
        ):
            return user["username"]

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Некорректный логин или пароль.",
    )


async def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
) -> str:
    """
    Получение текущего пользователя.

    Args:
        credentials (HTTPBasicCredentials, optional): Ввведенные пользователем
        имя пользователя и пароль.

    Returns:
        str: Имя пользователя (username) в случае успешной аутентификации.
    """

    return await authenticate_user(credentials)

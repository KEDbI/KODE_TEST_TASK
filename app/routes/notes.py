from fastapi import APIRouter, Depends, HTTPException
from app.database.database import (get_notes,
                                   get_user_data,
                                   get_username_by_id,
                                   insert_new_user,
                                   insert_new_note,)
from app.models.pydentic_models import User
from app.core.auth import authenticate_user
from app.yandex_api.speller_api import validate_text


notes_router = APIRouter()


@notes_router.get('/')
async def homepage() -> dict:
    return {'message': 'Добро пожаловать в сервис сохранения заметок! Для возможности чтения и добавления заметок '
                       'необходима регистрация'}


@notes_router.post('/registration')
async def registrate_user(user: User) -> dict:
    check_login = await get_user_data(username=user.username)
    if check_login:
        raise HTTPException(status_code=400, detail="Такой логин уже занят :(")
    await insert_new_user(user.username, user.password)
    return {'message': f'Регистрация прошла успешно! Ваш логин: {user.username}.'}


@notes_router.get('/{user_id}/text-validation')
async def validate_text_with_yandex_speller(user_id: int, note_text: str,
                                            user: User = Depends(authenticate_user)) -> dict:
    validated_text = await validate_text(note_text)
    return {'message': 'Результат проверки сервисом Yandex Speller ниже. Внести заметку в базу данных?',
            'text_errors': validated_text}


@notes_router.post('/{user_id}/add-note')
async def create_new_note(user_id: int, note_text: str, user: User = Depends(authenticate_user)) -> dict:
    await insert_new_note(user_id, note_text)
    return {'message': 'Заметка внесена!'}


@notes_router.get('/{user_id}/note_cancelled')
async def notify_note_cancelled(user_id: int, user: User = Depends(authenticate_user)) -> dict:
    return {'message': 'Внесение заметки отменено.'}


@notes_router.get('/{user_id}/view-notes')
async def view_user_notes(user_id: int, user: User = Depends(authenticate_user)) -> dict:
    username_from_db = await get_username_by_id(user_id)
    if username_from_db != user['username']:
        raise HTTPException(status_code=403, detail='Вы пытаетесь просмотреть не свои заметки')
    notes = await get_notes(user_id)
    return {'message': notes}

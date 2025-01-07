from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from matchvibe.app.database import SessionDep
from matchvibe.app.users.schemas import Users

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get('/', summary='Получить всех пользователей')
def get_all_users(session: SessionDep) -> list[Users]:
    users = session.exec(select(Users)).all()
    return users


@router.get('/{user_id}', summary='Получить пользователя по id')
def get_user_by_user_id(user_id: int, session: SessionDep) -> Users:
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.post('/', summary='Добавить пользователя')
def create_user(user: Users, session: SessionDep) -> Users:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete('/{user_id}', summary='Удалить пользователя')
def delete_hero(user_id: int, session: SessionDep):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    session.delete(user)
    session.commit()
    return {'ok': True}

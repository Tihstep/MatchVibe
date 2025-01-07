from pydantic import EmailStr, field_validator
from sqlmodel import Field
from datetime import date, datetime
import re
from matchvibe.app.database import Base


class Users(Base, table=True):
    user_id: int | None = Field(default=None, primary_key=True)
    phone_number: str = Field(default=None, description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: str = Field(default=None, min_length=1, max_length=50, description='Имя пользователя')
    last_name: str = Field(default=None, min_length=1, max_length=50, description='Фамилия пользователя')
    date_of_birth: date = Field(default=None, description='Дата рождения пользователя')
    email: EmailStr = Field(default=None, description='Электронная почта пользователя')

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r'^\+\d{1,15}$', values):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return values

    @field_validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls, values: date):
        if values and values >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        return values

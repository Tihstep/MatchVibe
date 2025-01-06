from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date, datetime
import re


class User(BaseModel):
    user_id: int
    phone_number: str = Field(
        default=None,
        description="Номер телефона в международном формате, начинающийся с '+'",
    )
    first_name: str = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="Имя студента, от 1 до 50 символов",
    )
    last_name: str = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="Фамилия студента, от 1 до 50 символов",
    )
    date_of_birth: date = Field(
        default=None, description="Дата рождения студента в формате ГГГГ-ММ-ДД"
    )
    email: EmailStr = Field(default=None, description="Электронная почта студента")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r"^\+\d{1,15}$", values):
            raise ValueError(
                'Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр'
            )
        return values

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, values: date):
        if values and values >= datetime.now().date():
            raise ValueError("Дата рождения должна быть в прошлом")
        return values

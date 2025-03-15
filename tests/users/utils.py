from typing import Literal
from sqlalchemy.inspection import inspect
from app.models import User


def to_dict(
    user: User, fields: list[Literal['id', 'name', 'email']] | None = None
) -> dict:
    result = {
        column.name: getattr(user, column.name)
        for column in inspect(user.__class__).columns
        if (column.name in fields if fields else True)
    }
    if created_at := result.get('created_at'):
        result['created_at'] = created_at.isoformat()
    return result

from pydantic import BaseModel, Field, field_validator
from enum import Enum

class Languages(Enum):
    RU = 'ru'
    EN = 'en'

class FetchNewsData(BaseModel):
    q: str = Field(default='bitcoin', min_length=1)
    lg: Languages

    @field_validator('q', 'lg')
    def validate_query(cls, value):
        if not value:
            raise ValueError('Query string \'q\' cannot be empty.')
        return value

    def to_json(self):
        return {
            'q': self.q,
            'lg': self.lg.value
        }

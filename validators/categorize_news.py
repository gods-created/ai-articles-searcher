from pydantic import BaseModel, Field, field_validator
from enum import Enum

class Categories(Enum):
    BUSINESS = 'business'
    ENTERTAINMENT = 'entertainment'
    GENERAL = 'general'
    HEALTH = 'health'
    SCIENCE = 'science'
    SPORTS = 'sports'
    TECHNOLOGY = 'technology'

class CategorizeNewsData(BaseModel):
    category: Categories

    @field_validator('category')
    def validate_query(cls, value):
        if not value:
            raise ValueError('Query string \'q\' cannot be empty.')
        return value

    def to_json(self):
        return {
            'category': self.category.value
        }

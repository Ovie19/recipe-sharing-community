from enum import Enum

class Category(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    APPETIZER = "appetizer"
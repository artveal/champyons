import json
from sqlalchemy.types import TypeDecorator, Text
from typing import List, Any

class JSONEncodedList(TypeDecorator):
    """
    Generic SQLAlchemy TypeDecorator to store a list as JSON.
    - Accepts any list
    - Serializes to JSON string for the DB
    - Deserializes back to list on load
    """
    impl = Text
    cache_ok = True

    def process_bind_param(self, value: List[Any], dialect):
        if value is None:
            return "[]"
        if not isinstance(value, list):
            raise ValueError("Expected a list for JSONEncodedList column")
        return json.dumps(value)

    def process_result_value(self, value: str, dialect):
        if not value:
            return []
        return json.loads(value)
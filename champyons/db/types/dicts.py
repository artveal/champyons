import json
from sqlalchemy.types import TypeDecorator, Text
from typing import Any, Dict

class JSONEncodedDict(TypeDecorator):
    """
    Generic SQLAlchemy TypeDecorator to store dicts as JSON.
    - Accepts any dict[str, Any]
    - Serializes to JSON for the DB
    - Deserializes back to dict on load
    """
    impl = Text
    cache_ok = True

    def process_bind_param(self, value: Dict[str, Any], dialect):
        if value is None:
            return "{}"
        if not isinstance(value, dict):
            raise ValueError("Expected dict for JSONEncodedDict column")
        return json.dumps({str(k): v for k, v in value.items()})

    def process_result_value(self, value: str, dialect):
        if not value:
            return {}
        raw = json.loads(value)
        return {str(k): v for k, v in raw.items()}
from dataclasses import dataclass, field
from typing import Dict, Any
from pathlib import Path
import json
from .nationality_rules import NationalityRules

DATA_DIR = Path(__file__).parent.parent / "data"

@dataclass(frozen=True)
class Demographics:
    code: str
    nationality_rules: NationalityRules = field(default_factory=NationalityRules)
    cultures: Dict[str, float] = field(default_factory=lambda: {"world": 1.0})
    immigrant_probability: float = 0.0
    immigration_sources: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        if not (0.0 <= self.immigrant_probability <= 1.0):
            raise ValueError(f"immigrant_probability must be between 0 and 1, got {self.immigrant_probability}")

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Demographics":
        nr_data = data.get("nationality_rules", {})
        nr = NationalityRules(**nr_data)
        return cls(
            code=data["code"],
            nationality_rules=nr,
            cultures=data.get("cultures", {"world": 1.0}),
            immigrant_probability=data.get("immigrant_probability", 0.0),
            immigration_sources=data.get("immigration_sources", {})
        )

    @classmethod
    def from_json_file(cls, filename: str) -> "Demographics":
        path = DATA_DIR / "demographics" / f"{filename}.json"
        with open(path, encoding="utf-8") as f:
            data: dict = json.load(f)
            data["code"] = filename
        return cls.from_json(data)
    
    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "nationality_rules": self.nationality_rules.to_dict(),
            "cultures": self.cultures,
            "immigrant_probability": self.immigrant_probability,
            "immigration_sources": self.immigration_sources,
        }

    def to_json(self) -> str:
        data = self.to_dict()
        data.pop("code")
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def to_json_file(self, filename: str) -> None:
        path = DATA_DIR / "demographics" / f"{filename}.json"
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_json())
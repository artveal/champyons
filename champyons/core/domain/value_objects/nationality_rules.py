from dataclasses import dataclass
import json

@dataclass(frozen=True)
class NationalityRules:
    nationality_by_birth: bool = True
    nationality_by_ancestry: bool = True

    def to_dict(self) -> dict:
        return {
            "nationality_by_birth": self.nationality_by_birth,
            "nationality_by_ancestry": self.nationality_by_ancestry,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)
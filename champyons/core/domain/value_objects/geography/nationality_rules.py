from dataclasses import dataclass, field
import json

from typing import Optional

@dataclass(frozen=True)
class NationalityRules:
    nationality_by_birth: bool = True # nationality awarded for being born in this nationality
    nationality_by_ancestry: bool = True # nationality awarded for being a descendant of this nationality

    default_residence_time_rule: Optional[int] = None # Default time of residence for gaining this nationality, in years. If None no nationality by residence will be given. 0 means that all residents will be awarded a nationality
    residence_time_rule_by_nation: dict[str, int] = field(default_factory=dict) # special rules for other nations when giving nationality by residence time.

    def get_residence_time_rule_for_nation_code(self, nation_code: str):
        return self.residence_time_rule_by_nation.get(nation_code, self.default_residence_time_rule)

    def to_dict(self) -> dict:
        return self.__dict__

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)
from dataclasses import dataclass, field
from typing import Dict, List, Any
from pathlib import Path
import random
import json

DATA_DIR = Path(__file__).parent.parent / "data"

@dataclass(frozen=True)
class Culture:
    code: str
    male_names: Dict[str, float] = field(default_factory=dict)
    female_names: Dict[str, float] = field(default_factory=dict)
    male_surnames: Dict[str, float] = field(default_factory=dict)
    female_surnames: Dict[str, float] = field(default_factory=dict)
    neuter_surnames: Dict[str, float] = field(default_factory=dict)
    male_composition_rule: List[str] = field(default_factory=list)
    female_composition_rule: List[str] = field(default_factory=list)

    def __post_init__(self):
        # Validar reglas de composición
        for rules in (self.male_composition_rule, self.female_composition_rule):
            for step in rules:
                try:
                    name_type, genders = [i.strip() for i in step.split(":")]
                except ValueError:
                    raise ValueError(f"Invalid composition step format: '{step}'")
                if name_type not in ("name", "surname"):
                    raise ValueError(f"Invalid name type '{name_type}' in '{step}'")
                for g in genders.split("|"):
                    if g not in ("male", "female", "neuter"):
                        raise ValueError(f"Invalid gender '{g}' in '{step}'")

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Culture":
        return cls(
            code=data["code"],
            male_names=data.get("male_names", {}),
            female_names=data.get("female_names", {}),
            male_surnames=data.get("male_surnames", {}),
            female_surnames=data.get("female_surnames", {}),
            neuter_surnames=data.get("neuter_surnames", {}),
            male_composition_rule=data.get("male_composition_rule", []),
            female_composition_rule=data.get("female_composition_rule", [])
        )

    @classmethod
    def from_json_file(cls, filename: str) -> "Culture":
        path = DATA_DIR / "culture" / f"{filename}.json"
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            data["code"] = filename
        return cls.from_json(data)
    
    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "male_names": self.male_names,
            "female_names": self.female_names,
            "male_surnames": self.male_surnames,
            "female_surnames": self.female_surnames,
            "neuter_surnames": self.neuter_surnames,
            "male_composition_rule": self.male_composition_rule,
            "female_composition_rule": self.female_composition_rule,
        }
    
    def to_json(self) -> str:
        data = self.to_dict()
        data.pop("code")
        return json.dumps(data, ensure_ascii=False)
    
    def to_json_file(self, filename: str) -> None:
        path = DATA_DIR / "demographics" / f"{filename}.json"
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_json())

    def get_random_fullname(self, gender: str, seed: int | None = None) -> list[str]:
        rng = random.Random(seed)
        if gender.lower() == "male":
            composition_rule = self.male_composition_rule
        elif gender.lower() == "female":
            composition_rule = self.female_composition_rule
        else:
            raise ValueError(f"Incorrect gender: {gender}")

        full_name = []
        for step in composition_rule:
            name_type, genders = [i.strip() for i in step.split(":")]
            dataset = {}
            gender_variations = genders.lower().split("|")
            if "male" in gender_variations:
                dataset.update(self.male_names if name_type == "name" else self.male_surnames)
            if "female" in gender_variations:
                dataset.update(self.female_names if name_type == "name" else self.female_surnames)
            if "neuter" in gender_variations:
                dataset.update(self.neuter_surnames)
            if not dataset:
                raise RuntimeError(f"Empty dataset for step '{step}'")
            full_name.append(rng.choices(list(dataset.keys()), weights=list(dataset.values()))[0])
        return full_name
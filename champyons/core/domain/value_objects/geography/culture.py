from dataclasses import dataclass, field
from typing import Dict, List, Any
from pathlib import Path
import random
import json

DATA_DIR = Path(__file__).parent.parent / "data"

@dataclass(frozen=True)
class Culture:
    " A dataset of names, surnames and full name composition rules, used for player generation "
    # Names
    male_names: Dict[str, float] = field(default_factory=dict)
    female_names: Dict[str, float] = field(default_factory=dict)

    # Surnames
    male_surnames: Dict[str, float] = field(default_factory=dict)
    female_surnames: Dict[str, float] = field(default_factory=dict)
    neuter_surnames: Dict[str, float] = field(default_factory=dict)

    # Full name composition rules
    male_composition_rule: List[str] = field(default_factory=list)
    female_composition_rule: List[str] = field(default_factory=list)

    # IDEA TO-DO: Implement here ethnicity

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
        return cls.from_json(data)
    
    def to_dict(self) -> dict:
        return {
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
    
@dataclass(frozen=True)
class CultureDistribution:
    """
    Represents the cultural composition of a nationality with probability weights.
    Used for generating realistic player names, appearances, etc.
    """
    distributions: Dict[Culture, float] = field(default_factory=dict)
    
    def __post_init__(self):
        # Validate distributions sum up to 1.0
        total = sum(self.distributions.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError(
                f"Culture probabilities must sum to 1.0, got {total}"
            )
        
        # Validate all posibilities are positive
        if any(prob < 0 for prob in self.distributions.values()):
            raise ValueError("All probabilities must be >= 0")
    
    def get_random_culture(self) -> Culture:
        """Returns a random Culture based on probability distribution."""
        import random
        
        cultures = list(self.distributions.keys())
        weights = list(self.distributions.values())
        return random.choices(cultures, weights=weights, k=1)[0]
    
    def get_probability(self, culture: Culture) -> float:
        """Returns the probability for a specific culture."""
        return self.distributions.get(culture, 0.0)
    
    def get_dominant_culture(self) -> Culture:
        """Returns the culture with highest probability."""
        return max(self.distributions.items(), key=lambda x: x[1])[0]
    
    @classmethod
    def single_culture(cls, culture: Culture) -> 'CultureDistribution':
        """Factory: Creates a distribution with 100% one culture."""
        return cls(distributions={culture: 1.0})
    
    @classmethod
    def mixed(cls, culture_weights: Dict[Culture, float]) -> 'CultureDistribution':
        """Factory: Creates a distribution with multiple cultures (auto-normalizes)."""
        total = sum(culture_weights.values())
        normalized = {
            culture: weight / total 
            for culture, weight in culture_weights.items()
        }
        return cls(distributions=normalized)
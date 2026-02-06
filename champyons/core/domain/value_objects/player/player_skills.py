from dataclasses import dataclass, field, fields
from typing import Dict

@dataclass
class PlayerSkills:
    shooting: float = field(default=10.0, metadata={
        "category": "technical",
        "weights_by_position": {"ST": 0.4, "CB": 0.1}
    })
    passing: float = field(default=10.0, metadata={
        "category": "technical",
        "weights_by_position": {"ST": 0.2, "CB": 0.2}
    })
    dribbling: float = field(default=10.0, metadata={
        "category": "technical",
        "weights_by_position": {"ST": 0.3, "CB": 0.1}
    })
    stamina: float = field(default=10.0, metadata={
        "category": "physical",
        "weights_by_position": {"ST": 0.05, "CB": 0.3}
    })
    strength: float = field(default=10.0, metadata={
        "category": "physical",
        "weights_by_position": {"ST": 0.05, "CB": 0.3}
    })

    def __post_init__(self):
        # Validación de valores entre 0 y 20
        for f in fields(self):
            value = getattr(self, f.name)
            if not (0 <= value <= 20):
                raise ValueError(f"Skill '{f.name}' must be between 0 and 20, got {value}")

    def weighted_total(self, position: str) -> float:
        total = 0.0
        for f in fields(self):
            value = getattr(self, f.name)
            weights: Dict[str, float] = f.metadata.get("weights_by_position", {})
            total += value * weights.get(position, 0.0)
        return total

    def group_by_category(self) -> Dict[str, Dict[str, float]]:
        result: Dict[str, Dict[str, float]] = {}
        for f in fields(self):
            category = f.metadata.get("category", "unknown")
            result.setdefault(category, {})[f.name] = getattr(self, f.name)
        return result
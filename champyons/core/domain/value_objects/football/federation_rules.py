# champyons/core/domain/value_objects/geography/nation_rules.py
from dataclasses import dataclass
from datetime import date
from typing import Optional
from ..game.transfer_window import TransferWindow

@dataclass(frozen=True)
class FederationRules:
    """
    Rules and regulations specific to a nation/nationality (represented by its federation).
    
    Domain Rules:
    - Defines transfer windows that override season defaults
    - Squad rules for competitions in this nation
    - Registration rules
    """
    
    # Transfer windows (override season defaults)
    # Store as month/day so they apply to any year
    window_1_start_month: int = 7   # July
    window_1_start_day: int = 1
    window_1_duration_days: int = 61  # ~2 months
    
    window_2_start_month: int = 1   # January  
    window_2_start_day: int = 1
    window_2_duration_days: int = 31  # 1 month
    
    # Time offset for this nation (UTC)
    time_offset: float = 0.0  # Hours from UTC
    
    # Squad rules
    default_squad_min_size: int = 18
    default_squad_max_size: int = 25
    max_foreign_players: Optional[int] = None
    min_homegrown_players: Optional[int] = None
    
    # Emergency signings
    allows_emergency_signings: bool = True
    
    def __post_init__(self):
        # Validate months
        if not 1 <= self.window_1_start_month <= 12:
            raise ValueError("Window 1 start month must be 1-12")
        if not 1 <= self.window_2_start_month <= 12:
            raise ValueError("Window 2 start month must be 1-12")
        
        # Validate days
        if not 1 <= self.window_1_start_day <= 31:
            raise ValueError("Window 1 start day must be 1-31")
        if not 1 <= self.window_2_start_day <= 31:
            raise ValueError("Window 2 start day must be 1-31")
        
        # Validate durations
        if self.window_1_duration_days < 1:
            raise ValueError("Window 1 duration must be at least 1 day")
        if self.window_2_duration_days < 1:
            raise ValueError("Window 2 duration must be at least 1 day")
        
        # Validate time offset
        if not -14 <= self.time_offset <= 14:
            raise ValueError("Time offset must be between -14 and +14")
        
        # Validate squad sizes
        if self.default_squad_max_size < self.default_squad_min_size:
            raise ValueError("Max squad size must be >= min squad size")
    
    def get_transfer_window(
        self, 
        year: int, 
        window_number: int
    ) -> TransferWindow:
        """
        Creates a TransferWindow for this nation in a specific year.
        
        Args:
            year: The year to create window for
            window_number: 1 or 2
        
        Returns:
            TransferWindow configured for this nation
        """
        from datetime import timedelta
        
        if window_number == 1:
            start = date(year, self.window_1_start_month, self.window_1_start_day)
            end = start + timedelta(days=self.window_1_duration_days)
        elif window_number == 2:
            # Window 2 might be in next year (e.g., Jan 2025 for 2024/25 season)
            start = date(year + 1, self.window_2_start_month, self.window_2_start_day)
            end = start + timedelta(days=self.window_2_duration_days)
        else:
            raise ValueError("Window number must be 1 or 2")
        
        return TransferWindow(
            start_date=start,
            end_date=end,
            time_offset=self.time_offset
        )
    
    @classmethod
    def default(cls) -> "FederationRules":
        """Returns default nation rules (UEFA-like)."""
        return cls()
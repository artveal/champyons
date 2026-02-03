from enum import Enum, auto

class PositionRoles(Enum):
    pass

class PositionAttackingRoles(PositionRoles):
    # Goalkeeper (GK) roles
    GK = auto()
    GK_BALL_PLAYING = auto()
    GK_NO_NONSENSE= auto()

    # Center back (CB) roles
    CB = auto()
    CB_OVERLAPPING = auto()
    CB_ADVANCED = auto()
    CB_BALL_PLAYING= auto()
    CB_NO_NONSENSE= auto()
    CB_WIDE_CENTRE = auto()

    # Full back (FB: RB/LB) roles
    FB = auto()
    FB_INSIDE_FULLBACK = auto()
    FB_WINGBACK = auto()
    FB_PLAYMAKING_WINGBACK = auto()
    FB_INSIDE_WINGBACK = auto()

    # Wingback (WB: RWB/LWB) roles
    WB = auto()
    WB_ADVANCED = auto()
    WB_PLAYMAKER = auto()
    WB_INSIDE = auto()

    # Defensive Midfielder (DM) roles
    DM = auto()
    DM_BOX_TO_BOX = auto()
    DM_HALFBACK = auto()
    DM_DEEP_LYING_PLAYMAKER = auto()
    DM_BOX_TO_BOX_PLAYMAKER = auto()

    # Central Midfielder (CM) roles
    CM = auto()
    CM_MIDFIELD_PLAYMAKER = auto()
    CM_ADVANCED_PLAYMAKER = auto()
    CM_ATTACKING = auto()
    CM_WIDE_CENTRAL = auto()
    CM_CHANNEL = auto()

    # Left/right midfielder (WM: RM/LM) roles
    WM_WINGER = auto()
    WM_WIDE_MIDFIELDER = auto()
    WM_INSIDE = auto()
    WM_PLAYMAKER = auto()

    # Attacking midfielder (AM) roles
    AM = auto()
    AM_ADVANCED_PLAYMAKER = auto()
    AM_CHANNEL = auto()
    AM_SECOND_STRIKER = auto()
    AM_FREE_ROLE = auto()

    # Striker (ST) roles
    ST_CHANNEL = auto()
    ST_DEEP_LYING = auto()
    ST_FALSE_NINE = auto()
    ST_CENTRE_FORWARD = auto()
    ST_POACHER = auto()
    ST_TARGET_FORWARD = auto()

    # Winger (WF: RW/LW) roles
    WF_WIDE_FORWARD = auto()
    WF_WINGER = auto()
    WF_INSIDE = auto()
    WF_INSIDE_FORWARD = auto()
    WF_PLAYMAKER = auto()

class PositionDefendingRoles(PositionRoles):
    # Goalkeeper roles
    GK = auto()
    GK_LINE_HOLDING = auto()
    GK_SWEEPER = auto()
    
    # Center back roles
    CB = auto()
    CB_COVERING = auto()
    CB_COVERING_WIDE = auto()
    CB_WIDE= auto()
    CB_STOPPING= auto()
    CB_STOPPING_WIDE = auto()

    # Full back roles
    FB = auto()
    FB_HOLDING = auto()
    FB_PRESSING = auto()

    # Wingback roles
    WB = auto()
    WB_HOLDING = auto()
    WB_PRESSING = auto()

    # Defensive Midfielder roles
    DM = auto()
    DM_WIDE_COVERING = auto()
    DM_SCREENING = auto()
    DM_PRESSING = auto()
    DM_DROPPING = auto()

    # Central Midfielder roles
    CM = auto()
    CM_WIDE_COVERING = auto()
    CM_SCREENING = auto()
    CM_PRESSING = auto()

    # Left/right midfielder roles
    WM_TRACKING = auto()
    WM_WIDE_MIDFIELDER = auto()
    WM_WIDE_OUTLET = auto()

    # Attacking midfielder roles
    AM = auto()
    AM_SPLITTING_OUTLET = auto()
    AM_CENTRAL_OUTLET = auto()
    AM_TRACKING = auto()

    # Striker roles
    ST_CENTRE_FORWARD = auto()
    ST_SPLITTING_OUTLET = auto()
    ST_CENTRAL_OUTLET = auto()
    ST_TRACKING = auto()

    # Winger Roles
    WF_WINGER = auto()
    WF_WIDE_OUTLET = auto()
    WF_INSIDE_OUTLET = auto()
    WF_TRACKING = auto()
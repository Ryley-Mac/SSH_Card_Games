from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Any

class SignalType(Enum):
    WIN = auto()
    LOSE = auto()
    DRAW = auto()

    BLACKJACK = auto()
    BUST = auto()
    HIT = auto()
    STAY = auto()
    DEAL = auto()

    ERROR = auto()
    WARNING = auto()
    INFO = auto()

    DISCONNECT = auto()
    RECONNECT = auto()

@dataclass
class Signal:
    type: SignalType
    message: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    value: int = 0

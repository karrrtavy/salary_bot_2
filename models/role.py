from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=False)
class Role():
    TABLE_KEY = "table_2"
    c_id: int
    c_1: str
    c_2: float
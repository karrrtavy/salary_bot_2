from dataclasses import dataclass
from datetime import date

@dataclass(frozen=False)
class Schedule:
    TABLE_KEY = "table_4"

    c_id: int
    c_1: date
    c_2: int

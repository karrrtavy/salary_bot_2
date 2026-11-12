from dataclasses import dataclass

@dataclass(frozen=False)
class Employee:
    TABLE_KEY = "table_3"

    c_id: int
    c_1: str
    c_2: str
    c_3: int
    c_4: int
    c_5: int
    c_6: int
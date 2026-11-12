from dataclasses import dataclass

@dataclass(frozen=False)
class Object:
    TABLE_KEY = "table_1"

    c_id: int
    c_1: str
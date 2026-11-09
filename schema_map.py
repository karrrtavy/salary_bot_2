import json
import os

from pathlib import Path

NAMES = None

def load():
    global NAMES
    if NAMES is None:
        try:
            path = Path(os.environ["SCHEMA_MAP_PATH"])
            NAMES = json.loads(path.read_text(encoding="utf-8"))
        except (KeyError, OSError, ValueError):
            raise RuntimeError("не удалось загрузить карту схем") from None
    return NAMES

def get_table(key:str) -> dict:
    names = load()
    try:
        return names[key]
    except KeyError:
        raise RuntimeError("неизвестная таблица в карте схем") from None
import json
from collections.abc import Callable
from dataclasses import is_dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any

import pandas as pd
from custom_python_logger import get_logger
from pydantic import BaseModel

from python_base_toolkit.consts.general import LOGGER_NAME

logger = get_logger(LOGGER_NAME)


_TYPE_SERIALIZERS: tuple[tuple[type | tuple[type, ...], Callable[[Any], object]], ...] = (
    (BaseModel, lambda obj: obj.model_dump()),
    (type, lambda obj: obj.__name__),
    (Enum, lambda obj: obj.value),
    ((set, tuple), list),
    ((datetime, date, time), lambda obj: obj.isoformat()),
    (Decimal, float),
    (Path, str),
)


def default_serialize(obj: object) -> object:
    if is_dataclass(obj) and not isinstance(obj, type | BaseModel):
        return obj.__dict__
    for types, serializer in _TYPE_SERIALIZERS:
        if isinstance(obj, types):
            return serializer(obj)
    if obj is pd.NA:
        return None
    logger.error(f"Object is not serializable: {obj}")
    raise TypeError(f"Type {type(obj)} not serializable")


def to_json_serializable(obj: Any) -> Any:
    """Convert an object to a JSON-serializable structure."""
    serialized_json = json.dumps(obj, default=default_serialize)
    return json.loads(serialized_json)

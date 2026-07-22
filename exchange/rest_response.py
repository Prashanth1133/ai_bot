from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class RestResponse:

    success: bool

    status_code: int

    payload: Any

    error: str | None = None
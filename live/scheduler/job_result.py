from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class JobResult:

    job_id: str

    success: bool

    duration: float

    message: str = ""

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )
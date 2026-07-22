from dataclasses import dataclass


@dataclass(slots=True)
class Excursion:

    mfe: float

    mae: float
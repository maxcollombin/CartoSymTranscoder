from dataclasses import dataclass
from typing import Optional
from enum import Enum

class Month(Enum):
    JANUARY = "january"
    FEBRUARY = "february"
    MARCH = "march"
    APRIL = "april"
    MAY = "may"
    JUNE = "june"
    JULY = "july"
    AUGUST = "august"
    SEPTEMBER = "september"
    OCTOBER = "october"
    NOVEMBER = "november"
    DECEMBER = "december"

@dataclass
class Date:
    year: int
    month: 'Month'
    day: int

@dataclass
class TimeOfDay:
    hour: int
    minutes: int
    seconds: float

@dataclass
class TimeInstant:
    date: Date
    time: TimeOfDay

@dataclass
class TimeInterval:
    start: TimeInstant
    end: TimeInstant

@dataclass
class Visualization:
    scale_denominator: float
    date_time: Optional[TimeInstant] = None
    date: Optional[Date] = None
    time_of_day: Optional[TimeOfDay] = None
    time_interval: Optional[TimeInterval] = None
    pass_: int = 0
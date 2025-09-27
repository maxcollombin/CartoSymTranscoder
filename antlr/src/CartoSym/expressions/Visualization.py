from dataclasses import dataclass
from typing import Optional
from enum import Enum

class Month(Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

@dataclass
class Date:
    year: int
    month: Month
    day: int

    def __post_init__(self):
        if not (1 <= self.day <= 31):
            raise ValueError(f"Invalid day: {self.day}")
        if self.month in {Month.APRIL, Month.JUNE, Month.SEPTEMBER, Month.NOVEMBER} and self.day > 30:
            raise ValueError(f"Invalid day: {self.day} for month: {self.month.name}")
        if self.month == Month.FEBRUARY:
            if (self.year % 4 == 0 and self.year % 100 != 0) or (self.year % 400 == 0):  # Leap year
                if self.day > 29:
                    raise ValueError(f"Invalid day: {self.day} for February in a leap year")
            elif self.day > 28:
                raise ValueError(f"Invalid day: {self.day} for February in a non-leap year")

@dataclass
class TimeOfDay:
    hour: int
    minutes: int
    seconds: float

    def __post_init__(self):
        if not (0 <= self.hour < 24):
            raise ValueError(f"Invalid hour: {self.hour}")
        if not (0 <= self.minutes < 60):
            raise ValueError(f"Invalid minutes: {self.minutes}")
        if not (0 <= self.seconds < 60):
            raise ValueError(f"Invalid seconds: {self.seconds}")

@dataclass
class TimeInstant:
    date: Date
    timeOfDay: TimeOfDay

@dataclass
class TimeInterval:
    start: TimeInstant
    end: TimeInstant

    def __post_init__(self):
        if self.start.date.year > self.end.date.year or (
            self.start.date.year == self.end.date.year and
            self.start.date.month.value > self.end.date.month.value
        ) or (
            self.start.date.year == self.end.date.year and
            self.start.date.month.value == self.end.date.month.value and
            self.start.date.day > self.end.date.day
        ):
            raise ValueError("Start time must be before end time")

@dataclass
class Visualization:
    scale_denominator: float
    date_time: Optional[TimeInstant] = None
    date: Optional[Date] = None
    time_of_day: Optional[TimeOfDay] = None
    time_interval: Optional[TimeInterval] = None
    pass_: int = 0
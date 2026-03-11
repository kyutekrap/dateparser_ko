from typing import TypedDict, List


class ParseResult(TypedDict):
    found_dates: List[DateObject]
    used_tokens: List[tuple]
    cleaned: str


class DateObject(TypedDict):
    y: int
    m: int
    d: int

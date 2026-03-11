from dateparser_ko.types import DateObject
from typing import List
from datetime import datetime, timezone


def last_quarter(context: str, temp_date: DateObject) -> List[DateObject]:
    current_date = datetime.now(tz=timezone.utc)
    current_quarter = (current_date.month - 1) // 3 + 1
    if current_quarter == 1:
        start_date = DateObject(y=current_date.year-1, m=1, d=1)
        end_date = DateObject(y=current_date.year-1, m=3, d=31)
    elif current_quarter == 2:
        start_date = DateObject(y=current_date.year, m=1, d=1)
        end_date = DateObject(y=current_date.year, m=3, d=31)
    elif current_quarter == 3:
        start_date = DateObject(y=current_date.year, m=2, d=1)
        end_date = DateObject(y=current_date.year, m=5, d=31)
    else:
        start_date = DateObject(y=current_date.year, m=6, d=1)
        end_date = DateObject(y=current_date.year, m=9, d=30)

    return [start_date, end_date]

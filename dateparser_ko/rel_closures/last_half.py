from dateparser_ko.types import DateObject
from typing import List
from datetime import datetime, timezone


def last_half(context: str, temp_date: DateObject) -> List[DateObject]:
    year = max(datetime.now(tz=timezone.utc).year, temp_date["y"])
    try:
        int_context = int(context)
        if int_context > 1000:
            year = int_context
    except Exception as _:
        pass

    start_date = DateObject(y=year, m=6, d=1)
    end_date = DateObject(y=year, m=12, d=31)

    return [start_date, end_date]

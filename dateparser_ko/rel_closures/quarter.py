from dateparser_ko.types import DateObject
from typing import List
from datetime import datetime, timezone


def quarter(context: str, temp_date: DateObject) -> List[DateObject]:
    year = temp_date["y"] if temp_date["y"] > 0 else datetime.now(tz=timezone.utc).year

    try:
        int_context = int(context)
        if int_context == 1:
            start_date = DateObject(y=year, m=1, d=1)
            end_date = DateObject(y=year, m=3, d=31)
            return [start_date, end_date]
        elif int_context == 2:
            start_date = DateObject(y=year, m=4, d=1)
            end_date = DateObject(y=year, m=6, d=30)
            return [start_date, end_date]
        elif int_context == 3:
            start_date = DateObject(y=year, m=7, d=1)
            end_date = DateObject(y=year, m=9, d=30)
            return [start_date, end_date]
        elif int_context == 4:
            start_date = DateObject(y=year, m=10, d=1)
            end_date = DateObject(y=year, m=12, d=31)
            return [start_date, end_date]

    except Exception as _:
        pass

    return []

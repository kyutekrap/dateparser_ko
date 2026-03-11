from dateparser_ko.types import DateObject
from datetime import datetime, timezone


def today(context: str, temp_date: DateObject) -> DateObject:
    today_date = datetime.now(tz=timezone.utc)
    return DateObject(y=today_date.year, m=today_date.month, d=today_date.day)

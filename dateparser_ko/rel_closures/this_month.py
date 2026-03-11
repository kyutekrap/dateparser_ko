from dateparser_ko.types import DateObject
from datetime import datetime, timezone


def this_month(context: str, temp_date: DateObject) -> DateObject:
    today = datetime.now(tz=timezone.utc)
    return DateObject(y=today.year, m=today.month, d=0)

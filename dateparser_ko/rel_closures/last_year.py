from dateparser_ko.types import DateObject
from datetime import datetime, timezone


def last_year(context: str, temp_date: DateObject) -> DateObject:
    return DateObject(y=datetime.now(tz=timezone.utc).year - 1, m=0, d=0)

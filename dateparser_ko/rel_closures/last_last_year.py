from dateparser_ko.types import DateObject
from datetime import datetime, timezone


def last_last_year(context: str, temp_date: DateObject) -> DateObject:
    year = datetime.now(tz=timezone.utc).year - 2
    date_obj = DateObject(y=year, m=0, d=0)
    return date_obj

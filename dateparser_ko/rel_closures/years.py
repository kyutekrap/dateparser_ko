from dateutil.relativedelta import relativedelta
from dateparser_ko.types import DateObject
from datetime import datetime, timezone, date
from typing import List


def years(context: str, temp_date: DateObject) -> List[DateObject]:
    today = datetime.now(tz=timezone.utc)

    if temp_date["y"] == 0 and temp_date["m"] == 0 and temp_date["d"] == 0:
        _end_date = today.replace(month=1, day=1) - relativedelta(days=1)
        end_date = DateObject(y=_end_date.year, m=_end_date.month, d=_end_date.day)
        relative_date = _end_date - relativedelta(years=int(context)) + relativedelta(years=1)
        start_date = DateObject(y=relative_date.year, m=1, d=1)
        return [start_date, end_date]

    else:
        given_date = date(
            temp_date["y"] if temp_date["y"] > 0 else today.year,
            temp_date["m"] if temp_date["m"] > 0 else 1,
            temp_date["d"] if temp_date["d"] > 0 else 1
        )
        start_date = DateObject(y=given_date.year, m=given_date.month, d=given_date.day)
        relative_date = given_date + relativedelta(years=int(context))
        relative_date = relative_date.replace(day=1) - relativedelta(days=1)
        end_date = DateObject(y=relative_date.year, m=relative_date.month, d=relative_date.day)
        return [start_date, end_date]

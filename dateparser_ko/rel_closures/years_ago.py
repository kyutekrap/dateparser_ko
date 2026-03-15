from dateutil.relativedelta import relativedelta
from dateparser_ko.types import DateObject
from datetime import datetime, timezone, date
from typing import List


def years_ago(context: str, temp_date: DateObject) -> List[DateObject]:
    ret: List[DateObject] = []

    today = datetime.now(tz=timezone.utc)
    end_date = date(
        temp_date["y"] if temp_date["y"] > 0 else today.year,
        temp_date["m"] if temp_date["m"] > 0 else 1,
        temp_date["d"] if temp_date["d"] > 0 else 1,
    )
    start_date = end_date - relativedelta(years=int(context))
    ret.append(DateObject(y=start_date.year, m=start_date.month, d=start_date.day))

    if temp_date["d"] == 0:
        end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
        ret.append(DateObject(y=end_date.year, m=end_date.month, d=end_date.day))

    return ret

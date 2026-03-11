from dateutil.relativedelta import relativedelta
from datetime import datetime, timezone
from dateparser_ko.types import DateObject


def last_month(context: str, temp_date: DateObject) -> DateObject:
    temp = (datetime.now(tz=timezone.utc) - relativedelta(months=1))

    date_obj = DateObject(y=temp.year, m=temp.month, d=0)
    return date_obj

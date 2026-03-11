from dateparser_ko.types import DateObject


def year(context: str, temp_date: DateObject) -> DateObject:
    return DateObject(y=int(context), m=0, d=0)

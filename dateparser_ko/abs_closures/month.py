from dateparser_ko.types import DateObject


def month(context: str, temp_date: DateObject) -> DateObject:
    return DateObject(y=temp_date["y"], m=int(context), d=0)

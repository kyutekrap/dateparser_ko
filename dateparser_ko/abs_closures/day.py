from dateparser_ko.types import DateObject


def day(context: str, temp_date: DateObject) -> DateObject:
    return DateObject(y=temp_date["y"], m=temp_date["m"], d=int(context))

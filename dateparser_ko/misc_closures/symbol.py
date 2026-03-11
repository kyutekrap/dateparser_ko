from dateparser_ko.types import DateObject


def symbol(context: str) -> DateObject:
    custom_date = DateObject(y=0, m=0, d=0)

    sep = next((c for c in context if not c.isdigit()), None)
    numbers = context.split(sep)
    max_len = 3

    year_i = 0
    while year_i < max_len:
        if len(numbers[year_i]) == 4:
            custom_date["y"] = int(numbers[year_i])
            break

        year_i += 1

    month_i = 0
    while month_i < max_len:
        if month_i == year_i:
            month_i += 1
            continue

        temp = int(numbers[month_i])
        if temp < 13:
            custom_date["m"] = temp
            break

        month_i += 1

    day_i = 0
    while day_i < max_len:
        if day_i == year_i or day_i == month_i:
            day_i += 1
            continue

        custom_date["d"] = int(numbers[day_i])
        break

    return custom_date

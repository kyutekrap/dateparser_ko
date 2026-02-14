import re
from typing import TypedDict, List
from datetime import datetime, timezone, date
from dateutil.relativedelta import relativedelta
import copy

# ===== REGEX EXPRESSIONS (START)

RE_IS_DIGIT = r'^-?\d+$'
RE_IS_BLANK = r'\s+'
RE_HAS_DIGIT = r'\d'

# ===== REGEX EXPRESSIONS (END)


# ===== KEYWORDS (START)

KW_YEAR = "년"
KW_MONTH = "월"
KW_DAY = "일"
KW_LAST_YEAR = "작년"
KW_LAST_YEAR2 = "지난 해"
KW_LAST_LAST_YEAR = "재작년"
KW_QUARTER = "분기"
KW_MONTHS = "개월"
KW_YEARS = "개년"
KW_YEARS2 = "년치"
KW_FIRST_HALF = "상반기"
KW_LAST_HALF = "하반기"
KW_THIS_YEAR = "올해"
KW_THIS_YEAR2 = "이번 연도"
KW_THIS_MONTH = "이번 달"
KW_LAST_MONTH = "지난 달"
KW_LAST_QUARTER = "지난 분기"
KW_PRESENT = "현재"
KW_TODAY = "오늘"
KW_TODAY2 = "금일"
KW_TODAY3 = "당일"
KW_THIS_MONTH2 = "금월"
KW_THIS_MONTH3 = "당월"
KW_LAST_MONTH2 = "전월"

ABSOLUTE_WORDS = [KW_YEAR, KW_MONTH, KW_DAY]
RELATIVE_WORDS = [KW_LAST_YEAR, KW_LAST_LAST_YEAR, KW_QUARTER, KW_MONTHS, KW_YEARS, KW_FIRST_HALF, KW_LAST_HALF,
    KW_THIS_YEAR, KW_THIS_YEAR2, KW_THIS_MONTH, KW_LAST_YEAR2, KW_LAST_MONTH, KW_LAST_QUARTER, KW_PRESENT, KW_YEARS2,
    KW_TODAY, KW_TODAY2, KW_TODAY3, KW_THIS_MONTH2, KW_THIS_MONTH3, KW_LAST_MONTH2]

# ===== KEYWORDS (END)


# ===== STOPWORDS (START)

NUMB_WORDS = ["일", "이", "삼", "사", "오", "육", "칠", "팔", "구", "십", "백", "천"]
DATE_WORDS = sorted(ABSOLUTE_WORDS + RELATIVE_WORDS, key=len, reverse=True)

# ===== STOPWORDS (END)


# ===== TAGS (START)

TAG_DW = "DW"

# ===== TAGS (END)


# ===== MODELS (START)


class DateObject(TypedDict):
    year: int
    month: int
    day: int


class DateRange(TypedDict):
    from_date: DateObject
    to_date: DateObject


# ===== MODELS (END)


def parse(text: str) -> List[DateRange]:
    
    # 0. Local variables

    old_string = text
    new_string = ""
    new_string_list: List[str] = []
    date_objects: List[DateRange] = []
    
    # 1. Wrap DATE_WORDS with Tags

    pattern = "|".join(map(re.escape, DATE_WORDS))
    old_string = re.sub(
        pattern,
        lambda m: f"<{TAG_DW}>{m.group(0)}</{TAG_DW}>",
        old_string
    )
    
    # 2. Replace irrelevant words with whitespace

    ignore = False
    for j, c in enumerate(list(old_string)):
        if ignore:
            if old_string[j:j + 5] == f"</{TAG_DW}>":
                new_string += f"</{TAG_DW}>"
                ignore = False
                continue

            new_string += c
            continue

        if old_string[j:j + 4] == f"<{TAG_DW}>":
            new_string += c
            ignore = True
            continue

        if bool(re.match(RE_IS_DIGIT, c)):
            new_string += c

        else:
            if c in NUMB_WORDS:
                new_string += c
            else:
                new_string += " "

    # 3. Replace NUMB_WORDS with real numbers

    ignore = False
    for word in re.findall(rf"</?{TAG_DW}>|[^<>]+?(?=<|$)", new_string):
        word = word.strip()

        if word == f"</{TAG_DW}>":
            ignore = False
            continue

        if ignore:
            new_string_list.append(word)
            continue

        if word == f"<{TAG_DW}>":
            ignore = True
            continue

        if bool(re.search(RE_HAS_DIGIT, word)):
            new_string_list.append(word)
            continue

        if len([c for c in list(word) if c not in NUMB_WORDS]) > 0:
            continue

        real_number = ""
        for j, c in enumerate(list(word)):
            index = NUMB_WORDS.index(c) + 1
            if index == 10:
                if real_number == "":
                    real_number += "10"
                else:
                    if len(word[j + 1:]) == 0:
                        real_number += "0"
            elif index == 11:
                if real_number == "":
                    real_number += "100"
                else:
                    if len(word[j + 1:]) == 0:
                        real_number += "00"
            elif index == 12:
                if real_number == "":
                    real_number += "1000"
                else:
                    if len(word[j + 1:]) == 0:
                        real_number += "000"
            else:
                real_number += str(index)

        if real_number != "":
            new_string_list.append(real_number)
            
    # 4. Join new_string_list into DateObjects

    from_date_object = DateObject(year=0, month=0, day=0)
    to_date_object = DateObject(year=0, month=0, day=0)
    date_range = DateRange(from_date=from_date_object, to_date=to_date_object)

    def add_date_range():
        if (
            from_date_object["year"] != 0
            and from_date_object["month"] != 0
            and from_date_object["day"] != 0
            and to_date_object["year"] != 0
            and to_date_object["month"] != 0
            and to_date_object["day"] != 0
        ):
            date_objects.append(copy.deepcopy(date_range))
            from_date_object["year"] = 0
            from_date_object["month"] = 0
            from_date_object["day"] = 0
            to_date_object["year"] = 0
            to_date_object["month"] = 0
            to_date_object["day"] = 0

    def clean_up_date_range():
        if (
            from_date_object["year"] == 0
            and from_date_object["month"] == 0
            and from_date_object["day"] == 0
            and to_date_object["year"] == 0
            and to_date_object["month"] == 0
            and to_date_object["day"] == 0
        ):
            return

        today = datetime.now(tz=timezone.utc).date()
        from_date_object.update({
            "year": from_date_object["year"] if from_date_object["year"] > 0 else today.year,
            "month": from_date_object["month"] if from_date_object["month"] > 0 else 1,
            "day": from_date_object["day"] if from_date_object["day"] > 0 else 1,
        })

        to_date_object["year"] = to_date_object["year"] if to_date_object["year"] > 0 else from_date_object["year"]
        if to_date_object["month"] == 0:
            if from_date_object["year"] == today.year:
                to_date_object["month"] = today.month
            else:
                to_date_object["month"] = 12
        if to_date_object["day"] == 0:
            if from_date_object["year"] == today.year:
                to_date_object["day"] = today.day
            else:
                to_date = date(to_date_object["year"], to_date_object["month"], 1) + relativedelta(months=1) - relativedelta(days=1)
                to_date_object["day"] = to_date.day

        date_objects.append(date_range)

    def from_absolute_words(_number: int, _word: str | None):
        if _word == KW_YEAR:
            if _number > 1000:
                if from_date_object["year"] == 0:
                    from_date_object["year"] = _number
                elif to_date_object["year"] == 0:
                    to_date_object["year"] = _number
                else:
                    clean_up_date_range()
                    from_date_object["year"] = _number
            else:
                if from_date_object["year"] == 0:
                    from_date_object["year"] = datetime.now(tz=timezone.utc).year - _number
                elif to_date_object["year"] == 0:
                    to_date_object["year"] = from_date_object["year"] + _number
                else:
                    clean_up_date_range()
                    from_date_object["year"] = datetime.now(tz=timezone.utc).year - _number

        elif _word == KW_MONTH:
            if from_date_object["month"] == 0:
                from_date_object["month"] = _number
            elif to_date_object["month"] == 0:
                to_date_object.update({
                    "year": to_date_object["year"] if to_date_object["year"] > 0 else from_date_object["year"],
                    "month": _number
                })
            else:
                clean_up_date_range()
                from_date_object["month"] = _number

        elif _word == KW_DAY:
            if from_date_object["day"] == 0:
                from_date_object["day"] = _number
            elif to_date_object["day"] == 0:
                to_date_object.update({
                    "year": to_date_object["year"] if to_date_object["year"] > 0 else from_date_object["year"],
                    "month": to_date_object["month"] if to_date_object["month"] > 0 else from_date_object["month"],
                    "day": _number
                })
            else:
                clean_up_date_range()
                from_date_object["day"] = _number

        else:
            if _number > 1000:
                if from_date_object["year"] == 0:
                    from_date_object["year"] = _number
                elif to_date_object["year"] == 0:
                    to_date_object["year"] = _number
                else:
                    clean_up_date_range()
                    from_date_object["year"] = _number
            else:
                if from_date_object["month"] == 0:
                    from_date_object["month"] = _number
                elif from_date_object["day"] == 0:
                    from_date_object["day"] = _number
                elif to_date_object["month"] == 0:
                    to_date_object["month"] = _number
                elif to_date_object["day"] == 0:
                    to_date_object["day"] = _number
                else:
                    clean_up_date_range()
                    from_date_object["month"] = _number

        add_date_range()

    def from_relative_words(_number: int, _word: str):
        if _word == KW_LAST_YEAR or _word == KW_LAST_YEAR2:
            if from_date_object["year"] == 0:
                from_date_object["year"] = datetime.now(tz=timezone.utc).year - 1
            elif to_date_object["year"] == 0:
                to_date_object["year"] = datetime.now(tz=timezone.utc).year - 1
            else:
                clean_up_date_range()
                from_date_object["year"] = datetime.now(tz=timezone.utc).year - 1

        elif _word == KW_LAST_MONTH or _word == KW_LAST_MONTH2:
            original_date = datetime.now(tz=timezone.utc)
            relative_date = original_date - relativedelta(months=1)
            if from_date_object["year"] == 0:
                from_date_object.update({
                    "year": relative_date.year,
                    "month": relative_date.month
                })
            elif to_date_object["year"] == 0:
                to_date_object.update({
                    "year": relative_date.year,
                    "month": relative_date.month
                })
            else:
                clean_up_date_range()
                from_date_object.update({
                    "year": relative_date.year,
                    "month": relative_date.month
                })

        elif _word == KW_LAST_LAST_YEAR:
            if from_date_object["year"] == 0:
                from_date_object["year"] = datetime.now(tz=timezone.utc).year - 2
            elif to_date_object["year"] == 0:
                to_date_object["year"] = datetime.now(tz=timezone.utc).year - 2
            else:
                clean_up_date_range()
                from_date_object["year"] = datetime.now(tz=timezone.utc).year - 2

        elif _word == KW_QUARTER:
            if not (
                from_date_object["month"] == 0
                and to_date_object["month"] == 0
            ):
                clean_up_date_range()

            if _number == 1:
                from_date_object.update({
                    "month": 1,
                    "day": 1
                })
                to_date_object.update({
                    "year": from_date_object["year"],
                    "month": 3,
                    "day": 31
                })
            elif _number == 2:
                from_date_object.update({
                    "month": 4,
                    "day": 1
                })
                to_date_object.update({
                    "year": from_date_object["year"],
                    "month": 6,
                    "day": 30
                })
            elif _number == 3:
                from_date_object.update({
                    "month": 7,
                    "day": 1
                })
                to_date_object.update({
                    "year": from_date_object["year"],
                    "month": 9,
                    "day": 30
                })
            elif _number == 4:
                from_date_object.update({
                    "month": 10,
                    "day": 1
                })
                to_date_object.update({
                    "year": from_date_object["year"],
                    "month": 12,
                    "day": 31
                })

        elif _word == KW_LAST_QUARTER:
            if not (
                from_date_object["month"] == 0
                and to_date_object["month"] == 0
            ):
                clean_up_date_range()

            original_date = datetime.now(tz=timezone.utc)
            relative_date = original_date - relativedelta(months=3)
            quarter = (relative_date.month - 1) // 3 + 1
            if quarter == 1:
                from_date_object.update({
                    "year": relative_date.year,
                    "month": 1,
                    "day": 1
                })
                to_date_object.update({
                    "year": relative_date.year,
                    "month": 3,
                    "day": 31
                })
            elif quarter == 2:
                from_date_object.update({
                    "year": relative_date.year,
                    "month": 4,
                    "day": 1
                })
                to_date_object.update({
                    "year": relative_date.year,
                    "month": 6,
                    "day": 30
                })
            elif quarter == 3:
                from_date_object.update({
                    "year": relative_date.year,
                    "month": 7,
                    "day": 1
                })
                to_date_object.update({
                    "year": relative_date.year,
                    "month": 9,
                    "day": 30
                })
            elif quarter == 4:
                from_date_object.update({
                    "year": relative_date.year,
                    "month": 10,
                    "day": 1
                })
                to_date_object.update({
                    "year": relative_date.year,
                    "month": 12,
                    "day": 31
                })

        elif _word == KW_MONTHS:
            if from_date_object["year"] == 0:
                if from_date_object["month"] == 0:
                    today_date = datetime.now(tz=timezone.utc)
                    relative_date = today_date - relativedelta(months=_number)
                    from_date_object.update({
                        "year": relative_date.year,
                        "month": relative_date.month,
                        "day": relative_date.day
                    })
                    to_date_object.update({
                        "year": today_date.year,
                        "month": today_date.month,
                        "day": today_date.day
                    })
                else:
                    original_date = date(
                        datetime.now(tz=timezone.utc).year,
                        from_date_object["month"],
                        from_date_object["day"] if from_date_object["day"] > 0 else 1
                    )
                    relative_date = original_date + relativedelta(months=_number)
                    from_date_object.update({
                        "year": original_date.year,
                        "day": original_date.day
                    })
                    to_date_object.update({
                        "year": relative_date.year,
                        "month": relative_date.month,
                        "day": relative_date.day
                    })
            elif to_date_object["year"] == 0:
                original_date = date(
                    from_date_object["year"],
                    from_date_object["month"] if from_date_object["month"] > 0 else 1,
                    from_date_object["day"] if from_date_object["day"] > 0 else 1
                )
                relative_date = original_date + relativedelta(months=_number)
                from_date_object.update({
                    "year": original_date.year,
                    "month": original_date.month,
                    "day": original_date.day
                })
                to_date_object.update({
                    "year": relative_date.year,
                    "month": relative_date.month,
                    "day": relative_date.day
                })
            else:
                clean_up_date_range()
                if from_date_object["month"] == 0:
                    today_date = datetime.now(tz=timezone.utc)
                    relative_date = today_date - relativedelta(months=_number)
                    from_date_object.update({
                        "year": relative_date.year,
                        "month": relative_date.month,
                        "day": relative_date.day
                    })
                    to_date_object.update({
                        "year": today_date.year,
                        "month": today_date.month,
                        "day": today_date.day
                    })
                else:
                    original_date = date(
                        datetime.now(tz=timezone.utc).year,
                        from_date_object["month"],
                        from_date_object["day"] if from_date_object["day"] > 0 else 1
                    )
                    relative_date = original_date + relativedelta(months=_number)
                    from_date_object.update({
                        "year": original_date.year,
                        "day": original_date.day
                    })
                    to_date_object.update({
                        "year": relative_date.year,
                        "month": relative_date.month,
                        "day": relative_date.day
                    })

        elif _word == KW_FIRST_HALF:
            if not (
                from_date_object["month"] == 0
                and to_date_object["month"] == 0
            ):
                clean_up_date_range()

            from_date_object.update({
                "month": 1,
                "day": 1
            })
            to_date_object.update({
                "year": from_date_object["year"],
                "month": 6,
                "day": 30
            })

        elif _word == KW_LAST_HALF:
            if not (
                from_date_object["month"] == 0
                and to_date_object["month"] == 0
            ):
                clean_up_date_range()

            from_date_object.update({
                "month": 7,
                "day": 1
            })
            to_date_object.update({
                "year": from_date_object["year"],
                "month": 12,
                "day": 31
            })

        elif _word == KW_YEARS or _word == KW_YEARS2:
            if from_date_object["year"] == 0:
                original_date = date(
                    datetime.now(tz=timezone.utc).year,
                    from_date_object["month"] if from_date_object["month"] > 0 else 1,
                    from_date_object["day"] if from_date_object["day"] > 0 else 1
                )
                relative_date = original_date - relativedelta(years=_number)
                from_date_object.update({
                    "year": relative_date.year,
                    "month": relative_date.month,
                    "day": relative_date.day
                })
                to_date_object.update({
                    "year": original_date.year,
                    "month": original_date.month,
                    "day": original_date.day
                })
            elif to_date_object["year"] == 0:
                original_date = date(
                    from_date_object["year"],
                    from_date_object["month"] if from_date_object["month"] > 0 else 1,
                    from_date_object["day"] if from_date_object["day"] > 0 else 1
                )
                relative_date = original_date + relativedelta(years=_number)
                from_date_object.update({
                    "month": original_date.month,
                    "day": original_date.day
                })
                to_date_object.update({
                    "year": relative_date.year,
                    "month": relative_date.month,
                    "day": relative_date.day
                })
            else:
                clean_up_date_range()
                original_date = date(
                    datetime.now(tz=timezone.utc).year,
                    from_date_object["month"] if from_date_object["month"] > 0 else 1,
                    from_date_object["day"] if from_date_object["day"] > 0 else 1
                )
                relative_date = original_date - relativedelta(years=_number)
                from_date_object.update({
                    "year": relative_date.year,
                    "month": relative_date.month,
                    "day": relative_date.day
                })
                to_date_object.update({
                    "year": original_date.year,
                    "month": original_date.month,
                    "day": original_date.day
                })

        elif _word == KW_THIS_YEAR or _word == KW_THIS_YEAR2:
            if from_date_object["year"] == 0:
                from_date_object["year"] = datetime.now(tz=timezone.utc).year
            elif to_date_object["year"] == 0:
                to_date_object["year"] = datetime.now(tz=timezone.utc).year
            else:
                clean_up_date_range()
                from_date_object["year"] = datetime.now(tz=timezone.utc).year

        elif _word == KW_THIS_MONTH or _word == KW_THIS_MONTH2 or _word == KW_THIS_MONTH3:
            if from_date_object["month"] == 0:
                from_date_object["month"] = datetime.now(tz=timezone.utc).month
            elif to_date_object["month"] == 0:
                to_date_object["month"] = datetime.now(tz=timezone.utc).month
            else:
                clean_up_date_range()
                from_date_object["month"] = datetime.now(tz=timezone.utc).month

        elif _word == KW_PRESENT or _word == KW_TODAY or _word == KW_TODAY2 or _word == KW_TODAY3:
            original_date = datetime.now(tz=timezone.utc)
            if from_date_object["year"] == 0:
                from_date_object.update({
                    "year": original_date.year,
                    "month": original_date.month,
                    "day": original_date.day
                })
            elif to_date_object["year"] == 0:
                to_date_object.update({
                    "year": original_date.year,
                    "month": original_date.month,
                    "day": original_date.day
                })
            else:
                clean_up_date_range()
                from_date_object.update({
                    "year": original_date.year,
                    "month": original_date.month,
                    "day": original_date.day
                })

        add_date_range()

    number = 0
    for j, token in enumerate(new_string_list):
        if bool(re.match(RE_IS_DIGIT, token)):
            if number != 0:
                from_absolute_words(number, None)
            number = int(token)
        elif token in ABSOLUTE_WORDS:
            word = ABSOLUTE_WORDS[ABSOLUTE_WORDS.index(token)]
            if number != 0:
                from_absolute_words(number, word)
                number = 0
        elif token in RELATIVE_WORDS:
            word = RELATIVE_WORDS[RELATIVE_WORDS.index(token)]
            from_relative_words(number, word)

    # 5. Clean-up latest date_range

    clean_up_date_range()

    return date_objects

from .first_half import first_half
from .last_half import last_half
from .last_last_year import last_last_year
from .last_month import last_month
from .last_quarter import last_quarter
from .last_year import last_year
from .quarter import quarter
from .this_month import this_month
from .this_year import this_year
from .today import today
from .months import months
from dateparser_ko.keywords import KW_LAST_YEAR, KW_QUARTER, KW_THIS_YEAR, KW_THIS_MONTH, KW_LAST_MONTH, \
    KW_LAST_QUARTER, KW_LAST_YEAR2, KW_LAST_LAST_YEAR, KW_FIRST_HALF, KW_LAST_HALF, KW_THIS_YEAR2, \
    KW_TODAY, KW_TODAY2, KW_TODAY3, KW_THIS_MONTH2, KW_THIS_MONTH3, KW_LAST_MONTH2, KW_MONTHS

mapping = {
    KW_LAST_YEAR: last_year,
    KW_LAST_YEAR2: last_year,
    KW_LAST_LAST_YEAR: last_last_year,
    KW_QUARTER: quarter,
    KW_FIRST_HALF: first_half,
    KW_LAST_HALF: last_half,
    KW_THIS_YEAR: this_year,
    KW_THIS_YEAR2: this_year,
    KW_THIS_MONTH: this_month,
    KW_LAST_MONTH: last_month,
    KW_LAST_QUARTER: last_quarter,
    KW_TODAY: today,
    KW_TODAY2: today,
    KW_TODAY3: today,
    KW_THIS_MONTH2: this_month,
    KW_THIS_MONTH3: this_month,
    KW_LAST_MONTH2: last_month,
    KW_MONTHS: months
}
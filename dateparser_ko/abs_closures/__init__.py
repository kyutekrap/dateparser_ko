from .day import day
from .month import month
from .year import year
from dateparser_ko.keywords import KW_YEAR, KW_MONTH, KW_DAY

mapping = {
    KW_YEAR: year,
    KW_MONTH: month,
    KW_DAY: day
}
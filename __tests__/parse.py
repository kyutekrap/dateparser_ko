from dateparser_ko import parse


def pretty_print(example: str):
    result = parse(example)
    print(f"Example: {example}\nResult: {result}")


pretty_print("2024년 매출")
pretty_print("2024년 1분기 매출")
pretty_print("3개월치 매출")
pretty_print("2024년 1월부터 삼십개월 매출")
pretty_print("2024년 3월~6월 매출")
pretty_print("작년 4분기 매출")
pretty_print("4년 전 매출")
pretty_print("현재 매출")
pretty_print("올해 매출")
pretty_print("올해 상반기 매출")
pretty_print("올해 하반기 매출")
pretty_print("2024년도 상위 10개 상품의 매출")
pretty_print("2020년부터 삼개년 매출")
pretty_print("지난 3개년 매출")
pretty_print("지난 해 매출")
pretty_print("지난 분기 매출")
pretty_print("이번 연도 매출")
pretty_print("지난 달 1일부터 10일 간의 매출")
pretty_print("1년치 매출")
pretty_print("이 회사의 이번 달 매출")

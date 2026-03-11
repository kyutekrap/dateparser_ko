from dateparser_ko import parse


def pretty_print(example: str):
    result = parse(example)
    print(f"Example: {example}\nFound Dates: {result["found_dates"]}\nUsed Tokens: {result["used_tokens"]}\nCleaned: {result["cleaned"]}")
    print("=================================================")


# pretty_print("2024년 매출")
# pretty_print("2024년 1분기 매출")
# pretty_print("2024년 3월~6월 매출")
# pretty_print("올해 매출")
# pretty_print("2024년 10월 상위 10개 상품의 매출")
# pretty_print("2024년 6월 15일 실적 보고")
# pretty_print("2024-06-15 실적 보고")
# pretty_print("지난 해 매출")
# pretty_print("지난 분기 매출")
# pretty_print("이번 연도 매출")
# pretty_print("이 회사의 이번 달 매출")
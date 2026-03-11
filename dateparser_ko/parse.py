from .keywords import NUMB_WORDS, ABS_WORDS, REL_WORDS
from .stopwords import STOPWORDS
from .symbols import ALL_SYMBOLS
from .types import ParseResult, DateObject
from .tags import AW, NW, PAD, SYMB, YEAR, RW, TERM
from .patterns import RE_IS_DIGIT, RE_HAS_DIGIT_AND_CHAR
from .abs_closures import mapping as abs_mapping
from .misc_closures import mapping as misc_mapping
from .rel_closures import mapping as rel_mapping
import re


def remove_stopwords(text: str) -> str:
    cleaned = []
    for token in text.split(" "):
        ignore = False
        for stopword in STOPWORDS:
            if token.endswith(stopword):
                cleaned.append(token[:-len(stopword)])
                ignore = True
                continue

        if not ignore:
            cleaned.append(token)

    return " ".join(cleaned)


def parse_year(text: str) -> str:
    parsed = ""

    tokens = list(text)
    tokens_len = len(tokens)

    skip_count = 0
    for i, c in enumerate(tokens):
        if skip_count > 0:
            skip_count -= 1
            continue

        if bool(re.match(RE_IS_DIGIT, c)):
            if i + 3 >= tokens_len:
                pass

            if (
                    bool(re.match(RE_IS_DIGIT, tokens[i + 1]))
                    and
                    bool(re.match(RE_IS_DIGIT, tokens[i + 2]))
                    and
                    bool(re.match(RE_IS_DIGIT, tokens[i + 3]))
                    and
                    (i + 4 == tokens_len or not bool(re.match(RE_IS_DIGIT, tokens[i + 4])))
            ):
                parsed += f"<{YEAR}>{c + tokens[i + 1] + tokens[i + 2] + tokens[i + 3]}</{YEAR}>"
                skip_count += 3
                continue

        parsed += c

    return parsed


def wrap_terms(text: str) -> str:
    parsed = ""

    tokens = list(text)
    skip_count = 0
    for i, c in enumerate(tokens):
        if skip_count > 0:
            skip_count -= 1
            continue

        chars = []
        for keyword in REL_WORDS:
            for j, ch in enumerate(tokens[i:]):
                if "".join(chars).replace(" ", "") == keyword and ch == " ":
                    break

                if len(chars) > len(list(keyword)):
                    break

                chars.append(ch)

            if "".join(chars).replace(" ", "") == keyword:
                break
            else:
                chars.clear()

        char_len = len(chars)
        if char_len > 0:
            parsed += f"<{TERM}>{"".join(chars)}</{TERM}>"
            skip_count = char_len - 1
            continue

        parsed += c

    return parsed


def tag_chars(text: str) -> list:
    tags = []

    skip_count = 0
    tokens = list(text)
    tokens_len = len(tokens)

    for i, c in enumerate(tokens):
        if skip_count > 0:
            skip_count -= 1
            continue

        if c == " ":
            tags.append(PAD)
            continue

        if i + 17 < tokens_len:
            if "".join(tokens[i:i + 6]) == f"<{YEAR}>" and "".join(tokens[i + 10:i + 17]) == f"</{YEAR}>":
                tags.extend([YEAR for _ in range(6)])
                tags.extend([NW for _ in range(4)])
                tags.extend([YEAR for _ in range(7)])
                skip_count = 16
                continue

        if i + 12 < tokens_len:
            if "".join(tokens[i:i + 6]) == f"<{TERM}>":
                start_pos = i + 6
                end_pos = i + 6 + 7
                while True:
                    if end_pos < tokens_len:
                        if "".join(tokens[start_pos:end_pos]) == f"</{TERM}>":
                            tags.extend([TERM for _ in range(6)])
                            tags.extend([RW for _ in range(start_pos - (i + 6))])
                            tags.extend([TERM for _ in range(7)])
                            skip_count = end_pos - i - 1
                            break

                    else:
                        break

                    start_pos += 1
                    end_pos += 1

                if skip_count > 0:
                    continue

        next_c = "" if i + 1 >= tokens_len else tokens[i + 1]
        next_2_c = "" if i + 2 >= tokens_len else tokens[i + 2]
        prev_t = None if i - 1 < 0 else tags[i - 1]
        prev_2_t = None if i - 2 < 0 else tags[i - 2]

        if (
                c in ABS_WORDS
                and
                (prev_t == NW or prev_t == YEAR)
        ):
            tags.append(AW)

        elif (
                (bool(re.match(RE_IS_DIGIT, c)) or c in NUMB_WORDS)
                and
                (prev_t == NW or prev_t == PAD or prev_t is None or prev_t == SYMB)
                and
                (bool(re.match(RE_IS_DIGIT,
                               next_c)) or next_c in NUMB_WORDS or next_c in ABS_WORDS or next_c in ALL_SYMBOLS or next_c == " "
                 or (i + 7 < tokens_len and "".join(tokens[i + 1:i + 7]) == f"<{TERM}>"))
                and
                (
                        prev_2_t is None or prev_2_t == SYMB or prev_2_t == NW or prev_2_t == AW or prev_2_t == PAD or next_2_c in ALL_SYMBOLS)
        ):
            tags.append(NW)

        elif (
                c in ALL_SYMBOLS
                and
                (prev_t == NW or prev_t == YEAR)
                and
                bool(re.match(RE_IS_DIGIT, next_c))
        ):
            tags.append(SYMB)

        else:
            tags.append(None)

    return tags


def generate_tokens(tags: list, tokens: list) -> list:
    useful_tokens = []

    counter = 0
    for i, t in enumerate(tags):
        if t is None or t == PAD:
            counter += 1
            continue

        if t == YEAR or t == TERM:
            continue

        useful_tokens.append((tokens[i], t, counter))
        counter += 1

    return useful_tokens


def normalize_chars(useful_tokens: list) -> list:
    normal_tokens = []

    useful_tokens_len = len(useful_tokens)
    for idx, token in enumerate(useful_tokens):
        c = token[0]
        t = token[1]
        p = token[2]

        prev_token = (None, None, None) if idx - 1 < 0 else useful_tokens[idx - 1]
        prev_t = prev_token[1]

        next_token = (None, None, None) if idx + 1 >= useful_tokens_len else useful_tokens[idx + 1]
        next_t = next_token[1]

        if t == NW and not bool(re.match(RE_IS_DIGIT, c)):
            index = NUMB_WORDS.index(c) + 1
            if index == 10:
                if prev_t != NW:
                    c = "10"
                elif next_t != NW:
                    c = "0"
                else:
                    c = ""
            elif index == 11:
                if prev_t != NW:
                    c = "100"
                elif next_t != NW:
                    c = "00"
                else:
                    c = ""
            elif index == 12:
                if prev_t != NW:
                    c = "1000"
                elif next_t != NW:
                    c = "000"
                else:
                    c = ""
            else:
                c = str(index)

        normal_tokens.append((c, t, p))

    return normal_tokens


def parse(text: str) -> ParseResult:
    response: ParseResult = {
        "found_dates": [],
        "used_tokens": [],
        "cleaned": ""
    }

    text = " ".join(text.split())
    text = remove_stopwords(text)

    response["cleaned"] = text

    text = parse_year(text)
    text = wrap_terms(text)
    tokens = list(text)
    tags = tag_chars(text)
    useful_tokens = generate_tokens(tags, tokens)

    response["used_tokens"] = useful_tokens

    normal_tokens = normalize_chars(useful_tokens)

    dates = []

    context = ""
    temp_date = DateObject(y=0, m=0, d=0)
    tokens_len = len(normal_tokens)
    skip_counter = 0
    for idx, token in enumerate(normal_tokens):
        if skip_counter > 0:
            skip_counter -= 1
            continue

        c = token[0]
        t = token[1]
        p = token[2]

        if t == NW:
            context += c
            if re.search(RE_HAS_DIGIT_AND_CHAR, context):
                if idx + 1 < tokens_len:
                    if normal_tokens[idx+1][1] != SYMB and normal_tokens[idx+1][1] != NW:
                        dates.append(misc_mapping[SYMB](context))
                        context = ""
                else:
                    dates.append(misc_mapping[SYMB](context))
                    context = ""

        elif t == AW:
            temp = abs_mapping[c](context, temp_date)
            if (0 < temp_date["y"] != temp["y"] > 0) or (0 < temp_date["m"] != temp["m"] > 0) or (0 < temp_date["d"] != temp["d"] > 0):
                dates.append(temp_date)
                temp_date = temp
            else:
                temp_date["y"] = max(temp_date["y"], temp["y"])
                temp_date["m"] = max(temp_date["m"], temp["m"])
                temp_date["d"] = max(temp_date["d"], temp["d"])
                if temp_date["y"] > 0 and temp_date["m"] > 0 and temp_date["d"] > 0:
                    dates.append(temp_date)
                    temp_date = DateObject(y=0, m=0, d=0)
            context = ""

        elif t == RW:
            current = c
            counter = idx + 1
            while counter < tokens_len:
                next_token = normal_tokens[counter]
                if next_token[1] == RW:
                    current += next_token[0]
                else:
                    break
                counter += 1
            skip_counter = counter - idx

            temp = rel_mapping[current.replace(" ", "")](context, temp_date)
            if isinstance(temp, list):
                for _temp in temp:
                    if _temp["y"] > 0 and _temp["m"] > 0 and _temp["d"] > 0:
                        dates.append(_temp)
                        temp_date = DateObject(y=0, m=0, d=0)
                    else:
                        temp_date["y"] = max(temp_date["y"], _temp["y"])
                        temp_date["m"] = max(temp_date["m"], _temp["m"])
                        temp_date["d"] = max(temp_date["d"], _temp["d"])
                        if temp_date["y"] > 0 and temp_date["m"] > 0 and temp_date["d"] > 0:
                            dates.append(temp_date)
                            temp_date = DateObject(y=0, m=0, d=0)
            else:
                if temp["y"] > 0 and temp["m"] > 0 and temp["d"] > 0:
                    dates.append(temp)
                    temp_date = DateObject(y=0, m=0, d=0)
                else:
                    temp_date["y"] = max(temp_date["y"], temp["y"])
                    temp_date["m"] = max(temp_date["m"], temp["m"])
                    temp_date["d"] = max(temp_date["d"], temp["d"])
                    if temp_date["y"] > 0 and temp_date["m"] > 0 and temp_date["d"] > 0:
                        dates.append(temp_date)
                        temp_date = DateObject(y=0, m=0, d=0)
            context = ""

        elif t == SYMB:
            context += c

    if temp_date["y"] > 0 or temp_date["m"] > 0 or temp_date["d"] > 0:
        dates.append(temp_date)

    response["found_dates"] = dates

    return response

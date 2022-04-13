def break_string_to_lines(some_string, max_line_char_limit=80):
    split_string = some_string.split(" ")
    full_string = ""
    line = ""
    current_char_amount = 0
    for word in split_string:
        line += f" {word}"
        current_char_amount += len(word) + 1
        if current_char_amount > max_line_char_limit:
            current_char_amount = 0
            full_string += f"{line}\n"
            line = ""

    return full_string

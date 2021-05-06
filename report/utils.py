def reverse_date_format(date_string):
    date_splitted = date_string.split("-")
    date_reversed = list(reversed(date_splitted))
    reversed_date_string = "-".join(date_reversed)
    return reversed_date_string

from datetime import datetime


def get_age(birth_date):
    today = datetime.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def get_formatted_date(birth_date):
    date = birth_date.strftime("%d.%m.%Y")
    return date


def get_date_from_string(str_date):
    return datetime.strptime(str_date, "%Y-%m-%d").date()

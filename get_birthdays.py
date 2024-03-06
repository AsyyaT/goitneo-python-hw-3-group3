from datetime import datetime, timedelta
from collections import defaultdict


def get_birthdays_per_week(users):
    weekday_to_day_name = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday"}
    birthday_to_people_names = defaultdict(list)
    current_date = datetime.today().date()
    week_ahead = current_date + timedelta(days=7)

    for user in users:
        birthday = user["birthday"].date()
        name = user["name"]
        birthday_this_year = birthday.replace(year=current_date.year)

        if birthday_this_year < current_date:
            birthday_this_year = birthday.replace(year=current_date.year + 1)

        weekday = birthday_this_year.weekday()

        if current_date <= birthday_this_year <= week_ahead:
            if weekday in (5, 6):
                birthday_to_people_names[weekday_to_day_name.get(0)].append(name)
            else:
                birthday_to_people_names[weekday_to_day_name.get(weekday)].append(name)

    birthdays = []
    for day, names in birthday_to_people_names.items():
        names = ', '.join(names)
        birthdays.append(f'{day}: {names}')

    return birthdays

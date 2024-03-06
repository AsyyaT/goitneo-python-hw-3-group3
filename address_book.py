from collections import UserDict
from datetime import datetime

from get_birthdays import get_birthdays_per_week


class PhoneException(Exception):
    pass


class DateFormatException(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Birthday(Field):
    def validate_date_format(self):
        try:
            datetime.strptime(self.value, "%d.%m.%Y").strftime("%d.%m.%Y")
        except ValueError:
            raise DateFormatException


class Phone(Field):
    def validate_phone(self):
        if not (len(self.value) == 10 and str(self.value).isdigit()):
            raise PhoneException


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone):
        p = Phone(phone)
        p.validate_phone()
        self.phones.append(p)

    def remove_phone(self, phone):
        for el in self.phones:
            if el.value == phone:
                self.phones.remove(el)

    def edit_phone(self, old_number, new_number):
        if old_number in [p.value for p in self.phones]:
            self.remove_phone(old_number)
            self.add_phone(new_number)

    def find_phone(self, phone):
        if phone in [p.value for p in self.phones]:
            return phone
        return "Number not found"

    def add_birthday(self, birthday_date):
        birthday = Birthday(birthday_date)
        birthday.validate_date_format()
        self.birthday = birthday


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, value):
        return self.data.get(value, "Contact not found.")

    def delete(self, value):
        self.data.pop(value, None)

    def birthdays_per_week(self):
        name_to_birthday = []
        for name, record in self.data.items():
            if record.birthday:
                name_to_birthday.append({'name': name, 'birthday': datetime.strptime(record.birthday.value, '%d.%m.%Y')})

        if name_to_birthday:
            birthdays = get_birthdays_per_week(name_to_birthday)
            if birthdays:
                return '\n'.join(birthdays)
            else:
                return "There is no birthdays this week."

        return "No one added birthday."

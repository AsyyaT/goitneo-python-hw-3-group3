from address_book import AddressBook, Record, PhoneException, DateFormatException


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me contact name and phone please."
        except KeyError:
            return "Enter valid contact name."
        except IndexError:
            return "Enter contact name."
        except PhoneException:
            return "Phone number must contain 10 digits"
        except DateFormatException:
            return "Following date format required: DD.MM.YYYY"

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record != 'Contact not found':
        record.add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)

    return "Contact added."


def show_all_contacts(book):
    formatted_contacts = []
    for name, record in book.data.items():
        formatted_contacts.append(str(record))

    return '\n'.join(formatted_contacts)


@input_error
def show_phone(book, args):
    name = args[0]
    return book.find(name)


def update_phone(book, args):
    try:
        name, phone, new_phone = args
    except ValueError:
        return "Please enter name, old number and new number."
    contact = book.find(name)
    contact.edit_phone(phone, new_phone)

    return "Contact updated."


def add_birthday(book, args):
    try:
        name, date = args
    except ValueError:
        return "Please enter a name and birthday."

    contact = book.find(name)
    contact.add_birthday(date)

    return "Birthday added."


@input_error
def show_birthday(book, args):
    name = args[0]
    contact = book.find(name)
    birthday = contact.birthday if contact.birthday else "Birthday for this contact not added."
    return birthday


def show_nearest_birthdays(book):
    return book.birthdays_per_week()


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "all":
            print(show_all_contacts(book))
        elif command == "phone":
            print(show_phone(book, args))
        elif command == "change":
            print(update_phone(book, args))
        elif command == "add-birthday":
            print(add_birthday(book, args))
        elif command == "show-birthday":
            print(show_birthday(book, args))
        elif command == "birthdays":
            print(show_nearest_birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

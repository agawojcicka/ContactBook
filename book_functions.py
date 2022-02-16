import SQLite


def add_data():
    contact_id = SQLite.get_id()
    first = input("First name: ")
    last = input("Last name: ")
    get_address(contact_id)
    get_phone(contact_id)
    email = input("Email address: ")

    SQLite.add(contact_id, first, last, email)


def get_address(contact_id):
    print("Address: ")
    street = input("Street address: ")
    building = input("Building number: ")
    flat = input("Flat number: ")
    post_code = input("Postal code : ")
    city = input("City: ")
    country = input("Country: ")

    SQLite.add_address(contact_id, street, building, flat, post_code, city, country)


def get_phone(contact_id):
    switch = "y"

    while switch == "y":
        phone = input("Enter the phone number: ")
        SQLite.add_phone(contact_id, phone)

        switch = input("Do you want to add another phone number to this contact? (y/n) ").lower()


def find_by():
    pattern = input("Find by:\n"
                    "1. First name\n"
                    "2. Last name\n"
                    )

    val = input("Enter the pattern: ")

    match pattern:
        case "1":
            return SQLite.find(val, None)
        case "2":
            return SQLite.find(None, val)


def change_rec():
    print("Which contact would you like to change?")
    first = input("First name: ")
    last = input("Last name: ")

    index = SQLite.get_contact_id(first, last)[0]

    pattern = input("Change:\n"
                    "1. First name\n"
                    "2. Last name\n"
                    "3. Address\n"
                    "4. Phone number\n"
                    "5. Email address\n")

    SQLite.change(index, pattern)


def remove_rec():
    first = input("Enter First name of contact you would like to remove: ")
    last = input("Enter Last name of contact you would like to remove: ")
    index = SQLite.get_contact_id(first, last)[0]

    SQLite.remove(index)


def display():
    db = SQLite.show_all()
    for item in db:
        print(item)


def initiate():
    switch = "y"
    while switch == "y":
        pattern = input("Would you like to:\n"
                        "1. Add contact\n"
                        "2. Find contact\n"
                        "3. Change contact\n"
                        "4. Remove contact\n"
                        "5. Display contacts on the screen\n")

        match pattern:
            case "1":
                add_data()
            case "2":
                print(find_by())
            case "3":
                change_rec()
            case "4":
                remove_rec()
            case "5":
                display()

        switch = input("Do you want to continue (y/n)?").lower()

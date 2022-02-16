import sqlite3

conn = sqlite3.connect('book.db')
c = conn.cursor()


def create_table():
    with conn:
        c.execute("""create table if not exists contacts (
                        contact_id integer,
                        first text,
                        last text,
                        email text,
                        PRIMARY KEY (contact_id))""")


def create_address_table():
    with conn:
        c.execute("""create table if not exists address (
                        contact_id integer,
                        street text,
                        building integer,
                        flat integer,
                        postal_code string,
                        city string,
                        country string,
                        FOREIGN KEY(contact_id) REFERENCES contacts(contact_id))""")


def create_phone_table():
    with conn:
        c.execute("""create table if not exists phone (
                        contact_id integer,
                        phone integer,
                        FOREIGN KEY(contact_id) REFERENCES address(contact_id),
                        FOREIGN KEY(contact_id) REFERENCES contacts(contact_id))""")


def get_id():
    i = 1
    with conn:
        c.execute("SELECT contact_id FROM contacts")

    idx = c.fetchall()

    while i in idx:
        i += 1

    return i


def get_contact_id(first, last):
    with conn:
        c.execute("SELECT contact_id FROM contacts WHERE :first LIKE UPPER(first) AND :last LIKE UPPER(last)",
                  {
                      'first': first,
                      'last': last
                  })

        return c.fetchone()


def add(contact_id, first, last, email):
    with conn:
        c.execute("INSERT INTO contacts VALUES (:contact_id, :first, :last, :email)",
                  {
                      'contact_id': contact_id,
                      'first': first,
                      'last': last,
                      'email': email
                  })


def add_address(contact_id, street, building, flat, postal_code, city, country):
    with conn:
        c.execute("INSERT INTO address VALUES (:contact_id, :street, :building, :flat, :postal_code, :city, :country)",
                  {
                      'contact_id': contact_id,
                      'street': street,
                      'building': building,
                      'flat': flat,
                      'postal_code': postal_code,
                      'city': city,
                      'country': country
                  })


def add_phone(contact_id, phone):
    with conn:
        c.execute("INSERT INTO phone VALUES (:contact_id, :phone)",
                  {
                      'contact_id': contact_id,
                      'phone': phone
                  })


def find(first, last):
    with conn:
        c.execute("""SELECT first, last, street, building, flat, postal_code, city, country, phone, email
                    FROM contacts INNER JOIN address ON contacts.contact_id = address.contact_id
                    INNER JOIN phone ON address.contact_id = phone.contact_id 
                    WHERE
                    :first IS NULL OR UPPER(:first) LIKE UPPER(first) AND
                    :last IS NULL OR UPPER(:last) LIKE UPPER(last)
                    """,
                  {
                      'first': first,
                      'last': last,
                  })

        return c.fetchall()


def change(index, pattern):
    with conn:
        match pattern:
            case "1":
                val = input("Enter new name: ")
                c.execute("UPDATE contacts SET first = :val WHERE contact_id = :id", {'val': val, 'id': index})
            case "2":
                val = input("Enter new last name: ")
                c.execute("UPDATE contacts SET last = :val WHERE contact_id = :id", {'val': val, 'id': index})
            case "3":
                change_address(index)
            case "4":
                change_phone(index)
            case "5":
                val = input("Enter new email address: ")
                c.execute("UPDATE contacts SET email = :val WHERE contact_id = :id", {'val': val, 'id': index})


def change_address(index):
    street = input("Enter new street: ")
    building = input("Enter new building number: ")
    flat = input("Enter new flat number: ")
    postal_code = input("Enter new postal code : ")
    city = input("Enter new city: ")
    country = input("Enter new country: ")

    with conn:
        c.execute("""UPDATE address SET street = :street, building = :building, flat = :flat,
         postal_code = :postal_code, city = :city, country = :country WHERE contact_id = :id""",
                  {
                      'id': index,
                      'street': street,
                      'building': building,
                      'flat': flat,
                      'postal_code': postal_code,
                      'city': city,
                      'country': country
                  })


def change_phone(index):
    pattern = input("Do you want to: \n"
                    "1. change phone number\n"
                    "2. add phone number\n")
    match pattern:
        case "1":
            with conn:
                c.execute("SELECT * FROM phone WHERE contact_id = :id", {'id': index})
                print(c.fetchall())

                to_change = input("Enter the number you would like to change: ")
                new_number = input("Enter new number: ")

                c.execute("UPDATE phone SET phone = :new_number WHERE phone = :phone",
                          {'new_number': new_number, 'phone': to_change})
        case "2":
            phone = input("Enter new phone number: ")
            add_phone(index, phone)


def remove(index):
    with conn:
        c.execute("DELETE FROM contacts WHERE contact_id = :index", {'index': index})
        c.execute("DELETE FROM address WHERE contact_id = :index", {'index': index})
        c.execute("DELETE FROM phone WHERE contact_id = :index", {'index': index})


def show_all():
    with conn:
        c.execute("""SELECT * FROM contacts INNER JOIN address ON contacts.contact_id = address.contact_id
                    INNER JOIN phone ON address.contact_id = phone.contact_id
                    WHERE first IS NOT NULL""")
        return c.fetchall()

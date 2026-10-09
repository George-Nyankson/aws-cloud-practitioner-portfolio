"""
Mini Database in Python
========================
A simple in-memory "database" built with lists and dictionaries.
Demonstrates CRUD (Create, Read, Update, Delete) operations and
basic search logic — the core ideas behind real data management systems.

Each "record" is a dictionary. All records are stored in a list, which
acts like a table. Every record gets a unique auto-incrementing "id",
similar to a primary key in a real database.
"""

# The "table": a list that holds all our records (dictionaries)
database = []

# Keeps track of the next id to assign (acts like an auto-increment primary key)
next_id = 1


def create_record(**fields):
    """CREATE: Add a new record to the database."""
    global next_id
    record = {"id": next_id}
    record.update(fields)
    database.append(record)
    next_id += 1
    print(f"Created record: {record}")
    return record


def read_all():
    """READ: Return every record in the database."""
    return database


def read_by_id(record_id):
    """READ: Find a single record by its id."""
    for record in database:
        if record["id"] == record_id:
            return record
    return None


def update_record(record_id, **fields):
    """UPDATE: Modify an existing record's fields by id."""
    record = read_by_id(record_id)
    if record is None:
        print(f"No record found with id {record_id}")
        return None
    record.update(fields)
    print(f"Updated record: {record}")
    return record


def delete_record(record_id):
    """DELETE: Remove a record from the database by id."""
    record = read_by_id(record_id)
    if record is None:
        print(f"No record found with id {record_id}")
        return False
    database.remove(record)
    print(f"Deleted record with id {record_id}")
    return True


def search(**criteria):
    """
    SEARCH: Find all records matching given field values.
    Example: search(name="George") returns every record where name == "George"
    """
    results = []
    for record in database:
        match = all(record.get(key) == value for key, value in criteria.items())
        if match:
            results.append(record)
    return results


def print_table():
    """Pretty-print all records like a simple table."""
    if not database:
        print("(empty database)")
        return
    columns = sorted({key for record in database for key in record})
    widths = {c: max(len(c), *(len(str(r.get(c, ""))) for r in database)) for c in columns}
    header = " | ".join(c.ljust(widths[c]) for c in columns)
    print(header)
    print("-" * len(header))
    for r in database:
        print(" | ".join(str(r.get(c, "")).ljust(widths[c]) for c in columns))


def demo():
    """Run a walkthrough of every CRUD operation."""
    print("\n--- CREATE ---")
    create_record(name="Ama", role="Designer", city="Accra")
    create_record(name="Kojo", role="Developer", city="Kumasi")
    create_record(name="Efua", role="Developer", city="Accra")

    print("\n--- READ (all) ---")
    print_table()

    print("\n--- READ (by id) ---")
    print(read_by_id(2))

    print("\n--- UPDATE ---")
    update_record(2, role="Senior Developer")

    print("\n--- SEARCH ---")
    print("Developers:", search(role="Senior Developer"))
    print("People in Accra:", search(city="Accra"))

    print("\n--- DELETE ---")
    delete_record(1)

    print("\n--- FINAL STATE ---")
    print_table()


def interactive_menu():
    """A simple text menu so you can try the database yourself."""
    menu = """
Mini Database Menu
1. Create record
2. View all records
3. Find record by id
4. Update record
5. Delete record
6. Search records
7. Run demo
0. Exit
"""
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Name: ")
            role = input("Role: ")
            city = input("City: ")
            create_record(name=name, role=role, city=city)

        elif choice == "2":
            print_table()

        elif choice == "3":
            rid = int(input("Record id: "))
            print(read_by_id(rid))

        elif choice == "4":
            rid = int(input("Record id to update: "))
            field = input("Field to update (name/role/city): ")
            value = input("New value: ")
            update_record(rid, **{field: value})

        elif choice == "5":
            rid = int(input("Record id to delete: "))
            delete_record(rid)

        elif choice == "6":
            field = input("Search field (name/role/city): ")
            value = input("Value to match: ")
            print(search(**{field: value}))

        elif choice == "7":
            demo()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    # Run the scripted demo first so you can see everything in action,
    # then drop into the interactive menu to try it yourself.
    demo()
    print("\n" + "=" * 40)
    print("Now try it yourself!")
    print("=" * 40)
    interactive_menu()

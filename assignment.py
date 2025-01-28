import time
import datetime
from tabulate import tabulate


def open_file():
    try:
        with open("students.txt", "rt") as students:
            data = students.readlines()
            return data

    except FileNotFoundError:
        print("\n\tFile Not Found! :0")
        return False


def id_verfication(student_id, data, add=False):
    if (len(student_id) != 4) or (not (student_id.isdigit())):
        print("\n\tInvalid ID! Try again. :0")
        return False

    elif add:
        if any(f"{student_id}" in line for line in data):
            print("\n\tStudent ID alread exist! Try again. :0")
            return False
        else:
            return True

    elif not any(f"{student_id}" in line for line in data):
        print("\n\tStudent ID does not exist! Try again. :0")
        return False

    else:
        return True


def st_details(
    student_id,
    name,
    g_name,
    books=False,
    old_books=False,
    up_books=False,
    total_books=False,
    x=False,
    y=False,
):
    print("\nStudent Details:")
    print(f"\n\tStudent ID: {student_id}")
    print(f"\tStudent Name: {name}")
    print(f"\tGuardian Name: {g_name}")

    if x:
        print(f"\tBorrowed Books: {books}")

    if y:
        print(f"\tPreviously Borrowed Books: {old_books}")
        print(f"\tBorrowed/Returned Books: {up_books}")
        print(f"\tTotal Number of Books: {total_books}")

    return None


def available_ids():
    data = open_file()
    if not data:
        return None

    used_ids = {line.split(",")[0] for line in data}

    print("\n\tAvailable IDs:", end=" ")

    count = 0
    for i in range(10000):
        ids = f"{i:04d}"
        if ids not in used_ids:
            print(f"{ids}", end=",")
            count += 1
            if count == 5:
                break

    if count == 0:
        print("House Full! No IDs available. :0")
    else:
        print(".....")

    return None


def add_student():
    data = open_file()
    if not data:
        return None

    print("\nAdd Menu:")
    available_ids()

    while True:
        student_id = input("\n\tEnter the student ID to add or [e] to exit: ").strip()

        if student_id.lower() == "e":
            print("\n\tExiting the menu. ;)")
            break

        id_validation = id_verfication(student_id, data, add=True)
        if not id_validation:
            continue

        name = input("\tEnter the student name: ").strip().capitalize()
        g_name = input("\tEnter the guardian name: ").strip().capitalize()

        while True:
            books = input("\n\tEnter the number of book(s) or [e] to exit: ").strip()

            if books == "e":
                print("\n\tExiting the menu. ;)")
                break

            elif int(books) > 10:
                print("\n\tCannot borrow more than 10 books! Try again. :0")
                continue

            elif int(books) < 0:
                print("\n\tYou haven't borrowed any books yet.")
                print("\tThat's why you are here to enter your data, right?")
                print("\tPlease check your input and try again. ;)")
                continue

            else:
                with open("students.txt", "at") as students:
                    students.write(f"{student_id},{name},{g_name},{books}\n")

                print("\nRecord added successfully! ;)")
                st_details(student_id, name, g_name, books, x=True)

                break

        break


def update_student():
    data = open_file()
    if not data:
        return None

    print("\nUpdate Menu:")

    while True:
        student_id = input(
            "\n\tEnter the Student ID to update or [e] to exit: "
        ).strip()

        if student_id.lower() == "e":
            print("\n\tExiting the menu. ;)")
            break

        id_validation = id_verfication(student_id, data)
        if not id_validation:
            continue

        for line in data:
            if f"{student_id}" in line:
                name, g_name, old_books = line.strip().split(",")[1:4]
                old_books = int(old_books)
                break

        print(f"\n\tStudent Name: {name}")
        print(f"\tGuardian Name: {g_name}")

        while True:
            choice = input("\n\tDo you want to update the name(s)? [yes/no]: ")

            if choice.lower() == "yes":
                name = input("\n\tEnter the student name: ").strip().capitalize()
                g_name = input("\tEnter the guardian name: ").strip().capitalize()

            elif choice.lower() == "no":
                print("\n\tName(s) not changed.")
                break

            else:
                print("\n\tInvalid Choice! Try again. :0")
                continue

            break

        print(f"\n\tPreviously Borrowed Books: {old_books}")
        print("\n\tEnter [+/-] before the number to borrow or to return the book(s).")

        while True:
            up_books = input("\n\tEnter the number of book(s) or [e] to exit: ").strip()
            input_val = up_books

            if up_books.lower() == "e":
                print("\n\tExiting the menu. ;)")
                break

            elif input_val.lstrip("+-").isdigit():
                up_books = int(up_books)
                total_books = old_books + up_books

                if total_books > 10:
                    print("\n\tCannot borrow more than '10' books! Try Again. :0")
                    print(f"\tCurrent total: {old_books}")
                    continue

                elif total_books < 0:
                    print("\n\tCannot return more than borrowed books! Try Again. :0")
                    print(f"\tCurrent total: {old_books}")
                    continue

                else:
                    with open("students.txt", "wt") as students:
                        for line in data:
                            if f"{student_id}" in line:
                                students.write(
                                    f"{student_id},{name},{g_name},{total_books}\n"
                                )
                            else:
                                students.write(line)

                    print("\nRecord updated successfully! ;)")
                    st_details(student_id, name, g_name, old_books=old_books, up_books=up_books, total_books=total_books, y=True)

                    break

            else:
                print("\n\tInvalid Input! Try again. :0")
                continue

        break


def list_student():
    data = open_file()
    if not data:
        return None

    print("\nListing Menu:")

    while True:
        student_id = input("\n\tEnter the Student ID to list or [e] to exit: ").strip()

        if student_id.lower() == "e":
            print("\n\tExiting the menu. ;)")
            break

        id_validation = id_verfication(student_id, data)
        if not id_validation:
            continue

        for line in data:
            if f"{student_id}" in line:
                student_id, name, g_name, books = line.strip().split(",")
                st_details(student_id, name, g_name, books, x=True)

                break

        break


def list_all_students():
    data = open_file()
    if not data:
        return None

    print("\nListing all students:\n")

    # You can use [A] part if you do not have the "tabulate" library installed
    # but "tabulate" is recomended.

    # [A]: {
    # for line in data:
    #     student_id, name, g_name, books = line.strip().split(",")
    #     st_details(student_id, name, g_name, books, x=True)
    # }

    # [B]: {
    headers = ["Student ID", "Student Name", "Guardian Name", "Borrowed Books"]

    table = []
    for line in data:
        student_id, name, g_name, books = line.strip().split(",")
        table.append([student_id, name, g_name, books])

    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
    # }

    print(f"\nTotal number of students: {len(data)}")


def delete_student():
    data = open_file()
    if not data:
        return None

    print("\nDelete Menu:")

    while True:
        student_id = input(
            "\n\tEnter the Student ID to delete or [e] to exit: "
        ).strip()

        if student_id.lower() == "e":
            print("\n\tExiting the menu. ;)")
            break

        id_validation = id_verfication(student_id, data)
        if not id_validation:
            continue

        for line in data:
            if f"{student_id}" in line:
                student_id, name, g_name, books = line.strip().split(",")
                st_details(student_id, name, g_name, books, x=True)

        while True:
            choice = input("\n\tAre you sure? [yes/no]: ")
            if choice.lower() == "yes":
                updated_data = [line for line in data if f"{student_id}" not in line]

                with open("students.txt", "wt") as students:
                    students.writelines(updated_data)

                print("\n\tStudent record deleted successfully!")
                break

            elif choice.lower() == "no":
                print("\n\tExiting the menu. ;)")
                break

            else:
                print("\n\tInvlid Input! Try again. :0")
                continue

        break


def main():
    print("\nWELCOME TO LIBRARY MANAGEMENT SYSTEM")
    print("=(Where Students Can Borrow Books!)=")

    while True:
        print(f"\nMain Menu:\t\t{datetime.date.today()}")
        print("\n\t[1] Add Student")
        print("\t[2] Update Student")
        print("\t[3] List Student")
        print("\t[4] List All Students")
        print("\t[5] Delete Student")
        print("\t[6] Available IDs")
        print("\t[e] Exit")

        choice = input("\n\tEnter your choice: ").strip()
        if choice == "1":
            add_student()
        elif choice == "2":
            update_student()
        elif choice == "3":
            list_student()
        elif choice == "4":
            list_all_students()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            available_ids()
        elif choice.lower() == "e":
            print("\nExiting the program. Bye! ;)\n")
            time.sleep(2)
            break
        else:
            print("\n\tInvalid Choice! Please try again. :0")


main()

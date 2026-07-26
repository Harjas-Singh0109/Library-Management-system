import csv

books_file = "books.csv"
issued_file = "issued_books.csv"

try:
    f = open(books_file, "r", newline="")
    f.close()
except FileNotFoundError:
    f = open(books_file, "w", newline="")
    writer = csv.writer(f)
    writer.writerow(["book_id", "title", "author", "total_copies", "available_copies"])
    f.close()

try:
    f = open(issued_file, "r", newline="")
    f.close()
except FileNotFoundError:
    f = open(issued_file, "w", newline="")
    writer = csv.writer(f)
    writer.writerow(["book_id", "student_name", "issue_date", "due_date", "returned"])
    f.close()

while True:
    print("===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Add a Book")
    print("2. View All Books")
    print("3. Search a Book")
    print("4. Issue a Book")
    print("5. Return a Book")
    print("6. View Issued Books")
    print("7. Exit")
    choice = input("Enter your choice (1-7): ")
    choice = choice.strip()

    if choice == "1":
        f = open(books_file, "r", newline="")
        reader = csv.DictReader(f)
        books = list(reader)
        f.close()

        book_id = input("Enter Book ID (unique): ")
        book_id = book_id.strip()

        found = False
        for b in books:
            if b["book_id"] == book_id:
                found = True

        if found == True:
            print("A book with ID '" + book_id + "' already exists.")
        else:
            title = input("Enter Title: ")
            title = title.strip()
            author = input("Enter Author: ")
            author = author.strip()
            total_copies = input("Enter Total Copies: ")
            total_copies = total_copies.strip()

            if total_copies.isdigit() and int(total_copies) > 0:
                new_book = {"book_id": book_id, "title": title, "author": author, "total_copies": total_copies, "available_copies": total_copies}
                books.append(new_book)

                f = open(books_file, "w", newline="")
                writer = csv.DictWriter(f, fieldnames=["book_id", "title", "author", "total_copies", "available_copies"])
                writer.writeheader()
                writer.writerows(books)
                f.close()

                print("Book '" + title + "' added successfully with " + total_copies + " copies.")
            else:
                print("Total copies must be a positive whole number.")

    elif choice == "2":
        f = open(books_file, "r", newline="")
        reader = csv.DictReader(f)
        books = list(reader)
        f.close()

        if len(books) == 0:
            print("No books in the library yet.")
        else:
            print("ID", "Title", "Author", "Total", "Available")
            for b in books:
                print(b["book_id"], b["title"], b["author"], b["total_copies"], b["available_copies"])

    elif choice == "3":
        keyword = input("Enter title or author to search: ")
        keyword = keyword.strip().lower()

        f = open(books_file, "r", newline="")
        reader = csv.DictReader(f)
        books = list(reader)
        f.close()

        found_any = False
        for b in books:
            if keyword in b["title"].lower() or keyword in b["author"].lower():
                print(b["book_id"], b["title"], b["author"], b["available_copies"])
                found_any = True

        if found_any == False:
            print("No matching books found.")

    elif choice == "4":
        book_id = input("Enter Book ID to issue: ")
        book_id = book_id.strip()

        f = open(books_file, "r", newline="")
        reader = csv.DictReader(f)
        books = list(reader)
        f.close()

        selected_book = None
        for b in books:
            if b["book_id"] == book_id:
                selected_book = b

        if selected_book == None:
            print("Book ID not found.")
        elif int(selected_book["available_copies"]) <= 0:
            print("Sorry, '" + selected_book["title"] + "' has no available copies right now.")
        else:
            student_name = input("Enter Student Name: ")
            student_name = student_name.strip()
            issue_date = input("Enter Issue Date (DD-MM-YYYY): ")
            issue_date = issue_date.strip()
            due_date = input("Enter Due Date (DD-MM-YYYY): ")
            due_date = due_date.strip()

            selected_book["available_copies"] = int(selected_book["available_copies"]) - 1

            f = open(books_file, "w", newline="")
            writer = csv.DictWriter(f, fieldnames=["book_id", "title", "author", "total_copies", "available_copies"])
            writer.writeheader()
            writer.writerows(books)
            f.close()

            f = open(issued_file, "a", newline="")
            writer = csv.DictWriter(f, fieldnames=["book_id", "student_name", "issue_date", "due_date", "returned"])
            writer.writerow({"book_id": book_id, "student_name": student_name, "issue_date": issue_date, "due_date": due_date, "returned": "No"})
            f.close()

            print("'" + selected_book["title"] + "' issued to " + student_name + ". Due date: " + due_date)

    elif choice == "5":
        book_id = input("Enter Book ID being returned: ")
        book_id = book_id.strip()
        student_name = input("Enter Student Name: ")
        student_name = student_name.strip()

        f = open(issued_file, "r", newline="")
        reader = csv.DictReader(f)
        records = list(reader)
        f.close()

        f = open(books_file, "r", newline="")
        reader = csv.DictReader(f)
        books = list(reader)
        f.close()

        matching_record = None
        for r in records:
            if r["book_id"] == book_id and r["student_name"].lower() == student_name.lower() and r["returned"] == "No":
                matching_record = r
                break

        if matching_record == None:
            print("No matching un-returned record found for this book and student.")
        else:
            matching_record["returned"] = "Yes"

            f = open(issued_file, "w", newline="")
            writer = csv.DictWriter(f, fieldnames=["book_id", "student_name", "issue_date", "due_date", "returned"])
            writer.writeheader()
            writer.writerows(records)
            f.close()

            for b in books:
                if b["book_id"] == book_id:
                    b["available_copies"] = int(b["available_copies"]) + 1

            f = open(books_file, "w", newline="")
            writer = csv.DictWriter(f, fieldnames=["book_id", "title", "author", "total_copies", "available_copies"])
            writer.writeheader()
            writer.writerows(books)
            f.close()

            print("Book returned successfully. Due date on record was: " + matching_record["due_date"])
            is_late = input("Was the book returned after the due date? (y/n): ")
            is_late = is_late.strip().lower()
            if is_late == "y":
                print("Note: this return was overdue. A fine may be applicable as per library rules.")

    elif choice == "6":
        f = open(issued_file, "r", newline="")
        reader = csv.DictReader(f)
        records = list(reader)
        f.close()

        active_records = []
        for r in records:
            if r["returned"] == "No":
                active_records.append(r)

        if len(active_records) == 0:
            print("No books are currently issued.")
        else:
            print("Book ID", "Student", "Issue Date", "Due Date")
            for r in active_records:
                print(r["book_id"], r["student_name"], r["issue_date"], r["due_date"])

    elif choice == "7":
        print("Exiting Library Management System. Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 7.")
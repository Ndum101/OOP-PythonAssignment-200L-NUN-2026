"""
============================================================
  OOP Group Project — Library Management System
============================================================
  Group Members:
    Ndubuisi Johnkennedy Okeke     | 242030102
    Rahmatallahi Ismael Mustapha   | 241030101
    Faisal Bagudu Ibrahim          | 242030094
    Tomiwa Giwa                    | 242030015
============================================================
  Course:     Object-Oriented Programming
  Level:      200L
  University: Nigerian University of Nissi (NUN)
  Year:       2026
============================================================
"""

import json
import os
from datetime import datetime, timedelta

DATA_FILE = "library.json"
LOAN_DAYS = 14


class Book:
    def __init__(self, book_id, title, author, copies):
        self.book_id          = book_id
        self.title            = title
        self.author           = author
        self.total_copies     = copies
        self.available_copies = copies

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, d):
        b = cls(d["book_id"], d["title"], d["author"], d["total_copies"])
        b.available_copies = d["available_copies"]
        return b


class Member:
    def __init__(self, member_id, name, email):
        self.member_id    = member_id
        self.name         = name
        self.email        = email
        self.issued_books = []

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, d):
        m = cls(d["member_id"], d["name"], d["email"])
        m.issued_books = d["issued_books"]
        return m


class IssuedRecord:
    def __init__(self, record_id, member_id, book_id, borrow_date, due_date, return_date=None):
        self.record_id   = record_id
        self.member_id   = member_id
        self.book_id     = book_id
        self.borrow_date = borrow_date
        self.due_date    = due_date
        self.return_date = return_date

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, d):
        return cls(**d)


class Library:
    def __init__(self):
        self.books   = {}
        self.members = {}
        self.records = []
        self._next_book_id   = 1
        self._next_member_id = 1
        self.load()

    def save(self):
        data = {
            "books":          {bid: b.to_dict() for bid, b in self.books.items()},
            "members":        {mid: m.to_dict() for mid, m in self.members.items()},
            "records":        [r.to_dict() for r in self.records],
            "next_book_id":   self._next_book_id,
            "next_member_id": self._next_member_id,
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        if not os.path.exists(DATA_FILE):
            return
        with open(DATA_FILE) as f:
            data = json.load(f)
        self.books   = {bid: Book.from_dict(b)   for bid, b in data["books"].items()}
        self.members = {mid: Member.from_dict(m) for mid, m in data["members"].items()}
        self.records = [IssuedRecord.from_dict(r) for r in data["records"]]
        self._next_book_id   = data["next_book_id"]
        self._next_member_id = data["next_member_id"]

    def add_book(self, title, author, copies=1):
        bid  = str(self._next_book_id)
        book = Book(bid, title, author, copies)
        self.books[bid] = book
        self._next_book_id += 1
        self.save()
        print(f"  Book added. ID: {bid}, Title: '{title}', Author: {author}, Copies: {copies}")

    def view_books(self):
        if not self.books:
            print("  No books in the library.")
            return
        print(f"\n  {'ID':<5} {'Title':<35} {'Author':<25} {'Available'}")
        print("  " + "-" * 72)
        for b in self.books.values():
            avail = f"{b.available_copies}/{b.total_copies}"
            flag  = " [OUT]" if b.available_copies == 0 else ""
            print(f"  {b.book_id:<5} {b.title:<35} {b.author:<25} {avail}{flag}")

    def search_books(self, query):
        q       = query.lower()
        results = [b for b in self.books.values()
                   if q in b.title.lower() or q in b.author.lower()]
        if not results:
            print("  No books found.")
            return
        print(f"\n  {'ID':<5} {'Title':<35} {'Author':<25} {'Available'}")
        print("  " + "-" * 72)
        for b in results:
            print(f"  {b.book_id:<5} {b.title:<35} {b.author:<25} {b.available_copies}/{b.total_copies}")

    def register_member(self, name, email):
        if any(m.email == email for m in self.members.values()):
            print(f"  Error: A member with email '{email}' already exists.")
            return
        mid    = str(self._next_member_id)
        member = Member(mid, name, email)
        self.members[mid] = member
        self._next_member_id += 1
        self.save()
        print(f"  Member registered. ID: {mid}, Name: {name}")

    def view_members(self):
        if not self.members:
            print("  No members registered.")
            return
        print(f"\n  {'ID':<5} {'Name':<25} {'Email':<30} {'Books Issued'}")
        print("  " + "-" * 70)
        for m in self.members.values():
            print(f"  {m.member_id:<5} {m.name:<25} {m.email:<30} {len(m.issued_books)}")

    def borrow_book(self, member_id, book_id):
        if member_id not in self.members:
            print(f"  Error: Member ID '{member_id}' not found.")
            return
        if book_id not in self.books:
            print(f"  Error: Book ID '{book_id}' not found.")
            return

        member = self.members[member_id]
        book   = self.books[book_id]

        if book_id in member.issued_books:
            print(f"  Error: {member.name} has already borrowed '{book.title}'.")
            return
        if book.available_copies <= 0:
            print(f"  Error: No copies of '{book.title}' are available.")
            return

        due_date = (datetime.now() + timedelta(days=LOAN_DAYS)).strftime("%Y-%m-%d")
        record   = IssuedRecord(
            record_id   = len(self.records) + 1,
            member_id   = member_id,
            book_id     = book_id,
            borrow_date = datetime.now().strftime("%Y-%m-%d"),
            due_date    = due_date,
        )
        self.records.append(record)
        member.issued_books.append(book_id)
        book.available_copies -= 1
        self.save()
        print(f"  '{book.title}' issued to {member.name}. Due date: {due_date}")

    def return_book(self, member_id, book_id):
        if member_id not in self.members:
            print(f"  Error: Member ID '{member_id}' not found.")
            return
        if book_id not in self.books:
            print(f"  Error: Book ID '{book_id}' not found.")
            return

        member = self.members[member_id]
        book   = self.books[book_id]

        if book_id not in member.issued_books:
            print(f"  Error: {member.name} has not borrowed '{book.title}'.")
            return

        for r in self.records:
            if r.member_id == member_id and r.book_id == book_id and r.return_date is None:
                r.return_date = datetime.now().strftime("%Y-%m-%d")
                break

        member.issued_books.remove(book_id)
        book.available_copies += 1
        self.save()
        print(f"  '{book.title}' returned by {member.name}.")

    def view_issued(self):
        active = [r for r in self.records if r.return_date is None]
        if not active:
            print("  No books are currently issued.")
            return
        print(f"\n  {'#':<5} {'Member':<22} {'Book':<30} {'Borrowed':<12} {'Due'}")
        print("  " + "-" * 78)
        for r in active:
            member_name = self.members.get(r.member_id, type("", (), {"name": "Unknown"})()).name
            book_title  = self.books.get(r.book_id,   type("", (), {"title": "Unknown"})()).title
            print(f"  {r.record_id:<5} {member_name:<22} {book_title:<30} {r.borrow_date:<12} {r.due_date}")


def ask(prompt):
    return input(f"  {prompt}: ").strip()

def menu():
    print("""
+--------------------------------------+
|      Library Management System       |
+--------------------------------------+
|  1. Add Book        2. View Books    |
|  3. Search Books    4. Borrow Book   |
|  5. Return Book     6. View Issued   |
|  7. Register Member 8. View Members  |
|  0. Exit                             |
+--------------------------------------+""")

def main():
    lib = Library()

    while True:
        menu()
        choice = ask("Choice")

        if choice == "0":
            print("\n  Goodbye.\n")
            break

        elif choice == "1":
            print("\n  -- Add Book --")
            title  = ask("Title")
            author = ask("Author")
            copies = int(ask("Copies") or "1")
            lib.add_book(title, author, copies)

        elif choice == "2":
            print("\n  -- All Books --")
            lib.view_books()

        elif choice == "3":
            print("\n  -- Search Books --")
            lib.search_books(ask("Title or author"))

        elif choice == "4":
            print("\n  -- Borrow Book --")
            lib.view_members()
            mid = ask("Member ID")
            lib.view_books()
            bid = ask("Book ID")
            lib.borrow_book(mid, bid)

        elif choice == "5":
            print("\n  -- Return Book --")
            lib.view_issued()
            mid = ask("Member ID")
            bid = ask("Book ID")
            lib.return_book(mid, bid)

        elif choice == "6":
            print("\n  -- Currently Issued --")
            lib.view_issued()

        elif choice == "7":
            print("\n  -- Register Member --")
            lib.register_member(ask("Name"), ask("Email"))

        elif choice == "8":
            print("\n  -- All Members --")
            lib.view_members()

        else:
            print("  Invalid choice.")

        input("\n  Press Enter to continue...")

if __name__ == "__main__":
    main()

import os
import json


# ============================================
#                BOOK ENTITY
# ============================================
class Book:
    def __init__(self, book_id, title, author, available=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.available = available

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "available": self.available
        }


# ============================================
#               MEMBER ENTITY
# ============================================
class Member:
    def __init__(self, member_id, name, borrowed_books=None):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = borrowed_books if borrowed_books else []

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "borrowed_books": self.borrowed_books
        }


# ============================================
#                LIBRARY SYSTEM
# ============================================
class Library:
    def __init__(self, books_file="books.json", members_file="members.json"):
        self.books_file = books_file
        self.members_file = members_file
        self.books = self._load_file(self.books_file)
        self.members = self._load_file(self.members_file)

    # -----------------------------
    # File Utilities
    # -----------------------------
    def _load_file(self, file_path):
        if not os.path.exists(file_path):
            return {}
        with open(file_path, "r") as f:
            return json.load(f)

    def _save_file(self, file_path, data):
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    # -----------------------------
    # Core Library Functionalities
    # -----------------------------
    def add_book(self, book):
        self.books[book.book_id] = book.to_dict()
        self._save_file(self.books_file, self.books)
        print("Book added successfully.")

    def add_member(self, member):
        self.members[member.member_id] = member.to_dict()
        self._save_file(self.members_file, self.members)
        print("Member added successfully.")

    def borrow_book(self, member_id, book_id):
        if member_id not in self.members:
            print("Invalid Member ID.")
            return

        if book_id not in self.books:
            print("Invalid Book ID.")
            return

        if not self.books[book_id]["available"]:
            print("Book is already borrowed.")
            return

        self.books[book_id]["available"] = False
        self.members[member_id]["borrowed_books"].append(book_id)

        self._save_file(self.books_file, self.books)
        self._save_file(self.members_file, self.members)

        print("Book borrowed successfully.")

    def return_book(self, member_id, book_id):
        if member_id not in self.members:
            print("Invalid Member ID.")
            return

        if book_id not in self.members[member_id]["borrowed_books"]:
            print("This member did not borrow this book.")
            return

        self.members[member_id]["borrowed_books"].remove(book_id)
        self.books[book_id]["available"] = True

        self._save_file(self.books_file, self.books)
        self._save_file(self.members_file, self.members)

        print("Book returned successfully.")

    # -----------------------------
    # Display Functions
    # -----------------------------
    def show_books(self):
        print("\n--- Library Books ---")
        for book in self.books.values():
            status = "Available" if book["available"] else "Borrowed"
            print(f'{book["book_id"]}: {book["title"]} by {book["author"]} ({status})')

    def show_members(self):
        print("\n--- Library Members ---")
        for member in self.members.values():
            print(f'{member["member_id"]}: {member["name"]} | Borrowed: {member["borrowed_books"]}')


# ============================================
#                  MAIN MENU
# ============================================
def main():
    library = Library()

    menu = """
========== Library Menu ==========
1. Add Book
2. Add Member
3. Borrow Book
4. Return Book
5. Show All Books
6. Show All Members
7. Exit
"""
    while True:
        print(menu)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            book = Book(
                input("Book ID: "),
                input("Title: "),
                input("Author: ")
            )
            library.add_book(book)

        elif choice == "2":
            member = Member(
                input("Member ID: "),
                input("Name: ")
            )
            library.add_member(member)

        elif choice == "3":
            library.borrow_book(
                input("Member ID: "),
                input("Book ID: ")
            )

        elif choice == "4":
            library.return_book(
                input("Member ID: "),
                input("Book ID: ")
            )

        elif choice == "5":
            library.show_books()

        elif choice == "6":
            library.show_members()

        elif choice == "7":
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

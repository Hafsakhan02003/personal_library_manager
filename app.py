import streamlit as st
import sqlite3

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row
    return conn

# Function to add a new book
def add_book(title, author, year, status="Available"):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year, status) VALUES (?, ?, ?, ?)", 
                   (title, author, year, status))
    conn.commit()
    conn.close()

# Function to view all books
def get_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

# Function to update book status
def update_book_status(book_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET status = ? WHERE id = ?", (status, book_id))
    conn.commit()
    conn.close()

# Function to delete a book
def delete_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

# Streamlit UI
st.title("📚 BAYT_AL_HIKMA"
    
" Personal Library Manager")

# Tabs
menu = ["Add Book", "View Books", "Manage Books"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Book":
    st.subheader("📖 Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Year", min_value=1000, max_value=2025, step=1)
    
    if st.button("Add Book"):
        if title and author:
            add_book(title, author, year)
            st.success(f"Book '{title}' added successfully!")
        else:
            st.warning("Please enter both Title and Author.")

elif choice == "View Books":
    st.subheader("📚 View All Books")
    books = get_books()
    
    if books:
        for book in books:
            st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - *{book['status']}*")
    else:
        st.info("No books found.")

elif choice == "Manage Books":
    st.subheader("⚙️ Manage Books")
    books = get_books()
    book_titles = [f"{book['id']} - {book['title']}" for book in books]

    if book_titles:
        selected_book = st.selectbox("Select a Book", book_titles)
        book_id = int(selected_book.split(" - ")[0])
        
        new_status = st.selectbox("Update Status", ["Available", "Borrowed"])
        if st.button("Update Status"):
            update_book_status(book_id, new_status)
            st.success("Book status updated!")

        if st.button("Delete Book"):
            delete_book(book_id)
            st.warning("Book deleted!")
    else:
        st.info("No books to manage.")

# Run Streamlit App using: `streamlit run app.py`

import streamlit as st
import sqlite3
import pandas as pd

# Initialize the SQLite database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create a Books table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        copies_available INTEGER
    )
''')
conn.commit()

def add_book(title, author, copies_available):
    cursor.execute('''
        INSERT INTO books (title, author, copies_available)
        VALUES (?, ?, ?)
    ''', (title, author, copies_available))
    conn.commit()

def lend_book(book_id):
    cursor.execute('''
        UPDATE books
        SET copies_available = copies_available - 1
        WHERE id = ?
    ''', (book_id,))
    conn.commit()

def show_books():
    cursor.execute('SELECT * FROM books')
    books_data = cursor.fetchall()
    if not books_data:
        st.warning("No books found.")
        return None
    columns = ['ID', 'Title', 'Author', 'Copies Available']
    books_df = pd.DataFrame(books_data, columns=columns)
    return books_df

# Streamlit app starts here
st.title("Library Management System")

# Sidebar for user input
menu = st.sidebar.selectbox("Menu", ["Add Book", "Lend Book", "Show Books"])

if menu == "Add Book":
    st.header("Add a New Book")
    new_title = st.text_input("Enter Book Title:")
    new_author = st.text_input("Enter Author Name:")
    new_copies = st.number_input("Enter Number of Copies:", min_value=1)
    if st.button("Add Book"):
        add_book(new_title, new_author, new_copies)
        st.success(f'Book "{new_title}" added successfully!')

elif menu == "Lend Book":
    st.header("Lend a Book")
    books_df = show_books()
    if books_df is not None:
        selected_book_id = st.selectbox("Select a book to lend:", books_df['ID'])
        if st.button("Lend Book"):
            lend_book(selected_book_id)
            st.success("Book lent successfully!")

elif menu == "Show Books":
    st.header("Available Books")
    books_df = show_books()
    if books_df is not None:
        #st.dataframe(books_df, index=True)
        st.dataframe(books_df.reset_index(drop=True))

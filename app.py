from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)

# 🔹 MSSQL Connection
def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=YOUR_SERVER_NAME;"   # e.g. DESKTOP-ABC123\SQLEXPRESS
        "DATABASE=LibraryDB;"
        "Trusted_Connection=yes;"
    )
    return conn

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    conn.close()

    result = []
    for book in books:
        result.append({
            "id": book[0],
            "title": book[1],
            "author": book[2]
        })

    return jsonify(result)

# Add Book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    title = data['title']
    author = data['author']

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Books (title, author) VALUES (?, ?)",
        (title, author)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Book added successfully"})

# Delete Book
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Books WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Book deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
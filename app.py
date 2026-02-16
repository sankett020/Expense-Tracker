from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database and table
def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            description TEXT,
            amount REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_expense():
    date = request.form["date"]
    category = request.form["category"]
    description = request.form["description"]
    amount = float(request.form["amount"])

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
        (date, category, description, amount),
    )
    conn.commit()
    conn.close()

    return redirect("/view")

@app.route("/view")
def view_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]
    conn.close()

    if total is None:
        total = 0

    return render_template("view.html", expenses=expenses, total=total)

if __name__ == "__main__":
    app.run(debug=True)

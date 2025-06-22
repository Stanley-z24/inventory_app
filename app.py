from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB_NAME = 'inventory.db'

# Initialize DB
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS inventory (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            category TEXT,
                            supplier TEXT,
                            quantity INTEGER)''')

@app.route('/')
def index():
    search = request.args.get('search', '')
    with sqlite3.connect(DB_NAME) as conn:
        if search:
            items = conn.execute("SELECT * FROM inventory WHERE name LIKE ?", ('%' + search + '%',)).fetchall()
        else:
            items = conn.execute("SELECT * FROM inventory").fetchall()
    return render_template('index.html', items=items, search=search)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    category = request.form['category']
    supplier = request.form['supplier']
    quantity = int(request.form['quantity'])
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO inventory (name, category, supplier, quantity) VALUES (?, ?, ?, ?)",
                     (name, category, supplier, quantity))
    return redirect('/')

@app.route('/low-stock')
def low_stock():
    with sqlite3.connect(DB_NAME) as conn:
        items = conn.execute("SELECT * FROM inventory WHERE quantity < 10").fetchall()
    return render_template('index.html', items=items, search='Low Stock')
    
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

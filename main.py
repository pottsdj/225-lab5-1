from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database file path
DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # This enables name-based access to columns
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                item_id TEXT NOT NULL
                price TEXT NOT NULL
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''  # Message indicating the result of the operation
    if request.method == 'POST':
        # Check if it's a delete action
        if request.form.get('action') == 'delete':
            contact_id = request.form.get('contact_id')
            db = get_db()
            db.execute('DELETE FROM items WHERE id = ?', (contact_id,))
            db.commit()
            message = 'Item deleted successfully.'
        else:
            name = request.form.get('name')
            item_id = request.form.get('item_id')
            price = request.form.get('price')
            if name and item_id and price:
                db = get_db()
                db.execute('INSERT INTO items (name, item_id, price) VALUES (?, ?, ?)', (name, item_id, price))
                db.commit()
                message = 'Item added successfully.'
            else:
                message = 'Missing name, ID number, or Price.'

    # Always display the contacts table
    db = get_db()
    contacts = db.execute('SELECT * FROM items').fetchall()

    # Display the HTML form along with the contacts table
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Inventory</title>
        </head>
        <body>
            <h2>Add Inventory</h2>
            <form method="POST" action="/">
                <label for="name">Name:</label><br>
                <input type="text" id="name" name="name" required><br>
                <label for="item_id">Item ID:</label><br>
                <input type="text" id="item_id" name="item_id" required><br>
                <label for="price">Price:</label><br>
                <input type="text" id="price" name="price" required><br><br>
                <input type="submit" value="Submit">
            </form>
            <p>{{ message }}</p>
            {% if items %}
                <table border="1">
                    <tr>
                        <th>Name</th>
                        <th>Item ID</th>
                        <th>Price</th>
                        <th>Delete</th>
                    </tr>
                    {% for item in items %}
                        <tr>
                            <td>{{ item['name'] }}</td>
                            <td>{{ item['item_id'] }}</td>
                            <td>{{ item['price'] }}</td>
                            <td>
                                <form method="POST" action="/">
                                    <input type="hidden" name="contact_id" value="{{ contact['id'] }}">
                                    <input type="hidden" name="action" value="delete">
                                    <input type="submit" value="Delete">
                                </form>
                            </td>
                        </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No items found.</p>
            {% endif %}
        </body>
        </html>
    ''', message=message, items=items)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()  # Initialize the database and table
    app.run(debug=True, host='0.0.0.0', port=port)

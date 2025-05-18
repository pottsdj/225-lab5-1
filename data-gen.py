import sqlite3
import os

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_test_data(num_items):
    """Generate test data for the contacts table."""
    db = connect_db()
    for i in range(num_items):
        name = f'Test Name {i}'
        item_id = f'123456789{i}'
        price = f'12{i}'
        db.execute('INSERT INTO items (name, item_id, price) VALUES (?, ?)', (name, item_id, price))
    db.commit()
    print(f'{num_items} test items added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_data(10)  # Generate 10 test contacts.

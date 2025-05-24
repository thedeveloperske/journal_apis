import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Add new columns if they do not exist
try:
    cursor.execute("ALTER TABLE items ADD COLUMN name TEXT;")
except Exception as e:
    if 'duplicate column name' not in str(e):
        print(e)
try:
    cursor.execute("ALTER TABLE items ADD COLUMN description TEXT DEFAULT '';")
except Exception as e:
    if 'duplicate column name' not in str(e):
        print(e)

conn.commit()
conn.close()
print('Columns name and description ensured in items table.')

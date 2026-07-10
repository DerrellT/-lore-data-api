import sqlite3

# CONNECT TO DATABASE
# If "lore.db" does not exist, SQLite will CREATE it automatically.
conn = sqlite3.connect("lore.db")

# Cursor = the object that actually sends SQL commands to the database
# The "messenger" between Python and SQLite
cursor = conn.cursor()




cursor.execute("""
CREATE TABLE IF NOT EXISTS regions (
    id INTEGER PRIMARY KEY,   -- unique identifier for each region
    name TEXT NOT NULL UNIQUE -- region name must exist and be unique
)
""")



cursor.execute("""
CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY,      -- unique ID for each character
    name TEXT NOT NULL UNIQUE,   -- character name must exist and be unique

    region_id INTEGER,           -- links to regions.id

    FOREIGN KEY (region_id) REFERENCES regions(id)
    -- This enforces the idea:
    -- "A character belongs to a valid region"
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    Id INTEGER PRIMARY KEY ,
    username TEXT NOT NULL ,
    password TEXT NOT NULL 
)
""")

#SEED DATA INITIAL TEST DATA
# Inserts Region ONLY if table is empty
cursor.execute("SELECT COUNT(*) FROM regions")

# fetchone() returns a tuple like: (0,)
if cursor.fetchone()[0] == 0:

    cursor.execute("""
    INSERT INTO regions (id, name)
    VALUES (1, 'Rema'), (2, 'Rumo')
    """)


cursor.execute("SELECT COUNT(*) FROM characters")

if cursor.fetchone()[0] == 0:


    cursor.execute("""
    INSERT INTO characters (id, name, region_id)
    VALUES (1, 'Jicho', 1), (2, 'Amara', 1), (3, 'Sikio', 2)
    """)

cursor.execute("SELECT COUNT(*) FROM testuser")

if cursor.fetchone()[0] == 0:
    
    cursor.execute("""
    INSERT INTO users (id, username, password)
    VALUES (1, 'Kenny', 'Cheesecake')
    """)


conn.commit()
cursor.execute("SELECT * FROM regions")
rows = cursor.fetchall()
print(rows)


conn.close()


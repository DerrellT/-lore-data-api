import sqlite3

# CONNECT TO DATABASE
# If "lore.db" does not exist, SQLite will CREATE it automatically.
conn = sqlite3.connect("lore.db")

# Cursor = the object that actually sends SQL commands to the database
# The "messenger" between Python and SQLite
cursor = conn.cursor()


#CREATE TABLES (DATABASE STRUCTURE / SCHEMA)
# Regions table
# This table stores all regions in the world.
# Each region has:
# - id (unique identifier)
# - name (region name)

# IF NOT EXISTS: Prevents errors if you run this file multiple times.
cursor.execute("""
CREATE TABLE IF NOT EXISTS regions (
    id INTEGER PRIMARY KEY,   -- unique identifier for each region
    name TEXT NOT NULL UNIQUE -- region name must exist and be unique
)
""")


# Characters table
# This table stores characters in your world.
# region_id links each character to a region
# called a FOREIGN KEY relationship.
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


#SEED DATA INITIAL TEST DATA

# This section is ONLY for learning and testing. In real systems, this is handled separately.
# Insert Region (ONLY if table is empty)
# We check how many rows exist in regions
cursor.execute("SELECT COUNT(*) FROM regions")

# fetchone() returns a tuple like: (0,)
if cursor.fetchone()[0] == 0:

    # Insert first region
    cursor.execute("""
    INSERT INTO regions (id, name)
    VALUES (1, 'Rema'), (2, 'Rumo')
    """)


cursor.execute("SELECT COUNT(*) FROM characters")

if cursor.fetchone()[0] == 0:

    # Insert first character
    # region_id = 1 means "Rema"
    cursor.execute("""
    INSERT INTO characters (id, name, region_id)
    VALUES (1, 'Jicho', 1), (2, 'Amara', 1), (3, 'Sikio', 2)
    """)


# Without commit, nothing is permanently saved to the database file
conn.commit()
cursor.execute("SELECT * FROM regions")
rows = cursor.fetchall()
print(rows)


# Always close connection to free resources and avoid locks
conn.close()

# Python connects → Cursor sends SQL → Database stores data → Commit saves → Close ends session
import sqlite3
from fastapi import FastAPI, HTTPException

app = FastAPI()

# ----------------------------
# DATABASE HELPER
# ----------------------------

def get_db_connection():
    conn = sqlite3.connect("lore.db")
    conn.row_factory = sqlite3.Row  # lets us return dict-like rows
    return conn


# GET ALL CHARACTERS (SQL VERSION)
@app.get("/characters/")
def get_all_chars():
    """Returns all characters only"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM characters")
    rows = cursor.fetchall() #all rows

    conn.close()

    # convert rows into clean JSON
    return [dict(row) for row in rows]

@app.get("/characters/{name}")
def get_character(name):
    """Return a character by exact name match."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("Select * FROM characters WHERE name = ? ", (name,))
    row = cursor.fetchone() #one row
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Character not found") 
    return dict(row)

@app.get("/regions/")
def get_all_regions():
    """Returns all regions only"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM regions")
    rows = cursor.fetchall() #all rows

    conn.close()

    # convert rows into clean JSON
    return [dict(row) for row in rows]

@app.get("/regions/{name}")
def get_region(name):
    """Return a region by exact name match."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("Select * FROM regions WHERE name = ? ", (name,))
    row = cursor.fetchone() #one row
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Region not found") 
    return dict(row)
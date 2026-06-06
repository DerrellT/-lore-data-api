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


# ----------------------------
# GET ALL CHARACTERS (SQL VERSION)
# ----------------------------

@app.get("/characters/")
def get_all_chars():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM characters")
    rows = cursor.fetchall() #featch all multi results

    conn.close()

    # convert rows into clean JSON
    return [dict(row) for row in rows]

@app.get("/characters/{name}")
def get_character(name):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("Select * FROM characters WHERE name = ? ", (name,))
    row = cursor.fetchone() #single result fetch one
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Character not found") 
    return dict(row)


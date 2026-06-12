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

@app.get("/characters/{name}") #request is sent and name is extraced
def get_character(name):        #name is extraced as parameter and calls get_char
    """Return a character by exact name match."""
    conn = get_db_connection()  #database is opened this opens lore.db
    cursor = conn.cursor()      #cursor is created to send SQL commands from python

    cursor.execute("SELECT * FROM characters WHERE name = ? ", (name,)) #SQL is exectuted
    row = cursor.fetchone() #one row and result is retrieved here
    conn.close()            #close connection
    if row is None:         #check if character exits
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

@app.post("/characters/")
def create_character(name: str, region_id: int): #str and int are the expected inputs
    """Create a character."""
    if not name:         
        raise HTTPException(status_code=400, detail="Character name missing") 

    if not region_id:        
        raise HTTPException(status_code=400, detail="Region id missing") 
 
    conn = get_db_connection()
    cursor = conn.cursor()    
    cursor.execute("SELECT * FROM regions WHERE id = ? ", (region_id,)) #compare existing region id to user input
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=400, detail="Invalid region_id")
    cursor.execute("SELECT * FROM characters WHERE name = ? ", (name,)) #SQL is exectuted
    name_row = cursor.fetchone()
    if name_row:
        raise HTTPException(status_code=400, detail="Name already exits")

    cursor.execute("INSERT INTO characters (name, region_id) VALUES (?, ?)", (name, region_id)) # ? are place holders
    conn.commit()
    conn.close()  
    return {"message": "Character created succesfully",
            "name": name,
            "region_id": region_id
            }         
   
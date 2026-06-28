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
    conn.commit() #commit before we query data
    
    cursor.execute("SELECT * FROM characters WHERE name = ? ", (name,)) #return the char the user created instead of echoing
    new_char = cursor.fetchone()
    if new_char is None:
        raise HTTPException(status_code=400, detail="Character loading error")
    conn.close()  
    return dict(new_char)

@app.put("/characters/")
def update_character(character_id: int, updated_name: str, new_region_id: int):
    """Update a character."""
    if character_id is None:         
        raise HTTPException(status_code=400, detail="Character field is empty") 

    if not new_region_id:        
        raise HTTPException(status_code=400, detail="Region field is empty") 
    
    if not updated_name:
        raise HTTPException(status_code=400, detail="Updated name field is empty") 

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM regions WHERE id = ? ", (new_region_id,))
    r_row = cursor.fetchone()
    if r_row is None:
        raise HTTPException(status_code=400, detail="Region does not exist")
    
    cursor.execute("SELECT * FROM characters WHERE id = ? ", (character_id,))
    c_row = cursor.fetchone()
    if c_row is None:        
        raise HTTPException(status_code=404, detail="Character does not exist")

    cursor.execute("SELECT * FROM characters WHERE name = ? AND id != ? ", (updated_name, character_id)) #checks for duplicate name but not this current character
    name_row = cursor.fetchone()
    if name_row:
        raise HTTPException(status_code=400, detail="Name already exits with another id")

    cursor.execute("UPDATE characters SET name = ?, region_id = ? WHERE id = ?", (updated_name, new_region_id, character_id))
    conn.commit()
    conn.close()
    return {
        "character_id": character_id,
        "updated_name": updated_name,
        "new_region_id": new_region_id,
        "message": "Character updated successfully"
        }
# design to search for ID
#    cursor.execute("DELETE FROM characters WHERE name = ? ", (old_name,))
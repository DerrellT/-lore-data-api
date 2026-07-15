import sqlite3
from fastapi import FastAPI, HTTPException 
from jose import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
app = FastAPI()

# ----------------------------
# JWT SETUP
# ----------------------------

SECRET_KEY = "your-secret-key" #private key API uses to sign tokens
ALGORITHM = "HS256" #how token is created
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):  
    token_data = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    token_data.update({"exp": expire})

    token = jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# ----------------------------
# DATABASE HELPER
# ----------------------------

def get_db_connection():
    conn = sqlite3.connect("lore.db")
    conn.row_factory = sqlite3.Row  # lets us return dict-like rows
    return conn

@app.post("/login/")
def user_login(username: str, password: str):
    """User logs"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    u_i = cursor.fetchone()
    if not u_i:
        conn.close()
        raise HTTPException(status_code=400, detail="Invalid login")
    
    stored_hash = u_i["password"]

    if not pwd_context.verify(password, stored_hash):
        conn.close()
        raise HTTPException(status_code=400, detail="Invalid login")


    user_data = {
        "id": u_i["id"],
        "username": u_i["username"]
        }
    conn.close()

    return {
        "access_token": create_access_token(user_data)
        }


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
    return {
        "message": "Character found",
        "character": dict(row)
        }

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
    return {
        "message": "Region found",
        "region": dict(row)
        }

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
        raise HTTPException(status_code=400, detail="Name already exists")

    cursor.execute("INSERT INTO characters (name, region_id) VALUES (?, ?)", (name, region_id)) # ? are place holders
    conn.commit() #commit before we query data
    cursor.execute( "SELECT * FROM characters WHERE name = ?", (name,))
    new_character = cursor.fetchone()
    conn.close()

    return {
        "message": "Character created successfully",
        "character": dict(new_character)
    }

@app.post("/regions/")
def create_region(region_id: int, name: str): #str and int are the expected inputs
    """Create a region."""
    if not name:         
        raise HTTPException(status_code=400, detail="Region name missing") 

    if not region_id:        
        raise HTTPException(status_code=400, detail="Region id missing") 
 
    conn = get_db_connection()
    cursor = conn.cursor()    
    
    cursor.execute("SELECT * FROM regions WHERE id = ? ", (region_id,)) #checks for duplicate name but not this current character
    name_row = cursor.fetchone()
    if name_row:
        raise HTTPException(status_code=400, detail="Region id already exists")
    
    cursor.execute("SELECT * FROM regions WHERE name = ? ", (name,)) #SQL is exectuted
    name_row = cursor.fetchone()
    if name_row:
        raise HTTPException(status_code=400, detail="Region name already exists")

    cursor.execute("INSERT INTO regions (id, name) VALUES (?, ?)", (region_id, name)) # ? are place holders
    conn.commit()
    cursor.execute( "SELECT * FROM regions WHERE name = ?", (name,))
    new_region = cursor.fetchone()
    conn.close()
    return {
        "message": "Region created successfully",
        "region": dict(new_region)
    }


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
        "message": "Character updated successfully",
        "character": {"id": character_id,
        "name": updated_name,
        "region_id": new_region_id
        }
        }


@app.put("/regions/")
def update_region( region_id: int, updated_region_name: str,):
    """Update a region."""
    
    if region_id is None:         
        raise HTTPException(status_code=400, detail="Region field is empty") 

    if not updated_region_name:
        raise HTTPException(status_code=400, detail="Updated name field is empty") 

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM regions WHERE name = ? AND id != ? ", (updated_region_name, region_id)) #checks for duplicate name but not this current character
    name_row = cursor.fetchone()
    if name_row:
        raise HTTPException(status_code=400, detail="Region exists")
    
    cursor.execute("SELECT * FROM regions WHERE id = ? ", (region_id,))
    r_row = cursor.fetchone()
    if r_row is None:
        raise HTTPException(status_code=400, detail="Region does not exist")
    
    cursor.execute("UPDATE regions SET name = ? WHERE id = ?", (updated_region_name, region_id))
    conn.commit()
    conn.close()
    return {
        "message": "Region updated successfully",
        "region": {"id": region_id,
        "name": updated_region_name
        }
        }



@app.delete("/characters/")
def delete_character(character_id: int,):
    """Delete a character."""
    if character_id is None:         
        raise HTTPException(status_code=400, detail="Character field is empty")  
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM characters WHERE id = ? ", (character_id,))
    c_row = cursor.fetchone()
    if not c_row :        
        raise HTTPException(status_code=404, detail="Character does not exists")

    cursor.execute("DELETE FROM characters WHERE id = ? ", (character_id,))
    conn.commit()
    conn.close()
    return {
        "message": "Character deleted successfully",
        "id": character_id
        }
        

@app.delete("/regions/")
def delete_region(region_id: int,):
    """Delete a region."""
    if region_id is None:         
        raise HTTPException(status_code=400, detail="Region field is empty")  
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM regions WHERE id = ? ", (region_id,))
    r_row = cursor.fetchone()
    if not r_row :        
        raise HTTPException(status_code=404, detail="Region does not exists")

    cursor.execute("DELETE FROM regions WHERE id = ? ", (region_id,))
    conn.commit()
    conn.close()
    return {
        "message": "Region deleted successfully",
        "id": region_id
        
        }


#uvicorn app:app --reload
import sqlite3
import hashlib

def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("User registered successfully.")
    except sqlite3.IntegrityError:
        print("Error: Username already exists.")
    finally:
        conn.close()
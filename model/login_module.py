import sqlite3
import hashlib

def login_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        stored_hash = result[0]
        entered_hash = hashlib.sha256(password.encode()).hexdigest()
        if stored_hash == entered_hash:
            print("Login successful.")
            return True
    print("Login failed.")
    return False
import sqlite3
from hashlib import sha256

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect('finance.db')
    except Exception as e:
        print(f"Error connecting to database: {e}")
    return conn
def setup_database():
    """Create tables if they don't exist."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Create 'users' table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    birthday TEXT,
                    email TEXT UNIQUE,
                    username TEXT UNIQUE,
                    password TEXT NOT NULL,
                    security_question TEXT,
                    security_answer TEXT NOT NULL
                )
            ''')
            conn.commit()
        except Exception as e:
            print(f"Error setting up database: {e}")
        finally:
            conn.close()

def setup_database2():
    print("Setting up database...")
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    transaction_type TEXT,
                    amount REAL,
                    description TEXT,
                    date TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
            conn.commit()
            print("Database setup complete.")
        except Exception as e:
            print(f"Error setting up database: {e}")
        finally:
            conn.close()


def user_exists():
    """Check if any users exist in the database."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM users')
            result = cursor.fetchone()
            return result[0] > 0
        except Exception as e:
            print(f"Error checking user existence: {e}")
        finally:
            conn.close()
    return False

def register_user(first_name, last_name, birthday, email, username, password, security_question, security_answer):
    """Register a new user with hashed password and security question/answer."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Hash the password
            hashed_password = sha256(password.encode('utf-8')).hexdigest()
            # Normalize the security answer to lowercase
            normalized_security_answer = security_answer.lower()
            cursor.execute('''
                INSERT INTO users (
                    first_name, last_name, birthday, email, username, password, 
                    security_question, security_answer
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                first_name, last_name, birthday, email, username, hashed_password, 
                security_question, normalized_security_answer
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("Username or email already exists.")
        except Exception as e:
            print(f"Error registering user: {e}")
        finally:
            conn.close()
    return False

def authenticate_user(username, password):
    """Check username and password against hashed password in the database."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE username=?', (username,))
            result = cursor.fetchone()
            if result and sha256(password.encode('utf-8')).hexdigest() == result[0]:
                return True
        except Exception as e:
            print(f"Error authenticating user: {e}")
        finally:
            conn.close()
    return False

def verify_user_details(last_name, birthday, security_answer):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE last_name=? AND birthday=? AND security_answer=?", (last_name, birthday, security_answer))
        return cursor.fetchone() is not None
    finally:
        conn.close()

def get_user_info(last_name, birthday, security_answer):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM users WHERE last_name=? AND birthday=? AND security_answer=?", (last_name, birthday, security_answer))
        return cursor.fetchone()
    finally:
        conn.close()

def get_current_user_info():
    # Placeholder for demonstration; replace with dynamic user tracking logic
    current_user_id = 1  # Assume a logged-in user ID is maintained
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT username, email, first_name, last_name, birthday FROM users WHERE id=?", (current_user_id,))
        user_info = cursor.fetchone()
        if user_info:
            return {
                'username': user_info[0],
                'email': user_info[1],
                'first_name': user_info[2],
                'last_name': user_info[3],
                'birthday': user_info[4]
            }
        return None
    finally:
        conn.close()

def update_user_info(user_info):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        # Assume password is being hashed externally or handle here
        cursor.execute("""
            UPDATE users SET
            email = ?,
            first_name = ?,
            last_name = ?,
            birthday = ?,
            password = ? WHERE username = ?
        """, (user_info['email'], user_info['first_name'], user_info['last_name'], user_info['birthday'], user_info['password'], user_info['username']))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating user info: {e}")
        return False
    finally:
        conn.close()

setup_database()  # Ensure our database is set up with the required tables when this module is imported

import sqlite3


DATABASE_NAME = "neuropilot.db"


def get_connection():

    connection = sqlite3.connect(DATABASE_NAME)

    return connection


def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    # Chat Sessions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            session_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Chat History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT DEFAULT 'neuropilot-default',
            user_message TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            input_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Migrate: Ensure session_id column exists if table was previously created
    try:
        cursor.execute("ALTER TABLE chat_history ADD COLUMN session_id TEXT DEFAULT 'neuropilot-default'")
    except sqlite3.OperationalError:
        pass

    # Document Memory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_memory (
            document_id TEXT PRIMARY KEY,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()

    connection.close()


# Save or Create Session
def create_session(session_id, title):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO chat_sessions (session_id, title)
        VALUES (?, ?)
    """, (session_id, title))

    connection.commit()

    connection.close()


# Get All Sessions (ChatGPT Sidebar)
def get_all_sessions():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT session_id, title, created_at
        FROM chat_sessions
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    sessions = []

    for row in rows:
        sessions.append({
            "session_id": row[0],
            "title": row[1],
            "created_at": row[2]
        })

    connection.close()

    return sessions


# Save Chat
def save_chat(user_message, ai_response, input_type, session_id="neuropilot-default"):

    connection = get_connection()

    cursor = connection.cursor()

    # Ensure a session entry exists for this session_id
    cursor.execute("SELECT session_id FROM chat_sessions WHERE session_id = ?", (session_id,))
    if cursor.fetchone() is None:
        title = user_message[:35] + ("..." if len(user_message) > 35 else "")
        cursor.execute("INSERT OR REPLACE INTO chat_sessions (session_id, title) VALUES (?, ?)", (session_id, title))

    cursor.execute("""
        INSERT INTO chat_history
        (session_id, user_message, ai_response, input_type)
        VALUES (?, ?, ?, ?)
    """, (session_id, user_message, ai_response, input_type))

    connection.commit()

    connection.close()


# Get Chat History (Optionally filtered by session_id)
def get_chat_history(session_id=None):

    connection = get_connection()

    cursor = connection.cursor()

    if session_id:
        cursor.execute("""
            SELECT id, user_message, ai_response,
                   input_type, created_at, session_id
            FROM chat_history
            WHERE session_id = ?
            ORDER BY id ASC
        """, (session_id,))
    else:
        cursor.execute("""
            SELECT id, user_message, ai_response,
                   input_type, created_at, session_id
            FROM chat_history
            ORDER BY id ASC
        """)

    rows = cursor.fetchall()

    history = []

    for row in rows:

        chat = {
            "id": row[0],
            "user_message": row[1],
            "ai_response": row[2],
            "input_type": row[3],
            "created_at": row[4],
            "session_id": row[5]
        }

        history.append(chat)

    connection.close()

    return history


# Clear Chat History (Optionally for a specific session)
def clear_chat_history(session_id=None):

    connection = get_connection()

    cursor = connection.cursor()

    if session_id:
        cursor.execute("DELETE FROM chat_history WHERE session_id = ?", (session_id,))
        cursor.execute("DELETE FROM chat_sessions WHERE session_id = ?", (session_id,))
    else:
        cursor.execute("DELETE FROM chat_history")
        cursor.execute("DELETE FROM chat_sessions")

    connection.commit()

    connection.close()

    return True


# Save Document Memory
def save_document(document_id, file_name, file_path):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO document_memory
        (document_id, file_name, file_path)
        VALUES (?, ?, ?)
    """, (document_id, file_name, file_path))

    connection.commit()

    connection.close()


# Get Document from Memory
def get_document(document_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT document_id, file_name, file_path
        FROM document_memory
        WHERE document_id = ?
    """, (document_id,))

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "document_id": row[0],
        "file_name": row[1],
        "file_path": row[2]
    }

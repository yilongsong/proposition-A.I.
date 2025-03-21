# src/propositionsai/db.py
import sqlite3

DB_PATH = "notes.db"

def init_db():
    """Initialize the database with a notes table and an FTS5 index for RAG."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the main notes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original TEXT NOT NULL,
            logic TEXT NOT NULL
        )
    """)
    
    # Create an FTS5 virtual table for full-text search on the 'logic' column.
    # This table will be automatically updated if you use triggers or rebuild it.
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts 
        USING fts5(logic, content='notes', content_rowid='id')
    """)
    
    # Populate the FTS table with existing data (if any)
    cursor.execute("INSERT INTO notes_fts(rowid, logic) SELECT id, logic FROM notes")
    
    conn.commit()
    conn.close()

def insert_note(original: str, logic: str):
    """Insert a new note and update the FTS index."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO notes (original, logic) VALUES (?, ?)",
        (original, logic)
    )
    new_id = cursor.lastrowid
    # Insert into the FTS table as well
    cursor.execute(
        "INSERT INTO notes_fts(rowid, logic) VALUES (?, ?)",
        (new_id, logic)
    )
    conn.commit()
    conn.close()

def search_notes(query: str):
    """
    Perform a full-text search over the 'logic' column and return matching rows.
    Returns a list of tuples: (id, original, logic)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT notes.id, notes.original, notes.logic
        FROM notes
        JOIN notes_fts ON notes.id = notes_fts.rowid
        WHERE notes_fts MATCH ?
    """, (query,))
    results = cursor.fetchall()
    conn.close()
    return results
import sqlite3

DB_PATH = "silentsos.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS trusted_contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            name TEXT NOT NULL,
            relation TEXT,
            phone TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            message_text TEXT,
            semantic_score INTEGER,
            context_score INTEGER,
            final_score INTEGER,
            risk_level TEXT,
            signals TEXT,
            location_lat REAL,
            location_lng REAL,
            alert_sent INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS safe_phrases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            phrase TEXT NOT NULL,
            sensitivity INTEGER DEFAULT 70
        );

        INSERT OR IGNORE INTO users (id, name, phone) VALUES (1, 'Default User', '');
    """)
    conn.commit()
    conn.close()
    print("✅ Database initialized!")

if __name__ == "__main__":
    init_db()
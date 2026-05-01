# database.py
import sqlite3

DB_PATH = "silentsos.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS trusted_contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            relation TEXT,
            phone TEXT,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_text TEXT NOT NULL,
            semantic_score INTEGER DEFAULT 0,
            context_bonus INTEGER DEFAULT 0,
            final_score INTEGER DEFAULT 0,
            risk_level TEXT DEFAULT 'low',
            signals TEXT DEFAULT '[]',
            explanation TEXT,
            lat REAL,
            lng REAL,
            unusual_location BOOLEAN DEFAULT 0,
            alert_sent BOOLEAN DEFAULT 0,
            alert_channels TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS safe_phrases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phrase TEXT NOT NULL,
            meaning TEXT,
            sensitivity INTEGER DEFAULT 80,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized")
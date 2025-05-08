def get_chat_data():
    import sqlite3
    import pandas as pd
    conn = sqlite3.connect("zoom_chat1.db")
    cursor = conn.cursor()

    # Create the table if it doesn't exist (prevents errors)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        sender TEXT,
        message TEXT,
        sentiment_score REAL,
        sentiment_type TEXT
    )
    """)
    
    cursor.execute("DELETE FROM chat_data")
    
    
    conn.commit()
    try:
        df = pd.read_sql_query("SELECT * FROM chat_data", conn)
    except Exception:
        df = pd.DataFrame(columns=["timestamp", "sender", "message", "sentiment_score", "sentiment_type"])
    conn.close()
    return df

get_chat_data()
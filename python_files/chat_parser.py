
def parse_chat_file(filepath):
    import re
    import sqlite3
    from textblob import TextBlob

    # Setup DB
    conn = sqlite3.connect("zoom_chat.db")
    cursor = conn.cursor()

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

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Compile regex pattern
    pattern = re.compile(r"(\d{2}:\d{2}:\d{2}) From (.*?) to .*?:")

    entries = []
    current_entry = None

    for line in lines:
        match = pattern.match(line)
        if match:
            # If there's an existing entry, store it
            if current_entry:
                entries.append(current_entry)

            # Start a new message
            timestamp, sender = match.groups()
            current_entry = {
                "timestamp": timestamp.strip(),
                "sender": sender.strip(),
                "message": ""
            }
        elif current_entry:
            # Accumulate message lines
            current_entry["message"] += line.strip() + " "

    # Add the last message
    if current_entry:
        entries.append(current_entry)

    # Process entries
    for entry in entries:
        blob = TextBlob(entry["message"])
        sentiment = blob.sentiment.polarity
        sentiment_type = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
        
        cursor.execute("INSERT INTO chat_data (timestamp, sender, message, sentiment_score, sentiment_type) VALUES (?, ?, ?, ?, ?)", 
                    (entry["timestamp"], entry["sender"], entry["message"].strip(), sentiment, sentiment_type))

    conn.commit()
    conn.close()

    print("✅ Multi-line chat data parsed and stored.")



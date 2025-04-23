import sqlite3

# Connect to the DB
conn = sqlite3.connect("zoom_chat.db")
cursor = conn.cursor()

# Create engagement_metrics table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS engagement_metrics (
    sender TEXT PRIMARY KEY,
    message_count INTEGER,
    avg_sentiment REAL,
    engagement_score REAL
)
""")

# Clear existing data to refresh
cursor.execute("DELETE FROM engagement_metrics")

# Aggregate metrics from chat_data
cursor.execute("""
SELECT sender, COUNT(*) as message_count, AVG(sentiment_score) as avg_sentiment
FROM chat_data
GROUP BY sender
""")

rows = cursor.fetchall()

# Calculate engagement score and insert
for sender, msg_count, avg_sent in rows:
    engagement_score = (msg_count * 1.5) + (avg_sent * 10)
    cursor.execute("""
        INSERT INTO engagement_metrics (sender, message_count, avg_sentiment, engagement_score)
        VALUES (?, ?, ?, ?)
    """, (sender, msg_count, avg_sent, engagement_score))

conn.commit()
conn.close()

print("✅ Engagement metrics updated successfully!")






# import sqlite3

# conn = sqlite3.connect("zoom_chat.db")
# cursor = conn.cursor()

# # Add new column
# cursor.execute("ALTER TABLE chat_data ADD COLUMN matched_keywords TEXT")
# conn.commit()
# conn.close()

# print("✅ 'matched_keywords' column added.")

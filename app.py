from flask import Flask, render_template, request, redirect
import sqlite3
import pandas as pd
from werkzeug.utils import secure_filename
import os

# Import from your module folder
from python_files.chat_parser import parse_chat_file
from python_files.keyword_extract import extract_keywords
from python_files.database_change import engagement_metrics_table

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to fetch chat data from SQLite
def get_chat_data():
    conn = sqlite3.connect("zoom_chat.db")
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
    conn.commit()

    try:
        df = pd.read_sql_query("SELECT * FROM chat_data", conn)
    except Exception:
        df = pd.DataFrame(columns=["timestamp", "sender", "message", "sentiment_score", "sentiment_type"])
    conn.close()
    return df

@app.route('/')
def index():
    df = get_chat_data()
    total_messages = df.shape[0]
    avg_sentiment = round(df['sentiment_score'].mean() * 100, 2) if total_messages > 0 else 0
    messages_by_user = df['sender'].value_counts().to_dict()

    return render_template("index.html",
                           total_messages=total_messages,
                           avg_sentiment=avg_sentiment,
                           messages_by_user=messages_by_user)

@app.route('/upload', methods=['POST'])
def upload_file():
    print("FILES:", request.files)
    print("FILES RECEIVED:", request.files)
    print("FORM DATA:", request.form)
    if 'chatFile' not in request.files:
        return "No file uploaded", 400

    file = request.files['chatFile']
    topic = request.form.get("topic")

    if file.filename == '':
        return "Empty file name", 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(filepath)

    # Run your analysis modules
    parse_chat_file(filepath)
    extract_keywords(topic)
    engagement_metrics_table()

    return redirect('/')

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')
    df = get_chat_data()
    filtered = df[df['message'].str.contains(keyword, case=False, na=False)]
    return render_template("search.html", messages=filtered.to_dict(orient='records'), keyword=keyword)

if __name__ == '__main__':
    app.run(debug=True)


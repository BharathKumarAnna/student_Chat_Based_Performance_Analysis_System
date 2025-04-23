from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Basic HTML response if not serving frontend separately
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['chatFile']
        topic = request.form['topic'].lower()
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            messages = []
            participants = set()
            topic_mentions = {}

            for line in lines:
                if 'From' in line and ':' in line:
                    try:
                        name = line.split('From ')[1].split(':')[0].strip()
                        msg = line.split(':', 1)[1].strip()
                        participants.add(name)
                        messages.append((name, msg))
                        if topic in msg.lower():
                            topic_mentions[name] = topic_mentions.get(name, 0) + 1
                    except IndexError:
                        continue

            return {
                "total_participants": len(participants),
                "total_messages": len(messages),
                "avg_engagement": round(len(messages) / (len(participants) + 1), 2),
                "topic": topic,
                "mentions": topic_mentions
            }

    return '''
        <h2>Upload Zoom Chat</h2>
        <form method="POST" enctype="multipart/form-data">
            <label>Zoom Chat File (.txt):</label><br>
            <input type="file" name="chatFile"><br><br>
            <label>Study Topic:</label><br>
            <input type="text" name="topic"><br><br>
            <button type="submit">Upload</button>
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)

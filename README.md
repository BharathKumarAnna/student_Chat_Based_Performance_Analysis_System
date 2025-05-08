# 📊 Zoom Engagement Analytics Dashboard

A responsive web dashboard that visualizes and analyzes Zoom chat engagement data. This platform helps organizations and educators track participant interaction, sentiment, and overall engagement across Zoom sessions.

---

## 🚀 Features

* 📈 Live engagement metrics embedded via Grafana
* 🧠 Sentiment analysis and participant insights
* 🧍‍♂️ Unique participant tracking
* 📅 Recent session history and summaries
* 📤 Upload Zoom chat files for processing
* 🎨 Beautiful, responsive UI with Bootstrap 5

---

## 🛠️ Tech Stack

* **Frontend**: HTML5, CSS3, Bootstrap 5, Font Awesome, Google Fonts
* **Charts & Analytics**: ApexCharts, Grafana (via iframe)
* **Backend (Expected)**: Python (Flask), with sentiment & NLP libraries (like `TextBlob`/`spaCy`)
* **Data Processing**: Python scripts parsing `.txt` Zoom chat exports
* **Deployment**: Localhost / Docker / Cloud server (configurable)

---

## 📂 Folder Structure

```
zoom-analytics-dashboard/
│
├── templates/
│   └── index.html            # Main dashboard HTML (this file)
├── static/
│   ├── css/                  # Custom styles (optional)
│   └── js/                   # JS files (ApexCharts etc.)
├── app.py                    # Flask app (example backend)
├── uploads/                  # Folder for uploaded Zoom chat files
├── README.md                 # You're here!
└── requirements.txt          # Python dependencies
```

---

## ⚙️ Getting Started

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/zoom-analytics-dashboard.git
cd zoom-analytics-dashboard
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the app (if using Flask):**

```bash
python app.py
```

4. **Access the dashboard:**

Navigate to `http://localhost:5000` in your browser.

---

## 📤 Upload & Analyze

1. Export a Zoom chat as `.txt`.
2. Upload the file via the "Upload Zoom Chat" card.
3. View engagement metrics and sentiment breakdown instantly.

---

## 📊 Live Engagement via Grafana

A Grafana iframe is embedded to display real-time sentiment or engagement charts. You can:

* Configure the `iframe` URL inside `index.html` with your local or cloud Grafana dashboard.
* Use Prometheus or another data source for time-series metrics.

---

## 🛡️ Security Note

Ensure file uploads are validated and sanitized before processing in production.

---

## 💡 Future Improvements

* Add real-time sentiment prediction
* Integrate database to store sessions
* Enable authentication and role-based access
* Deploy as a Dockerized app

---

## 📄 License by BHARATH KUMAR ANNA

MIT License. Free to use and modify.



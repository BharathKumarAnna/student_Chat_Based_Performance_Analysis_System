import requests

def save_grafana_panel_image():
    url = "http://localhost:3000/render/d-solo/aejrzjiuucp34e/2"
    params = {
        "orgId": 1,
        "from": "now-6h",
        "to": "now",
        "width": 1000,
        "height": 500,
        "theme": "light"
    }

    try:
        response = requests.get(url)
        response.raise_for_status()
        with open("static/images/engagement_snapshot.png", "wb") as f:
            f.write(response.content)
        print("✅ Grafana panel image saved to static/images/engagement_snapshot.png")
    except Exception as e:
        print("❌ Error downloading Grafana snapshot:", e)

# Run it manually or call after file upload
save_grafana_panel_image()

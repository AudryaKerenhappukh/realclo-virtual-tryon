import requests, time, streamlit as st
from utils.authenticate import encode_jwt_token

API_BASE = "https://api-singapore.klingai.com"
AVATAR_URL = f"{API_BASE}/v1/images/generations"
TRYON_URL = f"{API_BASE}/v1/images/kolors-virtual-try-on"


def api_headers():
    return {"Authorization": f"Bearer {encode_jwt_token()}",
            "Content-Type": "application/json"}

def create_task(endpoint, payload):
    resp = requests.post(endpoint, headers=api_headers(), json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()

def poll_task(endpoint, task_id, interval=3, max_attempts=40):
    status_url = f"{endpoint}/{task_id}"
    progress = st.progress(0, text="Processing...")
    for attempt in range(max_attempts):
        r = requests.get(status_url, headers=api_headers(), timeout=60)
        r.raise_for_status()
        data = r.json()
        status = data["data"]["task_status"]
        progress.progress((attempt + 1) / max_attempts, text=f"Status: {status}")
        if status == "succeed":
            progress.empty(); return data
        if status == "failed":
            progress.empty()
            st.error(f"Task failed: {data['data'].get('task_status_msg', 'Unknown error')}")
            return None
        time.sleep(interval)
    progress.empty(); st.error("Task polling timed out."); return None

def download_image(url):
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    from PIL import Image
    from io import BytesIO
    return Image.open(BytesIO(r.content))

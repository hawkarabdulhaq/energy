import requests

def load_logs():
    url = "https://raw.githubusercontent.com/your_repo/your_project/main/database/energy_logs.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch logs from {url}")
        return []

import requests
import json
import random
import time

# URL API
LOGIN_URL = "https://api-tg.vooi.io/api/v2/auth/login"
START_SESSION_URL = "https://api-tg.vooi.io/api/tapping/start_session"
FINISH_SESSION_URL = "https://api-tg.vooi.io/api/tapping/finish"
START_AUTO_TRADE_URL = "https://api-tg.vooi.io/api/autotrade/start"
CLAIM_AUTO_TRADE_URL = "https://api-tg.vooi.io/api/autotrade/claim"

# Header untuk request
headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://app.tg.vooi.io",
    "Referer": "https://app.tg.vooi.io/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
}

# Payload untuk login
login_payload = {
    "initData": "user=%7B%22id%22%3A1675657762%2C%22first_name%22%3A%22Budikusuma%20%F0%9F%8D%85%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22Budikusuma0908%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&chat_instance=-5735803826137507506&chat_type=sender&auth_date=1728206252&hash=8ddcb027b3510ff2767215a71ef38e29bb484c0a4634786b069542917c89d634"
}

# Fungsi untuk login dan mendapatkan token
def login():
    response = requests.post(LOGIN_URL, headers=headers, data=json.dumps(login_payload))
    if response.status_code in (200, 201):
        access_token = response.json().get('tokens', {}).get('access_token')
        if access_token:
            with open('data.txt', 'w') as file:
                file.write(f"Access Token: {access_token}\n")
            print("Access token berhasil disimpan ke data.txt")
            return access_token
    print(f"Request gagal dengan status code: {response.status_code}, respon: {response.text}")
    return None

# Fungsi untuk memulai sesi tapping
def start_session(access_token):
    session_headers = headers.copy()
    session_headers["Authorization"] = f"Bearer {access_token}"

    while True:
        print("\n--- Memulai sesi ---")
        start_response = requests.post(START_SESSION_URL, headers=session_headers)
        print(f"Status code: {start_response.status_code}, respon: {start_response.text}")  # Logging detail respon
        
        if start_response.status_code in [200, 201]:
            session_id = start_response.json().get("sessionId")
            print("Sukses memulai sesi, sessionId:", session_id)
            time.sleep(30)

            virt_points = random.randint(48, 54)
            print(f"VirtPoints yang digunakan: {virt_points}")

            finish_payload = {
                "sessionId": session_id,
                "tapped": {
                    "virtMoney": virt_points,
                    "virtPoints": 0
                }
            }
            finish_response = requests.post(FINISH_SESSION_URL, headers=session_headers, data=json.dumps(finish_payload))
            if finish_response.status_code == 200:
                print("Sukses menyelesaikan sesi:", finish_response.json())
            else:
                print("Gagal menyelesaikan sesi:", finish_response.status_code, finish_response.text)
        else:
            # Jika gagal karena token, coba login kembali
            if start_response.status_code == 401:  # Unauthorized
                print("Token tidak valid, mencoba login kembali...")
                access_token = login()
                if access_token:
                    continue  # Coba lagi dengan token baru
            print("Gagal memulai sesi:", start_response.status_code, start_response.text)
        time.sleep(3)

# Fungsi untuk memulai perdagangan otomatis
def start_auto_trade(access_token):
    auto_trade_headers = headers.copy()
    auto_trade_headers["Authorization"] = f"Bearer {access_token}"

    response = requests.post(START_AUTO_TRADE_URL, headers=auto_trade_headers)
    if response.status_code == 201:
        auto_trade_id = response.json()["autoTradeId"]
        with open("autotrade.txt", "w") as file:
            file.write(auto_trade_id)
        print(f"Perdagangan otomatis berhasil dimulai! ID: {auto_trade_id}")
        return auto_trade_id
    print(f"Gagal memulai perdagangan otomatis. Kode status: {response.status_code}")
    return None

# Fungsi untuk mengklaim reward
def claim_reward(auto_trade_id, access_token):
    claim_headers = headers.copy()
    claim_headers["Authorization"] = f"Bearer {access_token}"
    payload = {"autoTradeId": auto_trade_id}

    response = requests.post(CLAIM_AUTO_TRADE_URL, headers=claim_headers, data=json.dumps(payload))
    if response.status_code == 201:
        print("Reward berhasil diklaim!", response.json())
    else:
        print(f"Gagal mengklaim reward. Kode status: {response.status_code}")

# Program utama
if __name__ == "__main__":
    token = login()
    if token:
        # Memulai sesi tapping
        start_session(token)

        # Memulai perdagangan otomatis
        auto_trade_id = start_auto_trade(token)
        if auto_trade_id:
            print("Menunggu selama 4 jam sebelum mengklaim reward...")
            time.sleep(14400)  # Tunggu 4 jam
            claim_reward(auto_trade_id, token)

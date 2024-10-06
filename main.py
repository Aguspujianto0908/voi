import requests
import random
import json
import time
import os
import threading

class Colors:
    RESET = "\033[0m"
    DARK_BLUE = "\033[94m"  # Warna biru tua
    GREEN = "\033[92m"      # Warna hijau
    RED = "\033[91m"        # Warna merah
    YELLOW = "\033[93m"     # Warna kuning

def print_pattern():
    # Define the pattern
    pattern = [
        " ██████    ██████   ███████   ██    ██  ██   ██",
        "██    ██  ██        ██    ██  ██    ██  ██  ██",
        "████████  ████████  ██    ██  ██    ██  █████",
        "██    ██        ██  ██    ██  ██    ██  ██  ██",
        "██    ██   ██████   ███████    ██████   ██   ██"
    ]

    # Adjust the pattern to fit the terminal width
    for line in pattern:
        print(Colors.DARK_BLUE + line + Colors.RESET)

# Menampilkan pola di awal
print_pattern()

# Memeriksa apakah file data.txt sudah ada dan memiliki konten
accounts = []
if not os.path.exists('data.txt') or os.stat('data.txt').st_size == 0:
    while True:
        name = input("Masukkan nama akun (atau ketik 'exit' untuk keluar): ")
        if name.lower() == 'exit':
            break
        token = input("Masukkan token otorisasi: ")
        
        # Menanyakan apakah ingin menggunakan proxy
        use_proxy = input("Apakah Anda ingin menggunakan proxy? (y/n): ").strip().lower()
        
        if use_proxy == 'y':
            proxy = input("Masukkan proxy (contoh: http://user:pass@ip:port) atau ketik 'no' untuk tidak menggunakan proxy: ")
            if proxy.lower() == 'no':
                proxy = ''  # Set proxy ke string kosong
        else:
            proxy = ''
        
        add_account_to_file(name, token, proxy)
        print(f"Akun '{name}' telah ditambahkan.\n")
else:
    accounts = edit_accounts_in_file()

# Fungsi untuk menjalankan tugas untuk setiap akun
def run_account_tasks(account):
    print(f"\n--- Iterasi untuk {account['name']} ---")
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {account['token']}",
        "Content-Length": "0",
        "Origin": "https://app.tg.vooi.io",
        "Referer": "https://app.tg.vooi.io/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
    }

    # Mengatur proxy jika ada
    proxies = {
        "http": account['proxy'],
        "https": account['proxy'],
    } if account['proxy'] else {}

    start_response = requests.post(start_url, headers=headers, proxies=proxies)

    if start_response.status_code in [200, 201]:
        start_data = start_response.json()
        session_id = start_data.get("sessionId")
        print("Sukses memulai sesi.")

        # Hitung mundur selama countdown_duration
        for i in range(countdown_duration, 0, -1):
            print(f"Menunggu {i} detik sebelum menyelesaikan sesi...", end='\r')
            time.sleep(1)

        print("Selesai menunggu.")

        virt_money = random.randint(48, 54)
        virt_points = 0

        finish_payload = {
            "sessionId": session_id,
            "tapped": {
                "virtMoney": virt_money,
                "virtPoints": virt_points
            }
        }

        finish_headers = headers.copy()
        finish_headers["Content-Type"] = "application/json"

        finish_response = requests.post(finish_url, headers=finish_headers, data=json.dumps(finish_payload), proxies=proxies)

        if finish_response.status_code in [200, 201]:
            finish_data = finish_response.json()
            tapped_money = finish_data['tapped'].get('virtMoney')
            print(f"Sukses menyelesaikan sesi. VirtMoney yang ditambahkan ke saldo: {tapped_money}")
        else:
            print("Gagal menyelesaikan sesi:", finish_response.status_code)
    else:
        print("Gagal memulai sesi:", start_response.status_code)

# Perulangan terus menerus jika ada akun yang valid
if accounts:
    while True:
        threads = []
        for account in accounts:
            thread = threading.Thread(target=run_account_tasks, args=(account,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Hitung mundur sebelum iterasi berikutnya
        for i in range(iteration_pause, 0, -1):
            print(f"Semua akun telah menjalankan tugas. Menunggu {i} detik sebelum iterasi berikutnya...", end='\r')
            time.sleep(1)

        print()  # Untuk membuat baris baru setelah hitung mundur selesai
else:
    print("Tidak ada akun yang valid untuk dijalankan.")

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
    pattern = [
        " ██████    ██████   ███████   ██    ██  ██   ██",
        "██    ██  ██        ██    ██  ██    ██  ██  ██",
        "████████  ████████  ██    ██  ██    ██  █████",
        "██    ██        ██  ██    ██  ██    ██  ██  ██",
        "██    ██   ██████   ███████    ██████   ██   ██"
    ]
    for line in pattern:
        print(Colors.DARK_BLUE + line + Colors.RESET)

def add_account_to_file(name, token, proxy):
    with open('data.txt', 'a') as file:
        file.write(f"{name},{token},{proxy}\n")

def edit_accounts_in_file():
    accounts = []
    if os.path.exists('data.txt'):
        with open('data.txt', 'r') as file:
            for line in file:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) == 3:  # Pastikan ada 3 elemen
                        name, token, proxy = parts
                        accounts.append({'name': name, 'token': token, 'proxy': proxy})
    return accounts

def save_accounts_to_file(accounts):
    with open('data.txt', 'w') as file:
        for account in accounts:
            file.write(f"{account['name']},{account['token']},{account['proxy']}\n")

def menu():
    print("Pilih opsi:")
    print("1. Tambah Akun")
    print("2. Edit Akun")
    print("3. Hapus Akun")
    print("4. Lihat Akun")
    print("5. Jalankan Tugas")
    print("6. Keluar")

def manage_accounts():
    accounts = edit_accounts_in_file()
    while True:
        menu()
        choice = input("Masukkan pilihan (1-6): ")
        
        if choice == '1':
            name = input("Masukkan nama akun: ")
            token = input("Masukkan token otorisasi: ")
            use_proxy = input("Apakah Anda ingin menggunakan proxy? (y/n): ").strip().lower()
            if use_proxy == 'y':
                proxy = input("Masukkan proxy (contoh: http://user:pass@ip:port) atau ketik 'no' untuk tidak menggunakan proxy: ")
                if proxy.lower() == 'no':
                    proxy = ''
            else:
                proxy = ''
            add_account_to_file(name, token, proxy)
            print(f"Akun '{name}' telah ditambahkan.\n")
        
        elif choice == '2':
            if not accounts:
                print("Tidak ada akun untuk diedit.")
                continue
            print("Akun yang tersedia:")
            for idx, account in enumerate(accounts):
                print(f"{idx + 1}. {account['name']}")
            idx = int(input("Masukkan nomor akun yang ingin diedit: ")) - 1
            if 0 <= idx < len(accounts):
                name = input("Masukkan nama akun baru: ")
                token = input("Masukkan token otorisasi baru: ")
                use_proxy = input("Apakah Anda ingin menggunakan proxy? (y/n): ").strip().lower()
                if use_proxy == 'y':
                    proxy = input("Masukkan proxy (contoh: http://user:pass@ip:port) atau ketik 'no' untuk tidak menggunakan proxy: ")
                    if proxy.lower() == 'no':
                        proxy = ''
                else:
                    proxy = ''
                accounts[idx] = {'name': name, 'token': token, 'proxy': proxy}
                save_accounts_to_file(accounts)
                print("Akun berhasil diedit.")
            else:
                print("Nomor akun tidak valid.")
        
        elif choice == '3':
            if not accounts:
                print("Tidak ada akun untuk dihapus.")
                continue
            print("Akun yang tersedia:")
            for idx, account in enumerate(accounts):
                print(f"{idx + 1}. {account['name']}")
            idx = int(input("Masukkan nomor akun yang ingin dihapus: ")) - 1
            if 0 <= idx < len(accounts):
                del accounts[idx]
                save_accounts_to_file(accounts)
                print("Akun berhasil dihapus.")
            else:
                print("Nomor akun tidak valid.")
        
        elif choice == '4':
            if not accounts:
                print("Tidak ada akun yang tersimpan.")
            else:
                print("Akun yang tersimpan:")
                for account in accounts:
                    print(f"Nama: {account['name']}, Token: {account['token']}, Proxy: {account['proxy']}")
        
        elif choice == '5':
            if not accounts:
                print("Tidak ada akun yang valid untuk dijalankan.")
            else:
                return accounts  # Kembali ke pemanggilan tugas jika ada akun yang valid
        
        elif choice == '6':
            print("Keluar dari program.")
            exit()
        
        else:
            print("Pilihan tidak valid.")

# Menampilkan pola di awal
print_pattern()

# Mengelola akun sebelum menjalankan tugas
accounts = manage_accounts()

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

    proxies = {
        "http": account['proxy'],
        "https": account['proxy'],
    } if account['proxy'] else {}

    start_url = "https://api-tg.vooi.io/api/tapping/start_session"
    finish_url = "https://api-tg.vooi.io/api/tapping/finish"
    countdown_duration = 30  # Hitung mundur sebelum menyelesaikan sesi
    iteration_pause = 3  # Waktu jeda antar iterasi

    start_response = requests.post(start_url, headers=headers, proxies=proxies)

    if start_response.status_code in [200, 201]:
        start_data = start_response.json()
        session_id = start_data.get("sessionId")
        print("Sukses memulai sesi.")

        for i in range(countdown_duration, 0, -1):
            print(f"Menunggu {i} detik sebelum menyelesaikan sesi...", end='\r')
            time.sleep(1)

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

        for i in range(3, 0, -1):
            print(f"Semua akun telah menjalankan tugas. Menunggu {i} detik sebelum iterasi berikutnya...", end='\r')
            time.sleep(1)

        print()  # Untuk membuat baris baru setelah hitung mundur selesai
else:
    print("Tidak ada akun yang valid untuk dijalankan.")

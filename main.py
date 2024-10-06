import threading
import time
import random

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

def run_account_tasks(account):
    # Simulasikan menjalankan tugas untuk setiap akun
    print(f"--- Iterasi untuk {account['name']} ---")
    print("Sukses memulai sesi.")
    virt_money = random.randint(48, 54)
    print(f"Sukses menyelesaikan sesi. VirtMoney yang ditambahkan ke saldo: {virt_money}")

# Menampilkan pola di awal
print_pattern()

# Contoh akun untuk demonstrasi
accounts = [{'name': 'budi kusuma'}, {'name': 'andi'}]

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

        print("Semua akun telah menjalankan tugas. Menunggu 3 detik sebelum iterasi berikutnya...")
else:
    print("Tidak ada akun yang valid untuk dijalankan.")

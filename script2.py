import os
import time
import hashlib
from datetime import datetime
from PIL import ImageGrab
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# -------------------------
# Configuration
# -------------------------
OUTPUT_DIR = "encrypted_screenshots"
TEMP_DIR = "temp_screens"
LOG_FILE = "log.txt"
DES_BLOCK_SIZE = 8

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# -------------------------
# Key Handling
# -------------------------
def get_des_key_from_user():
    while True:
        key_input = input("Enter 8-character DES key: ")
        if len(key_input) == 8:
            return key_input.encode()
        else:
            print("❌ Key must be exactly 8 characters.")

# -------------------------
# Encryption / Decryption
# -------------------------
def encrypt_des(data, key):
    cipher = DES.new(key, DES.MODE_CBC)
    encrypted = cipher.encrypt(pad(data, DES_BLOCK_SIZE))
    return cipher.iv + encrypted

def decrypt_des(encrypted_data, key):
    iv = encrypted_data[:DES_BLOCK_SIZE]
    cipher = DES.new(key, DES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted_data[DES_BLOCK_SIZE:]), DES_BLOCK_SIZE)

# -------------------------
# Hashing
# -------------------------
def calculate_sha256(data):
    return hashlib.sha256(data).hexdigest()

# -------------------------
# Screenshot Capture & Encrypt
# -------------------------
def capture_and_encrypt(interval, key):
    count = 1
    print(f"\n📸 Monitoring started — capturing every {interval} seconds (Ctrl+C to stop)\n")
    try:
        while True:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            raw_filename = f"screenshot_{timestamp}.png"
            temp_path = os.path.join(TEMP_DIR, raw_filename)

            # Take screenshot using Pillow
            screenshot = ImageGrab.grab()
            screenshot.save(temp_path)

            # Read and encrypt
            with open(temp_path, 'rb') as f:
                raw_data = f.read()
            encrypted_data = encrypt_des(raw_data, key)

            # Save encrypted file
            enc_filename = raw_filename + ".enc"
            enc_path = os.path.join(OUTPUT_DIR, enc_filename)
            with open(enc_path, 'wb') as f:
                f.write(encrypted_data)

            # Log hash
            hash_value = calculate_sha256(encrypted_data)
            with open(LOG_FILE, 'a') as log:
                log.write(f"{enc_filename} | {timestamp} | {hash_value}\n")

            os.remove(temp_path)
            print(f"[{count}] Screenshot captured, encrypted, and logged.")
            count += 1
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped.")

# -------------------------
# Decrypt & Verify
# -------------------------
def decrypt_and_verify(file_path, key):
    if not os.path.exists(file_path):
        print("❌ File not found.")
        return

    with open(file_path, 'rb') as f:
        encrypted_data = f.read()

    calculated_hash = calculate_sha256(encrypted_data)

    # Match with log
    with open(LOG_FILE, 'r') as log:
        lines = log.readlines()

    matched = False
    for line in lines:
        parts = [x.strip() for x in line.split('|')]
        if parts[0] == os.path.basename(file_path):
            logged_hash = parts[2]
            matched = True
            break

    if not matched:
        print("⚠️ No log entry found for this file.")
        return

    if calculated_hash != logged_hash:
        print("❌ Hash mismatch! File may be tampered.")
        return

    # Decrypt and save
    decrypted_data = decrypt_des(encrypted_data, key)
    out_path = file_path.replace(".enc", "_decrypted.png")
    with open(out_path, 'wb') as f:
        f.write(decrypted_data)

    print("✅ Hash verified.")
    print(f"🖼️ Decrypted screenshot saved as: {out_path}")

# -------------------------
# Main Menu
# -------------------------
if __name__ == "__main__":
    print("\n=== Screenshot Monitoring App (Pillow + DES + SHA-256) ===")
    print("1. Start Monitoring")
    print("2. Decrypt & Verify Screenshot")

    choice = input("Select an option (1 or 2): ")

    if choice == '1':
        interval = int(input("Enter interval (in seconds): "))
        key = get_des_key_from_user()
        capture_and_encrypt(interval, key)
    elif choice == '2':
        file_path = input("Enter full path of .enc file: ")
        key = get_des_key_from_user()
        decrypt_and_verify(file_path, key)
    else:
        print("❌ Invalid choice.")

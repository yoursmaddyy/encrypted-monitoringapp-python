# 🛡️ Encrypted Screenshot Monitoring App

A Python-based security tool that periodically takes encrypted desktop screenshots and logs metadata for secure monitoring and integrity verification.

---

## 🚀 Features

- 🖼️ Automated screenshot capture at regular intervals
- 🔐 AES encryption of screenshots for secure storage
- 🧾 SHA-256 hashing for integrity verification
- 📁 Log file tracking all actions (timestamps, filenames, hashes)
- 🔓 Decryption tool to view encrypted screenshots
- ✅ Hash verification to detect tampering

---

## 🛠️ Technologies Used

- Python 3
- [Pillow](https://pypi.org/project/Pillow/) – for capturing screenshots
- [PyCryptodome](https://pypi.org/project/pycryptodome/) – for AES encryption
- `hashlib`, `os`, `time`, `datetime` – built-in modules for core functions

---


---

## 🧪 How It Works

1. Run `main.py` to start monitoring
2. Every X seconds:
   - Takes a screenshot
   - Encrypts it with AES
   - Computes and stores a SHA-256 hash
   - Logs the entire event
3. Use included tools to decrypt and verify screenshots later

---

## ⚙️ Configuration

Edit `config.py` to modify:

- Screenshot interval (in seconds)
- AES secret key (must be 16, 24, or 32 bytes)
- Folder paths for storage

---

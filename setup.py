import os
import base64
import hashlib
import uuid
from cryptography.fernet import Fernet

LICENSE_FILE = "license.key"

# Encryption key (must be the same in tgtx.py)
SECRET_KEY = base64.urlsafe_b64encode(hashlib.sha256(b"my_secret_phrase").digest()[:32])

# Pre-approved activation keys
VALID_KEYS = [
    "A9D7KLMXRT52QWECNJ8VZ3HUB"  # First Mac PC
]

def get_hardware_id():
    """Generates a unique hardware ID (MAC address)."""
    return hashlib.sha256(uuid.getnode().to_bytes(6, 'big')).hexdigest()

def encrypt_data(data):
    """Encrypts data before saving it."""
    cipher = Fernet(SECRET_KEY)
    return cipher.encrypt(data.encode()).decode()

def setup_activation():
    """Handles activation before installation."""
    print("🔒 This software requires activation.")

    activation_key = input("Enter your activation key: ").strip().upper()
    if activation_key not in VALID_KEYS:
        print("❌ Invalid activation key. Please contact support.")
        exit()

    hardware_id = get_hardware_id()  # Get unique hardware ID
    license_data = f"{activation_key}:{hardware_id}"  # Store both key & hardware ID

    # Encrypt and save license
    with open(LICENSE_FILE, "w") as f:
        f.write(encrypt_data(license_data))

    print("✅ Activation successful! Proceeding with installation.")

if not os.path.exists(LICENSE_FILE):
    setup_activation()

# Install dependencies
print("[+] Installing requirements ...")
os.system('pip install termcolor colorama requests rich tgcrypto IP2Location pytz licensing pyfiglet pick asyncio configparser lolpython pyrogram telethon vobject geopy names Faker gender-guesser')

os.system('pip uninstall -y setuptools')
os.system('pip install setuptools==66.0.0')

print("[+] Setup complete!")
print("[+] Now you can run TGTX tool!")

import os
import json
import uuid
import hashlib

LICENSE_FILE = "licenses.json"

def get_hwid():
    mac = uuid.getnode()
    hwid = hashlib.sha256(str(mac).encode()).hexdigest()
    return hwid

def load_licenses():
    if not os.path.isfile(LICENSE_FILE):
        return {}
    with open(LICENSE_FILE, "r") as f:
        return json.load(f)

def save_licenses(data):
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def validate_key(input_key):
    valid_keys = {
        "00xsuhd798he87ghewyhdhasbds",
        "00xy9q23d98qyus798yduashdau",
        "00xsdh98u3whe97wqehriuyfhwu"
    }
    return input_key in valid_keys

def main():
    hwid = get_hwid()
    licenses = load_licenses()

    while True:
        input_key = input("Enter your license key (or type 'exit' to quit): ").strip()
        if input_key.lower() == 'exit':
            print("Exiting...")
            break

        if not validate_key(input_key):
            print("[ERROR] Invalid license key. Please try again.")
            continue  # retry

        if input_key in licenses:
            if licenses[input_key] == hwid:
                print("[OK] License key recognized for this machine. Access granted.")
                break
            else:
                print("[ERROR] License key already used on a different machine.")
                print(f"Your HWID: {hwid}")
                print(f"Registered HWID: {licenses[input_key]}")
                break
        else:
            licenses[input_key] = hwid
            save_licenses(licenses)
            print("[OK] License key registered to this machine. Access granted.")
            break

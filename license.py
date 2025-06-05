import os
import json
import uuid
import hashlib

LICENSE_FILE = "licenses.json"

def get_hwid():
    """
    Get a machine-specific HWID.
    Here we use the MAC address hashed for simplicity.
    """
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
    """
    Replace this function with your own license key validation logic.
    For demo: let's say valid keys are stored in a set.
    """
    valid_keys = {
        "ABCDEF-123456-XYZ789",
        "LICENSE-EXAMPLE-KEY123",
        "SAMPLE-KEY-000000"
    }
    return input_key in valid_keys

def main():
    hwid = get_hwid()
    licenses = load_licenses()

    input_key = input("Enter your license key: ").strip()

    if not validate_key(input_key):
        print("[ERROR] Invalid license key.")
        return

    if input_key in licenses:
        if licenses[input_key] == hwid:
            print("[OK] License key recognized for this machine. Access granted.")
        else:
            print("[ERROR] License key already used on a different machine.")
            print(f"Your HWID: {hwid}")
            print(f"Registered HWID: {licenses[input_key]}")
    else:
        # New license registration for this HWID
        licenses[input_key] = hwid
        save_licenses(licenses)
        print("[OK] License key registered to this machine. Access granted.")

if __name__ == "__main__":
    main()

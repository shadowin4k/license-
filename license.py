import json
import hashlib
import uuid
import os

LICENSE_FILE = "license.json"

VALID_KEYS = {
    "00xsuhd798he87ghewyhdhasbds",
    "00xy9q23d98qyus798yduashdau",
    "00xsdh98u3whe97wqehriuyfhwu",
    "00xujhnd78asyd7qhqdy7u2yhdu",
    "00xndsaudhsuad893dwqdwqdqwd"
}

def get_hwid():
    mac = uuid.getnode()
    return hashlib.sha256(str(mac).encode()).hexdigest()

def load_licenses():
    if not os.path.isfile(LICENSE_FILE):
        return {}
    with open(LICENSE_FILE, "r") as f:
        return json.load(f)

def save_licenses(data):
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def main():
    hwid = get_hwid()
    bound_licenses = load_licenses()

    # Check if HWID is already bound to a key
    for key, bound_hwid in bound_licenses.items():
        if bound_hwid == hwid:
            print(f"Your machine is already bound to license key: {key}")
            print("You cannot use a different license key on this machine.")
            return

    user_key = input("Enter your license key: ").strip()

    if user_key not in VALID_KEYS:
        print("Invalid license key.")
        return

    if user_key in bound_licenses and bound_licenses[user_key] != hwid:
        print("This license key is already bound to another machine.")
        return

    # Check if HWID already bound to a different key (redundant)
    for key, bound_hwid in bound_licenses.items():
        if bound_hwid == hwid and key != user_key:
            print("This machine is already bound to a different license key.")
            return

    # Bind the key to this HWID and save file (only now!)
    bound_licenses[user_key] = hwid
    save_licenses(bound_licenses)

    print(f"License key {user_key} successfully bound to this machine.")
    print("Access granted!")

if __name__ == "__main__":
    main()

import json
import hashlib
import uuid
import os

LICENSES_DB_FILE = "licenses_db.json"

# Your requested license keys (all unbound)
INITIAL_LICENSES = {
    "00xsuhd798he87ghewyhdhasbds": None,
    "00xy9q23d98qyus798yduashdau": None,
    "00xsdh98u3whe97wqehriuyfhwu": None,
    "00xujhnd78asyd7qhqdy7u2yhdu": None,
    "00xndsaudhsuad893dwqdwqdqwd": None
}

def get_hwid():
    mac = uuid.getnode()
    return hashlib.sha256(str(mac).encode()).hexdigest()

def load_licenses():
    if not os.path.exists(LICENSES_DB_FILE):
        with open(LICENSES_DB_FILE, "w") as f:
            json.dump(INITIAL_LICENSES, f)
        return INITIAL_LICENSES.copy()
    with open(LICENSES_DB_FILE, "r") as f:
        return json.load(f)

def save_licenses(data):
    with open(LICENSES_DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def main():
    hwid = get_hwid()
    licenses = load_licenses()

    # Check if this HWID is already bound to a key
    bound_key_for_hwid = None
    for key, bound_hwid in licenses.items():
        if bound_hwid == hwid:
            bound_key_for_hwid = key
            break

    if bound_key_for_hwid:
        print(f"Your machine is already bound to license key: {bound_key_for_hwid}")
        print("You cannot use a different license key on this machine.")
        return

    user_key = input("Enter your license key: ").strip()

    if user_key not in licenses:
        print("Invalid license key.")
        return

    if licenses[user_key] is not None and licenses[user_key] != hwid:
        print("This license key is already bound to another machine.")
        return

    # Double check if HWID already has a different key (redundant)
    for key, bound_hwid in licenses.items():
        if bound_hwid == hwid and key != user_key:
            print("This machine is already bound to a different license key.")
            return

    licenses[user_key] = hwid
    save_licenses(licenses)

    print(f"License key {user_key} successfully bound to this machine.")
    print("Access granted!")

if __name__ == "__main__":
    main()

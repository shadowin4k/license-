import json
import hashlib
import uuid
import os

LICENSE_FILE = "license.json"

# Your license keys initially unbound (None)
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
    if not os.path.isfile(LICENSE_FILE):
        with open(LICENSE_FILE, "w") as f:
            json.dump(INITIAL_LICENSES, f, indent=4)
        return INITIAL_LICENSES.copy()
    with open(LICENSE_FILE, "r") as f:
        return json.load(f)

def save_licenses(data):
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def main():
    hwid = get_hwid()
    licenses = load_licenses()

    # Check if this HWID already has a bound key
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

    # Double check if HWID already bound to another key (redundant)
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

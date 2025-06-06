import os
import uuid
import hashlib
import json

LICENSES_DB_FILE = "licenses_db.json"

# Valid license keys (not saved unless used)
VALID_LICENSE_KEYS = {
    "00xsuhd798he87ghewyhdhasbds",
    "00xy9q23d98qyus798yduashdau",
    "00xqwekj123jkqwej123kwej12",
    "00xasdfasfdasdfasdfsadfasdf",
}

def get_hwid():
    return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()

def load_licenses_db():
    if os.path.isfile(LICENSES_DB_FILE):
        with open(LICENSES_DB_FILE, "r") as f:
            return json.load(f)
    return {}  # Only used keys are stored

def save_licenses_db(data):
    with open(LICENSES_DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def find_key_by_hwid(licenses_db, hwid):
    for key, bound_hwid in licenses_db.items():
        if bound_hwid == hwid:
            return key
    return None

def main():
    hwid = get_hwid()
    licenses_db = load_licenses_db()

    # Prevent different key reuse on same HWID
    existing_key = find_key_by_hwid(licenses_db, hwid)
    if existing_key:
        print(f"This PC is already bound to license key: {existing_key}")
        print("You cannot use a different license key on this machine.")
        input("Press Enter to exit...")
        return

    key = input("Enter your license key:\n> ").strip()

    if key not in VALID_LICENSE_KEYS:
        print("Invalid license key.")
        input("Press Enter to exit...")
        return

    if key in licenses_db:
        if licenses_db[key] == hwid:
            print("License key recognized on this PC. Access granted.")
        else:
            print("This license key is already used on a different PC. Access denied.")
    else:
        # Bind new key
        licenses_db[key] = hwid
        save_licenses_db(licenses_db)
        print("License key accepted and bound to this PC. Access granted.")

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()

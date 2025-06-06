import os
import uuid
import hashlib

LICENSES_DB_FILE = "licenses_db.json"

# Predefined license keys - all unbound initially (value=None)
INITIAL_LICENSES = {
    "00xsuhd798he87ghewyhdhasbds": None,
    "00xy9q23d98qyus798yduashdau": None,
    "00xqwekj123jkqwej123kwej12": None,
    "00xasdfasfdasdfasdfsadfasdf": None,
}

def get_hwid():
    # Use MAC address hashed as HWID
    mac = uuid.getnode()
    hwid = hashlib.sha256(str(mac).encode()).hexdigest()
    return hwid

def load_licenses_db():
    if not os.path.isfile(LICENSES_DB_FILE):
        # If file doesn't exist, initialize with INITIAL_LICENSES
        return INITIAL_LICENSES.copy()
    with open(LICENSES_DB_FILE, "r") as f:
        return json.load(f)

def save_licenses_db(data):
    with open(LICENSES_DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def find_key_by_hwid(licenses_db, hwid):
    # Check if this HWID is already bound to any key
    for key, bound_hwid in licenses_db.items():
        if bound_hwid == hwid:
            return key
    return None

def main():
    hwid = get_hwid()
    licenses_db = load_licenses_db()

    # Check if this HWID already has a license bound
    existing_key = find_key_by_hwid(licenses_db, hwid)
    if existing_key:
        print(f"This PC is already bound to license key: {existing_key}")
        print("You cannot use a different license key on this machine.")
        input("Press Enter to exit...")
        return

    # Otherwise ask user to input license key
    key = input("Enter your license key:\n> ").strip()

    if key not in licenses_db:
        print("Invalid license key.")
        input("Press Enter to exit...")
        return

    if licenses_db[key] is None:
        # License key is unbound, bind it now to this HWID
        licenses_db[key] = hwid
        save_licenses_db(licenses_db)
        print("License key accepted and bound to this PC. Access granted.")
    else:
        # License key already bound to some HWID
        if licenses_db[key] == hwid:
            # Same HWID: allow usage
            print("License key recognized on this PC. Access granted.")
        else:
            # Different HWID: reject usage
            print("This license key is already used on a different PC. Access denied.")

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()

import os
import json
import uuid
import hashlib
import sys

LICENSE_FILE = "license.json"          # stores only current license key + hwid for this machine
LICENSES_DB_FILE = "licenses_db.json" # stores all license keys and their HWID bindings

# Initial license keys, all unbound (None means unbound)
INITIAL_LICENSES = {
    "00xsuhd798he87ghewyhdhasbds": None,
    "00xy9q23d98qyus798yduashdau": None,
    "00xsdh98u3whe97wqehriuyfhwu": None,
    "00xujhnd78asyd7qhqdy7u2yhdu": None,
    "00xndsaudhsuad893dwqdwqdqwd": None
}

def get_hwid():
    return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()

def load_local_license():
    if os.path.isfile(LICENSE_FILE):
        with open(LICENSE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_local_license(key, hwid):
    with open(LICENSE_FILE, "w") as f:
        json.dump({"key": key, "hwid": hwid}, f)

def load_licenses_db():
    if os.path.isfile(LICENSES_DB_FILE):
        with open(LICENSES_DB_FILE, "r") as f:
            return json.load(f)
    else:
        # Save initial licenses if DB file doesn't exist
        with open(LICENSES_DB_FILE, "w") as f:
            json.dump(INITIAL_LICENSES, f)
        return INITIAL_LICENSES.copy()

def save_licenses_db(db):
    with open(LICENSES_DB_FILE, "w") as f:
        json.dump(db, f)

def main():
    current_hwid = get_hwid()
    local = load_local_license()
    licenses_db = load_licenses_db()

    # If local license exists and HWID matches current machine, valid
    if local.get("key") and local.get("hwid") == current_hwid:
        # Verify that license is still bound in DB to this HWID (consistency check)
        bound_hwid = licenses_db.get(local["key"])
        if bound_hwid == current_hwid:
            print("[*] License already activated and valid.")
            sys.exit(0)
        else:
            print("[-] Local license does not match server record. Please reactivate.")
            # We allow fall-through to ask for license input

    # If local license exists but HWID differs, deny to prevent key switching on same machine
    if local.get("key") and local.get("hwid") != current_hwid:
        print("[-] License key found for different machine on this device. Access denied.")
        sys.exit(1)

    # Prevent multiple keys bound to same HWID (check DB)
    for key, hwid in licenses_db.items():
        if hwid == current_hwid:
            print(f"[*] This machine is already bound to license key: {key}")
            # Save local license for consistency
            save_local_license(key, current_hwid)
            sys.exit(0)

    # Ask user for license key input
    print("Enter your license key:")
    key = input("> ").strip()

    # Validate key existence
    if key not in licenses_db:
        print("[-] Invalid key.")
        sys.exit(1)

    # Check if key is already bound to a different HWID
    bound_hwid = licenses_db.get(key)
    if bound_hwid is None:
        # Key is free - bind to this HWID
        licenses_db[key] = current_hwid
        save_licenses_db(licenses_db)
        save_local_license(key, current_hwid)
        print("[+] License activated successfully.")
        sys.exit(0)
    elif bound_hwid == current_hwid:
        # Key already bound to this HWID
        save_local_license(key, current_hwid)
        print("[*] License already activated and valid.")
        sys.exit(0)
    else:
        print("[-] This key is already used on another machine.")
        sys.exit(1)

if __name__ == "__main__":
    main()

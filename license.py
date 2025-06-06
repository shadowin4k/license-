import os
import json
import uuid
import hashlib
import sys

LICENSE_FILE = "license.json"          # stores current license key + hwid for this machine
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
    # Use MAC address hashed as HWID
    mac = uuid.getnode()
    return hashlib.sha256(str(mac).encode()).hexdigest()

def load_local_license():
    if os.path.isfile(LICENSE_FILE):
        try:
            with open(LICENSE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("[-] Local license file is corrupted.")
            return {}
    return {}

def save_local_license(key, hwid):
    with open(LICENSE_FILE, "w") as f:
        json.dump({"key": key, "hwid": hwid}, f, indent=4)
        f.flush()

def load_licenses_db():
    if os.path.isfile(LICENSES_DB_FILE):
        try:
            with open(LICENSES_DB_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("[-] Licenses DB file is corrupted. Resetting to initial licenses.")
            save_licenses_db(INITIAL_LICENSES)
            return INITIAL_LICENSES.copy()
    else:
        # Save initial licenses if DB file doesn't exist
        save_licenses_db(INITIAL_LICENSES)
        return INITIAL_LICENSES.copy()

def save_licenses_db(db):
    with open(LICENSES_DB_FILE, "w") as f:
        json.dump(db, f, indent=4)
        f.flush()

def main():
    current_hwid = get_hwid()
    local = load_local_license()
    licenses_db = load_licenses_db()

    # Check if local license exists and matches current machine HWID
    if local.get("key") and local.get("hwid") == current_hwid:
        bound_hwid = licenses_db.get(local["key"])
        if bound_hwid == current_hwid:
            print("[*] License already activated and valid.")
            sys.exit(0)
        else:
            print("[-] Local license does not match server record. Please reactivate.")

    # If local license exists but HWID differs, deny access
    if local.get("key") and local.get("hwid") != current_hwid:
        print("[-] License key found for different machine on this device. Access denied.")
        sys.exit(1)

    # Check if current HWID is already bound to a license in the DB
    for key, hwid in licenses_db.items():
        if hwid == current_hwid:
            print(f"[*] This machine is already bound to license key: {key}")
            save_local_license(key, current_hwid)  # sync local license file
            sys.exit(0)

    # Ask user for license key
    print("Enter your license key:")
    key = input("> ").strip()

    if key not in licenses_db:
        print("[-] Invalid key.")
        sys.exit(1)

    bound_hwid = licenses_db.get(key)
    if bound_hwid is None:
        # Key is free to bind
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
        # Key bound to different HWID
        print("[-] This key is already used on another machine.")
        sys.exit(1)

if __name__ == "__main__":
    main()

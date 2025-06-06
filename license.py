import os
import json
import uuid
import hashlib
import sys

LICENSE_FILE = "license.json"        # local cache for current machine
LICENSES_DB_FILE = "licenses_db.json" # initial license keys list (all unbound)

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
    print(f"Loading local license from {LICENSE_FILE}")
    if os.path.isfile(LICENSE_FILE):
        with open(LICENSE_FILE, "r") as f:
            data = json.load(f)
            print(f"Local license loaded: {data}")
            return data
    return {}

def save_local_license(key, hwid):
    print(f"Saving local license key={key} hwid={hwid} to {LICENSE_FILE}")
    with open(LICENSE_FILE, "w") as f:
        json.dump({"key": key, "hwid": hwid}, f)


def load_licenses_db():
    # Load static initial license keys; if missing, create with INITIAL_LICENSES
    if os.path.isfile(LICENSES_DB_FILE):
        with open(LICENSES_DB_FILE, "r") as f:
            return json.load(f)
    else:
        with open(LICENSES_DB_FILE, "w") as f:
            json.dump(INITIAL_LICENSES, f)
        return INITIAL_LICENSES.copy()

def main():
    current_hwid = get_hwid()
    local = load_local_license()
    licenses_db = load_licenses_db()  # Just keys with None values (unbound)

    # If local license exists and HWID matches current machine, valid
    if local.get("key") and local.get("hwid") == current_hwid:
        print("[*] License already activated and valid.")
        sys.exit(0)

    # If local license exists but HWID differs, deny to prevent key switching on same machine
    if local.get("key") and local.get("hwid") != current_hwid:
        print("[-] License key found for different machine on this device. Access denied.")
        sys.exit(1)

    # Prevent multiple keys bound to same HWID (check local license only since no DB updates)
    if local.get("hwid") == current_hwid:
        print(f"[*] This machine is already bound to license key: {local.get('key')}")
        sys.exit(0)

    # Ask user for license key input
    print("Enter your license key:")
    key = input("> ").strip()

    # Validate key existence in initial keys list
    if key not in licenses_db:
        print("[-] Invalid key.")
        sys.exit(1)

    # Check if key is already used on a different HWID (using local license file only)
    if local.get("key") == key and local.get("hwid") != current_hwid:
        print("[-] This key is already used on another machine.")
        sys.exit(1)

    # If no local license or the same key on this machine, save local license file only
    save_local_license(key, current_hwid)
    print("[+] License activated successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()

import os
import json
import uuid
import hashlib
import sys

LICENSE_FILE = "license.json"

# Hardcoded valid keys
VALID_KEYS = {
    "00xsuhd798he87ghewyhdhasbds",
    "00xy9q23d98qyus798yduashdau",
    "00xsdh98u3whe97wqehriuyfhwu",
    "00xujhnd78asyd7qhqdy7u2yhdu",
    "00xndsaudhsuad893dwqdwqdqwd"
}

def get_hwid():
    return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()

def load_local_license():
    if os.path.isfile(LICENSE_FILE):
        with open(LICENSE_FILE, "r") as f:
            return json.load(f)
    return None

def save_local_license(key, hwid):
    with open(LICENSE_FILE, "w") as f:
        json.dump({"key": key, "hwid": hwid}, f)

def main():
    current_hwid = get_hwid()
    local = load_local_license()

    if local:
        saved_key = local.get("key")
        saved_hwid = local.get("hwid")

        if saved_hwid != current_hwid:
            print("[-] License key is bound to a different machine. Access denied.")
            sys.exit(1)

        # HWID matches, so license is valid
        print(f"[*] License key '{saved_key}' already activated on this machine.")
        sys.exit(0)

    # No license file - ask for key
    print("Enter your license key:")
    key = input("> ").strip()

    if key not in VALID_KEYS:
        print("[-] Invalid license key.")
        sys.exit(1)

    # Save the key and HWID locally
    save_local_license(key, current_hwid)
    print("[+] License activated successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()

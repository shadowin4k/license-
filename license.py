import os
import json
import uuid
import hashlib
import sys

# Hardcoded license keys
LICENSES = {
    "00xsuhd798he87ghewyhdhasbds": None,
    "00xy9q23d98qyus798yduashdau": None,
    "00xsdh98u3whe97wqehriuyfhwu": None,
    "00xujhnd78asyd7qhqdy7u2yhdu": None,
    "00xndsaudhsuad893dwqdwqdqwd": None
}

LICENSE_FILE = "license.json"

def get_hwid():
    """Generate a SHA-256 hashed hardware ID using the machine's MAC address."""
    return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()

def load_local_license():
    """Load locally saved license data from license.json."""
    if os.path.isfile(LICENSE_FILE):
        with open(LICENSE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_local_license(key, hwid):
    """Save license and HWID binding to local file."""
    with open(LICENSE_FILE, "w") as f:
        json.dump({"key": key, "hwid": hwid}, f)

def main():
    current_hwid = get_hwid()
    local = load_local_license()

    if local.get("key") and local.get("hwid") == current_hwid:
        print("[*] License already activated and valid.")
        sys.exit(0)

    print("Enter your license key:")
    key = input("> ").strip()

    if key not in LICENSES:
        print("[-] Invalid key.")
        sys.exit(1)

    bound_hwid = LICENSES[key]
    if bound_hwid is None or bound_hwid == current_hwid:
        LICENSES[key] = current_hwid
        save_local_license(key, current_hwid)
        print("[+] License activated successfully.")
        sys.exit(0)
    else:
        print("[-] This key is already used on another machine.")
        sys.exit(1)

if __name__ == "__main__":
    main()

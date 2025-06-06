import uuid
import hashlib
import sys

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

def main():
    current_hwid = get_hwid()
    licenses_db = INITIAL_LICENSES.copy()  # In-memory licenses, no file loading
    local_license = {}  # Simulate local license cache in memory

    # If local license exists and HWID matches current machine, valid
    if local_license.get("key") and local_license.get("hwid") == current_hwid:
        print("[*] License already activated and valid.")
        sys.exit(0)

    # If local license exists but HWID differs, deny to prevent key switching on same machine
    if local_license.get("key") and local_license.get("hwid") != current_hwid:
        print("[-] License key found for different machine on this device. Access denied.")
        sys.exit(1)

    # Prevent multiple keys bound to same HWID (check local license only since no DB updates)
    if local_license.get("hwid") == current_hwid:
        print(f"[*] This machine is already bound to license key: {local_license.get('key')}")
        sys.exit(0)

    # Ask user for license key input
    print("Enter your license key:")
    key = input("> ").strip()

    # Validate key existence in initial keys list
    if key not in licenses_db:
        print("[-] Invalid key.")
        sys.exit(1)

    # Check if key is already used on a different HWID (local_license only)
    if local_license.get("key") == key and local_license.get("hwid") != current_hwid:
        print("[-] This key is already used on another machine.")
        sys.exit(1)

    # Bind license key to current HWID in memory (simulate saving local license)
    local_license["key"] = key
    local_license["hwid"] = current_hwid

    print("[+] License activated successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()

import os
import json
import uuid
import hashlib
import sys

LICENSES = {
    "ABC123-DEF456-GHI789": None,  # Initially unbound
    "XYZ987-UVW654-RST321": None
}

LICENSE_FILE = "license.json"

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

def main():
    local = load_local_license()
    current_hwid = get_hwid()

    if "key" in local and "hwid" in local:
        if local["hwid"] == current_hwid and LICENSES.get(local["key"]) in [None, current_hwid]:
            print("[*] License already activated and valid.")
            sys.exit(0)  # success
        else:
            print("[!] License mismatch or used on another machine.")
            input("Press any key to exit...")
            sys.exit(1)

    print("Enter your license key:")
    key = input("> ").strip()

    if key not in LICENSES:
        print("Invalid key. Access denied.")
        sys.exit(1)

    bound_hwid = LICENSES[key]
    if bound_hwid is None:
        LICENSES[key] = current_hwid
        save_local_license(key, current_hwid)
        print("[+] License activated successfully.")
        sys.exit(0)
    elif bound_hwid == current_hwid:
        save_local_license(key, current_hwid)
        print("[+] License recognized.")
        sys.exit(0)
    else:
        print("[-] This key is already used on another machine.")
        input("Press any key to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()

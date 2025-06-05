import os
import json
import uuid
import hashlib

LICENSE_FILE = "licenses.json"


def get_hwid():
    """Generate HWID by hashing MAC address."""
    mac = uuid.getnode()
    hwid = hashlib.sha256(str(mac).encode()).hexdigest()
    return hwid


def load_licenses():
    """Load license data from JSON file."""
    if not os.path.isfile(LICENSE_FILE):
        return {}
    with open(LICENSE_FILE, "r") as f:
        return json.load(f)


def save_licenses(data):
    """Save license data to JSON file."""
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def is_key_valid(key, hwid, licenses):
    """
    Check if key is valid:
    - If key not in licenses: invalid
    - If key is registered to this HWID: valid
    - If key registered to another HWID: invalid
    """
    if key not in licenses:
        return False, "Key does not exist."
    if licenses[key] == hwid:
        return True, "Key is valid for this machine."
    else:
        return False, "Key already registered to another machine."


def register_key(key, hwid, licenses):
    """Register a key to this machine's HWID."""
    licenses[key] = hwid
    save_licenses(licenses)


def get_registered_key(hwid, licenses):
    """Return key registered for this HWID if any."""
    for key, registered_hwid in licenses.items():
        if registered_hwid == hwid:
            return key
    return None


def main():
    hwid = get_hwid()
    licenses = load_licenses()

    # Check if this machine already has a registered key
    existing_key = get_registered_key(hwid, licenses)
    if existing_key:
        print(f"Your machine is already registered with key: {existing_key}")
        return

    print("Enter your license key:")
    entered_key = input("> ").strip()

    valid, msg = is_key_valid(entered_key, hwid, licenses)
    if valid:
        print("Key is already registered to this machine. Access granted.")
    else:
        if msg == "Key does not exist.":
            print("Invalid key. Access denied.")
        elif msg == "Key already registered to another machine.":
            print("This key is already used on another machine. Access denied.")
        else:
            # Key exists but not registered to this HWID - register it now
            print("Registering this key to your machine...")
            register_key(entered_key, hwid, licenses)
            print("Registration successful. Access granted.")


if __name__ == "__main__":
    main()

import uuid
import hashlib

# Hardcoded license keys with HWID bindings (empty string means unregistered)
licenses = {
    "ABC123-DEF456-GHI789": "",
    "XYZ987-UVW654-RST321": "",
    "MYKEY-0001-HELLO": ""
}

def get_hwid():
    """Generate HWID by hashing the MAC address."""
    mac = uuid.getnode()
    hwid = hashlib.sha256(str(mac).encode()).hexdigest()
    return hwid

def is_key_valid(key, hwid):
    """
    Check if the license key is valid and whether it's registered to this machine.
    Returns (bool valid, str message).
    """
    if key not in licenses:
        return False, "Key does not exist."
    if licenses[key] == "":
        # Key is valid but not registered yet
        return True, "Key is valid and unregistered."
    elif licenses[key] == hwid:
        # Key is valid and registered to this HWID
        return True, "Key is valid for this machine."
    else:
        # Key registered to a different machine
        return False, "Key already registered to another machine."

def register_key(key, hwid):
    """Register the license key to this machine's HWID."""
    licenses[key] = hwid

def get_registered_key(hwid):
    """Return the license key registered for this HWID, or None if none."""
    for key, registered_hwid in licenses.items():
        if registered_hwid == hwid:
            return key
    return None

def main():
    hwid = get_hwid()
    existing_key = get_registered_key(hwid)
    if existing_key:
        print(f"Your machine is already registered with key: {existing_key}")
        print("Access granted.")
        return

    while True:
        entered_key = input("Enter your license key (or type 'exit' to quit): ").strip()
        if entered_key.lower() == "exit":
            print("Exiting...")
            break

        valid, msg = is_key_valid(entered_key, hwid)
        if valid:
            if licenses[entered_key] == "":
                register_key(entered_key, hwid)
                print("Registration successful. Access granted.")
            else:
                print("Key is already registered to this machine. Access granted.")
            break
        else:
            print(f"Access denied: {msg}")

if __name__ == "__main__":
    main()

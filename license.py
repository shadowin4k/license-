import uuid
import hashlib

# Hardcoded licenses: key -> hwid (empty string means unregistered)
licenses = {
    "ABC123-DEF456-GHI789": "",
    "XYZ987-UVW654-RST321": "",
    "MYKEY-0001-HELLO": ""
}

def get_hwid():
    mac = uuid.getnode()
    hwid = hashlib.sha256(str(mac).encode()).hexdigest()
    return hwid

def is_key_valid(key, hwid):
    if key not in licenses:
        return False, "Key does not exist."
    if licenses[key] == "":
        # Key is valid but unregistered, can register now
        return True, "Key is valid and unregistered."
    elif licenses[key] == hwid:
        # Key is valid and registered to this HWID
        return True, "Key is valid for this machine."
    else:
        # Key is registered to another machine
        return False, "Key already registered to another machine."

def register_key(key, hwid):
    licenses[key] = hwid

def get_registered_key(hwid):
    for key, registered_hwid in licenses.items():
        if registered_hwid == hwid:
            return key
    return None

def main():
    hwid = get_hwid()
    existing_key = get_registered_key(hwid)
    if existing_key:
        print(f"Your machine is already registered with key: {existing_key}")
        return

    while True:
        entered_key = input("Enter your license key (or type 'exit' to quit): ").strip()
        if entered_key.lower() == "exit":
            print("Exiting...")
            break

        valid, msg = is_key_valid(entered_key, hwid)
        if valid:
            if licenses[entered_key] == "":
                # Register this key now
                register_key(entered_key, hwid)
                print("Registration successful. Access granted.")
            else:
                print("Key is already registered to this machine. Access granted.")
            break
        else:
            print(f"Access denied: {msg}")

if __name__ == "__main__":
    main()

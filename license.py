import os
import uuid
import hashlib
import json
import sys
import argparse
import re
from typing import Dict, Optional

# Local license database file
LICENSES_FILE = "your_licenses_DO_NOT_DELETE.json"

# Hardcoded valid license keys (replace with server validation in production)
VALID_LICENSE_KEYS = {
    "0x783624",
    "0x1a2b3c",
    "0xabcdef",
    "0x987654",
}

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_hwid() -> str:
    """Generate a stable HWID based on system identifiers."""
    try:
        mac = str(uuid.getnode())
        hostname = os.popen('hostname').read().strip()
        cpu_info = os.popen('wmic cpu get ProcessorId' if os.name == 'nt' else 'cat /proc/cpuinfo').read().strip()
        combined = f"{mac}:{hostname}:{cpu_info}"
        return hashlib.sha256(combined.encode()).hexdigest()
    except Exception as e:
        print(f"Error generating HWID: {e}")
        sys.exit(1)

def load_license_data() -> Dict[str, str]:
    """Load the local license data."""
    if not os.path.isfile(LICENSES_FILE):
        return {}
    try:
        with open(LICENSES_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, PermissionError, OSError) as e:
        print(f"Error loading license data: {e}")
        return {}

def save_license_data(data: Dict[str, str]) -> bool:
    """Save the local license data."""
    try:
        with open(LICENSES_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except (PermissionError, OSError) as e:
        print(f"Error saving license data: {e}")
        return False

def find_key_by_hwid(license_data: Dict[str, str], hwid: str) -> Optional[str]:
    """Find a license key bound to the given HWID."""
    return next((key for key, bound_hwid in license_data.items() if bound_hwid == hwid), None)

def validate_key_format(key: str) -> bool:
    """Check that the key matches 0x###### format."""
    return bool(re.match(r'^0x[0-9a-fA-F]{6}$', key))

def validate_key_server(key: str) -> bool:
    """Validate license key (placeholder for server validation)."""
    return key in VALID_LICENSE_KEYS

def get_license_key() -> Optional[str]:
    """Safely get license key from input, environment variable, or command-line argument."""
    parser = argparse.ArgumentParser(description="License Key Validation")
    parser.add_argument('--key', type=str, help='License key')
    args = parser.parse_args()

    if args.key:
        print("Using license key from command-line argument")
        return args.key.strip()

    key = os.environ.get('LICENSE_KEY')
    if key:
        print("Using license key from environment variable")
        return key.strip()

    try:
        return input("Enter your license key:\n> ").strip()
    except EOFError:
        print("Error: Input stream closed.")
        return None
    except KeyboardInterrupt:
        print("Input interrupted by user. Exiting.")
        sys.exit(1)

def main() -> int:
    """Main license validation logic."""
    hwid = get_hwid()
    license_data = load_license_data()

    existing_key = find_key_by_hwid(license_data, hwid)
    if existing_key:
        print(f"This PC is already bound to license key: {existing_key}")
        print("Access granted.")
        return 0

    while True:
        clear_screen()
        print("License verification[+]")

        key = get_license_key()
        if not key:
            continue
        if not validate_key_format(key):
            print("Invalid key format. Must be 0x followed by 6 hexadecimal digits.")
            input("Press Enter to try again...")
            continue
        if not validate_key_server(key):
            print("Invalid license key.")
            input("Press Enter to try again...")
            continue

        if key in license_data:
            if license_data[key] == hwid:
                print("License key recognized on this PC. Access granted.")
                return 0
            else:
                print("This license key is already used on a different PC.")
                input("Press Enter to try again...")
                continue

        license_data[key] = hwid
        if save_license_data(license_data):
            print("License key accepted and bound to this PC. Access granted.")
            return 0
        else:
            print("Failed to save license data. Access denied.")
            input("Press Enter to try again...")
            continue

if __name__ == "__main__":
    sys.exit(main())

import os
import uuid
import hashlib
import json
import sys
import argparse
import re
from typing import Dict, Optional

LICENSES_DB_FILE = "licenses_db.json"

# Hardcoded license keys in the format 0x###### (6 hex digits)
# Replace with server-based validation for production
VALID_LICENSE_KEYS = {
    "0x783624",
    "0x1a2b3c",
    "0xabcdef",
    "0x987654",
}

def get_hwid() -> str:
    """Generate a stable HWID based on multiple system identifiers."""
    try:
        mac = str(uuid.getnode())  # MAC address
        hostname = os.popen('hostname').read().strip()  # Hostname
        cpu_info = os.popen('wmic cpu get ProcessorId' if os.name == 'nt' else 'cat /proc/cpuinfo').read().strip()  # CPU info
        combined = f"{mac}:{hostname}:{cpu_info}"
        return hashlib.sha256(combined.encode()).hexdigest()
    except Exception as e:
        print(f"Error generating HWID: {e}")
        sys.exit(1)

def load_licenses_db() -> Dict[str, str]:
    """Load the licenses database from file, handling errors."""
    if not os.path.isfile(LICENSES_DB_FILE):
        return {}
    try:
        with open(LICENSES_DB_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, PermissionError, OSError) as e:
        print(f"Error loading licenses database: {e}")
        return {}

def save_licenses_db(data: Dict[str, str]) -> bool:
    """Save the licenses database to file, handling errors."""
    try:
        with open(LICENSES_DB_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except (PermissionError, OSError) as e:
        print(f"Error saving licenses database: {e}")
        return False

def find_key_by_hwid(licenses_db: Dict[str, str], hwid: str) -> Optional[str]:
    """Find a license key bound to the given HWID."""
    return next((key for key, bound_hwid in licenses_db.items() if bound_hwid == hwid), None)

def validate_key_format(key: str) -> bool:
    """Validate that the key matches the format 0x###### (6 hex digits)."""
    return bool(re.match(r'^0x[0-9a-fA-F]{6}$', key))

def validate_key_server(key: str) -> bool:
    """Placeholder for server-based key validation (e.g., for Network Security Dashboard)."""
    # Example: Replace with API call to your Express server
    # try:
    #     response = requests.post('http://your-server/api/validate-license', json={'key': key})
    #     return response.status_code == 200
    # except requests.RequestException as e:
    #     print(f"Server validation failed: {e}")
    #     return False
    return key in VALID_LICENSE_KEYS

def get_license_key() -> Optional[str]:
    """Safely get license key from input, environment variable, or command-line argument."""
    # Check command-line argument
    parser = argparse.ArgumentParser(description="License Key Validation")
    parser.add_argument('--key', type=str, help='License key')
    args = parser.parse_args()
    if args.key:
        print("Using license key from command-line argument")
        return args.key.strip()

    # Check environment variable
    key = os.environ.get('LICENSE_KEY')
    if key:
        print("Using license key from environment variable")
        return key.strip()

    # Fallback to interactive input
    try:
        return input("Enter your license key:\n> ").strip()
    except EOFError:
        print("Error: Input stream closed. Provide a license key via --key, LICENSE_KEY environment variable, or run interactively.")
        return None
    except KeyboardInterrupt:
        print("Input interrupted by user. Exiting.")
        sys.exit(1)

def main() -> int:
    """Main function for license validation."""
    hwid = get_hwid()
    licenses_db = load_licenses_db()

    # Check if HWID is already bound to a key
    existing_key = find_key_by_hwid(licenses_db, hwid)
    if existing_key:
        print(f"This PC is already bound to license key: {existing_key}")
        print("Access granted.")
        return 0  # Success (proceeds to LEINON :banner)

    # Prompt for key with up to 10,000 attempts
    max_attempts = 10000
    for attempt in range(1, max_attempts + 1):
        key = get_license_key()
        if not key:
            continue
        if not validate_key_format(key):
            print("Invalid key format. Must be 0x followed by 6 hexadecimal digits.")
            continue
        if not validate_key_server(key):
            print("Invalid license key.")
            continue

        # Check if key is already used
        if key in licenses_db:
            if licenses_db[key] == hwid:
                print("License key recognized on this PC. Access granted.")
                return 0  # Success (proceeds to LEINON :banner)
            else:
                print("This license key is already used on a different PC. Access denied.")
                print("Please try another key.")
                continue

        # Bind new key
        licenses_db[key] = hwid
        if save_licenses_db(licenses_db):
            print("License key accepted and bound to this PC. Access granted.")
            return 0  # Success (proceeds to LEINON :banner)
        else:
            print("Failed to save license database. Access denied.")
            print("Please try again.")
            continue

    print(f"Failed after {max_attempts} attempts. Exiting.")
    return 1  # Failure (does not proceed to :banner)

if __name__ == "__main__":
    sys.exit(main())

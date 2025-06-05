import os
import json
import uuid
import hashlib

LICENSE_FILE = "licenses.json"

def get_hwid():
    mac = uuid.getnode()
    hwid = hashlib.sha256(str(mac).encode()).hexdigest()
    return hwid

def load_licenses():
    if not os.path.isfile(LICENSE_FILE):
        return {}
    with open(LICENSE_FILE, "r") as f:
        return json.load(f)

def save_licenses(data):
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def validate_key(input_key):
    valid_keys = {
        "00xsuhd798he87ghewyhdhasbds",
        "00xy9q23d98qyus798yduashdau",
        "00xsdh98u3whe97wqehriuyfhwu"
    }
    return input_key in valid_keys

            break

#!/usr/bin/env python3
import os, sys, time, json, glob
import requests
import serial
from serial import SerialException

# ---- Configure via env or edit defaults ----
TOKEN = os.getenv("UBIDOTS_TOKEN", "PUT-YOUR-TOKEN-HERE")
DEVICE_LABEL = os.getenv("UBIDOTS_DEVICE", "machine-a")
PORT_HINT = os.getenv("NANO_PORT", "")  # e.g., "/dev/cu.usbmodem113101" or Windows: "COM3" or "COM5"
BAUD = int(os.getenv("NANO_BAUD", "115200"))
UBIDOTS_URL = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/"
HEADERS = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

PORT_PATTERNS = []
if PORT_HINT:
    PORT_PATTERNS.append(PORT_HINT)
# Prefer cu.* on macOS for initiating connections
PORT_PATTERNS += ["/dev/cu.usbmodem*", "/dev/tty.usbmodem*"]

def find_port():
    for pat in PORT_PATTERNS:
        if "*" in pat:
            matches = sorted(glob.glob(pat))
            if matches:
                return matches[0]
        else:
            return pat
    return None

def open_serial_with_retry(retries=6, delay=1.2):
    last_err = None
    for i in range(retries):
        port = find_port()
        if not port:
            last_err = "No serial port found. Set NANO_PORT or plug the board."
            time.sleep(delay)
            continue
        try:
            # Open the port
            ser = serial.Serial(port, BAUD, timeout=2)
            # Give the board a moment after the port opens
            time.sleep(0.5)
            return ser
        except SerialException as e:
            msg = str(e)
            last_err = msg
            # Common “busy” case on macOS/Linux
            if "Resource busy" in msg or "busy" in msg.lower():
                print("\n⚠️  Port busy! Close Arduino Serial Monitor or Serial Plotter and rerun this script.\n", file=sys.stderr)
                break
            time.sleep(delay)
    raise RuntimeError(f"Could not open serial port. Last error: {last_err}")

def post_to_ubidots(payload: dict):
    r = requests.post(UBIDOTS_URL, headers=HEADERS, data=json.dumps(payload), timeout=10)
    r.raise_for_status()
    return r.status_code

def main():
    if not TOKEN or TOKEN.startswith("PUT-"):
        print("Set UBIDOTS_TOKEN first.", file=sys.stderr)
        sys.exit(1)

    print(f"Posting to Ubidots device: {DEVICE_LABEL}")
    try:
        ser = open_serial_with_retry()
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    print(f"✅ Serial connected. Reading JSON lines → {UBIDOTS_URL}")
    try:
        with ser:
            while True:
                line = ser.readline().decode(errors="ignore").strip()
                if not line:
                    continue
                # Expect lines like: {"distance_cm":25}
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    continue

                try:
                    code = post_to_ubidots(payload)
                    print(f"OK {code}: {payload}")
                except Exception as e:
                    print(f"POST failed: {e}", file=sys.stderr)
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nBye!")
        sys.exit(0)

if __name__ == "__main__":
    main()

'''
UBIDOTS_TOKEN and UBIDOTS_DEVICE can be set via environment variables.
Example (macOS/Linux):
  export UBIDOTS_TOKEN="BBUS-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  export UBIDOTS_DEVICE="machine-a"
  export NANO_PORT="/dev/cu.usbmodem113101"  # optional
  python3 ubidots-bridge.py

  If you need to kill anyone using thre serial prot you can do this
  lsof /dev/tty.usbmodem* /dev/cu.usbmodem*    # see who owns it
  kill -9 <PID>

'''
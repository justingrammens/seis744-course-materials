#!/usr/bin/env python3
import os, sys, time, json, glob
import serial
from serial import SerialException
import paho.mqtt.client as mqtt

# ---------- Config (env overrides) ----------
SERIAL_BAUD   = int(os.getenv("NANO_BAUD", "115200"))
PORT_HINT     = os.getenv("NANO_PORT", "")              # e.g., "/dev/cu.usbmodem113101" or "COM5"
MQTT_HOST     = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT     = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC    = os.getenv("MQTT_TOPIC", "PIOT/ConstrainedDevice/SensorMsg")
MQTT_CLIENTID = os.getenv("MQTT_CLIENTID", "nano33ble-data-bridge")
QOS           = int(os.getenv("MQTT_QOS", "0"))         # 0 or 1 is fine here

# Prefer cu.* on macOS; respect explicit hint first
PORT_PATTERNS = [p for p in [PORT_HINT, "/dev/cu.usbmodem*", "/dev/tty.usbmodem*"] if p]

def find_port():
    for pat in PORT_PATTERNS:
        if not pat:
            continue
        if "*" in pat:
            matches = sorted(glob.glob(pat))
            if matches:
                return matches[0]
        else:
            return pat
    return None

def open_serial_with_retry(retries=6, delay=1.2):
    last_err = None
    for _ in range(retries):
        port = find_port()
        if not port:
            last_err = "No serial port found. Set NANO_PORT or plug the board."
            time.sleep(delay)
            continue
        try:
            ser = serial.Serial(port, SERIAL_BAUD, timeout=2)
            time.sleep(0.5)  # let it settle
            return ser
        except SerialException as e:
            msg = str(e)
            last_err = msg
            if "busy" in msg.lower():
                print("\n⚠️  Port busy! Close Arduino Serial Monitor/Plotter and rerun.\n", file=sys.stderr)
                break
            time.sleep(delay)
    raise RuntimeError(f"Could not open serial port. Last error: {last_err}")

def ensure_mqtt():
    client = mqtt.Client(client_id=MQTT_CLIENTID, clean_session=True)
    # Add auth if needed:
    # client.username_pw_set("user", "pass")
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=30)
    client.loop_start()
    return client

def main():
    print(f"MQTT → {MQTT_HOST}:{MQTT_PORT}  topic → {MQTT_TOPIC}")
    try:
        ser = open_serial_with_retry()
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    client = ensure_mqtt()
    print("✅ Serial connected. Streaming JSON lines to MQTT… (Ctrl+C to stop)")

    try:
        with ser:
            while True:
                line = ser.readline().decode(errors="ignore").strip()
                if not line:
                    continue
                try:
                    print(f"← {line}")
                    payload = json.loads(line)   # Expect {"distance_cm": <int>}
                except json.JSONDecodeError:
                    print(f"⚠️  Invalid JSON: {line}", file=sys.stderr)
                    continue

                # Publish the JSON as-is
                info = client.publish(MQTT_TOPIC, json.dumps(payload), qos=QOS, retain=False)
                rc = info.rc
                if rc != mqtt.MQTT_ERR_SUCCESS:
                    print(f"Publish failed rc={rc}", file=sys.stderr)
                else:
                    print(f"→ {MQTT_TOPIC} {payload}")
                time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()
        print("\nBye!")

if __name__ == "__main__":
    main()

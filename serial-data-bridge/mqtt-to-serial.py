#!/usr/bin/env python3
import os, sys, time, json, glob
import serial
from serial import SerialException
import paho.mqtt.client as mqtt

# ---------- Config (env overrides) ----------
SERIAL_BAUD   = int(os.getenv("NANO_BAUD", "115200"))
PORT_HINT     = os.getenv("NANO_PORT", "")              # e.g., "/dev/cu.usbmodem113101" or "COM5"
#MQTT_HOST     = os.getenv("MQTT_HOST", "localhost")
MQTT_HOST     = os.getenv("MQTT_HOST", "mqtt-dashboard.com") 
MQTT_PORT     = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC    = os.getenv("MQTT_TOPIC", "sensors/nano33ble/command")
MQTT_CLIENTID = os.getenv("MQTT_CLIENTID", "nano33ble-command-bridge")
QOS           = int(os.getenv("MQTT_QOS", "0"))         # 0 or 1 is fine here

# Prefer cu.* on macOS; respect explicit hint first
PORT_PATTERNS = [p for p in [PORT_HINT, "/dev/cu.usbmodem*", "/dev/tty.usbmodem*"] if p]

# Global serial connection (accessed in MQTT callback)
ser = None

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
            s = serial.Serial(port, SERIAL_BAUD, timeout=2)
            time.sleep(0.5)  # let it settle
            return s
        except SerialException as e:
            msg = str(e)
            last_err = msg
            if "busy" in msg.lower():
                print("\n⚠️  Port busy! Close Arduino Serial Monitor/Plotter and rerun.\n", file=sys.stderr)
                break
            time.sleep(delay)
    raise RuntimeError(f"Could not open serial port. Last error: {last_err}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Connected to MQTT broker at {MQTT_HOST}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC, qos=QOS)
        print(f"📡 Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"❌ Failed to connect to MQTT broker, return code {rc}", file=sys.stderr)

def on_message(client, userdata, msg):
    """
    Called when a message is received from MQTT.
    Sends the payload to the serial port.
    """
    global ser
    if ser is None or not ser.is_open:
        print("⚠️  Serial port not open, ignoring message", file=sys.stderr)
        return

    try:
        payload = msg.payload.decode('utf-8').strip()
        print(f"← {msg.topic}: {payload}")

        # Send to serial port with newline (Arduino expects line-terminated input)
        ser.write((payload + '\n').encode('utf-8'))
        ser.flush()

    except Exception as e:
        print(f"❌ Error processing message: {e}", file=sys.stderr)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"⚠️  Unexpected disconnection from MQTT broker (rc={rc})", file=sys.stderr)

def main():
    global ser

    print(f"MQTT ← {MQTT_HOST}:{MQTT_PORT}  topic ← {MQTT_TOPIC}")

    # Open serial port
    try:
        ser = open_serial_with_retry()
        print(f"✅ Serial port opened: {ser.port}")
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    # Setup MQTT client with callbacks
    client = mqtt.Client(client_id=MQTT_CLIENTID, clean_session=True)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    # Add auth if needed:
    # client.username_pw_set("user", "pass")

    try:
        client.connect(MQTT_HOST, MQTT_PORT, keepalive=30)
    except Exception as e:
        print(f"❌ Failed to connect to MQTT broker: {e}", file=sys.stderr)
        ser.close()
        sys.exit(1)

    print("✅ Listening for MQTT messages... (Ctrl+C to stop)")

    try:
        # Blocking loop - handles all MQTT network traffic and callbacks
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n⏸  Interrupted by user")
    finally:
        client.disconnect()
        if ser and ser.is_open:
            ser.close()
        print("\nBye!")

if __name__ == "__main__":
    main()

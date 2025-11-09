# Serial Data Bridge - SEIS744 Course Materials

This folder contains Python scripts for bridging serial sensor data to cloud/local platforms. These examples demonstrate two different approaches for publishing IoT sensor data from Arduino-based devices.

## Overview

Both scripts read JSON-formatted sensor data from a serial port (e.g., Arduino Nano 33 BLE) and publish the data to different destinations:

1. **Local MQTT Broker** (`serial-to-mqtt.py`) - Publishes data to a local MQTT server
2. **Ubidots Cloud API** (`ubidots-bridge.py`) - Sends data directly to Ubidots using their REST API

## Prerequisites

- Python 3.x
- Required packages:
  ```bash
  pip install pyserial paho-mqtt requests
  ```
- Arduino or compatible microcontroller sending JSON data via serial
- Expected JSON format: `{"distance_cm": 25}` or similar key-value pairs

## Option 1: MQTT Publishing (serial-to-mqtt.py)

Publishes sensor data to a local or remote MQTT broker.

### Configuration

Set environment variables or use defaults:

```bash
export MQTT_HOST="localhost"          # MQTT broker address
export MQTT_PORT="1883"               # MQTT broker port
export MQTT_TOPIC="sensors/nano33ble/data"
export MQTT_CLIENTID="nano33ble-data-bridge"
export NANO_PORT="/dev/cu.usbmodem113101"  # Optional: specific serial port
export NANO_BAUD="115200"             # Serial baud rate
export MQTT_QOS="0"                   # Quality of Service (0, 1, or 2)
```

### Usage

```bash
python3 serial-to-mqtt.py
```

### Features

- Auto-detects USB serial ports (prefers `/dev/cu.usbmodem*` on macOS)
- Publishes JSON payloads to configurable MQTT topic
- Retry logic for serial port connection
- Detects and warns about busy ports (Serial Monitor/Plotter conflicts)

### Example Output

```
MQTT → localhost:1883  topic → sensors/nano33ble/data
✅ Serial connected. Streaming JSON lines to MQTT… (Ctrl+C to stop)
→ sensors/nano33ble/data {'distance_cm': 25}
→ sensors/nano33ble/data {'distance_cm': 30}
```

## Option 2: Ubidots Direct API (ubidots-bridge.py)

Sends sensor data directly to Ubidots cloud platform using HTTP POST requests.

### Configuration

Set environment variables:

```bash
export UBIDOTS_TOKEN="BBUS-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export UBIDOTS_DEVICE="machine-a"     # Your Ubidots device label
export NANO_PORT="/dev/cu.usbmodem113101"  # Optional
export NANO_BAUD="115200"
```

### Usage

```bash
python3 ubidots-bridge.py
```

### Features

- Posts directly to Ubidots Industrial API (v1.6)
- Automatic device creation in Ubidots
- Token-based authentication
- Error handling for network issues
- Auto-detects serial ports

### Example Output

```
Posting to Ubidots device: machine-a
✅ Serial connected. Reading JSON lines → https://industrial.api.ubidots.com/api/v1.6/devices/machine-a/
OK 200: {'distance_cm': 25}
OK 200: {'distance_cm': 30}
```

## Troubleshooting

### Port Busy Error

If you see "Port busy!" error, close Arduino IDE's Serial Monitor or Serial Plotter:

```bash
# Check what's using the port (macOS/Linux)
lsof /dev/tty.usbmodem* /dev/cu.usbmodem*

# Kill the process if needed
kill -9 <PID>
```

### Port Not Found

- Set `NANO_PORT` environment variable to your specific port
- On Windows: `COM3`, `COM5`, etc.
- On macOS: `/dev/cu.usbmodem*` or `/dev/tty.usbmodem*`
- On Linux: `/dev/ttyUSB0`, `/dev/ttyACM0`, etc.

### Serial Data Format

Ensure your Arduino sketch outputs valid JSON lines:

```cpp
// Example Arduino code
void loop() {
  int distance = readSensor();
  Serial.print("{\"distance_cm\":");
  Serial.print(distance);
  Serial.println("}");
  delay(100);
}
```

## Architecture Comparison

### MQTT Approach (serial-to-mqtt.py)

**Pros:**
- Lightweight publish/subscribe protocol
- Local processing possible
- Multiple subscribers can consume same data
- Works offline with local broker
- Lower latency

**Cons:**
- Requires MQTT broker setup
- Additional infrastructure to manage

### Direct API Approach (ubidots-bridge.py)

**Pros:**
- No local infrastructure needed
- Direct cloud integration
- Built-in data visualization in Ubidots
- Managed service (no server maintenance)

**Cons:**
- Requires internet connection
- API rate limits may apply
- Higher latency than local MQTT

## Course Context

These examples demonstrate key IoT integration patterns:
- Serial communication protocols
- Data serialization (JSON)
- MQTT messaging for IoT
- RESTful API integration
- Environment-based configuration
- Error handling and retries
- Cloud vs. local data processing

## License

Educational materials for SEIS744 course.

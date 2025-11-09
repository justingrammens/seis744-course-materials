# Arduino Examples for SEIS 744

This repository contains a collection of Arduino sketches demonstrating various sensors on the Arduino Nano 33 BLE Sense (Rev1) and external Grove sensors.

## Overview of Examples

### 1. `ble-sense-proximity` - Optical Proximity Sensing
**Hardware:** Built-in APDS9960 sensor on Arduino Nano 33 BLE Sense

**Description:** Measures proximity using infrared light reflection from the onboard APDS9960 sensor.

**Key Features:**
- Uses optical sensing (infrared LED + photodetector)
- Range: 0-255 (0 = far, 255 = very close/saturated)
- Best for detecting objects within ~20cm
- Outputs JSON: `{"proximity": <value>}`
- Update rate: 500ms

**Physical Principle:** The APDS9960 emits infrared light and measures how much light reflects back. More reflection indicates a closer object. Works best with reflective surfaces and is affected by ambient light conditions.

---

### 2. `grove-ultrasonic` - Acoustic Distance Measurement
**Hardware:** External Grove Ultrasonic Ranger (connected to D11 Grove port)

**Description:** Measures distance using ultrasonic sound waves (time-of-flight measurement).

**Key Features:**
- Uses acoustic sensing (ultrasonic transducer)
- Range: 0-400 cm with centimeter precision
- Best for detecting objects from 2cm to 4 meters
- Outputs JSON: `{"distance_cm": <value>}` or `{"error": "out_of_range"}`
- Update rate: 5 seconds (1 Hz)

**Physical Principle:** The sensor emits a 40kHz ultrasonic pulse and measures the time it takes for the echo to return. Distance is calculated using the speed of sound (~343 m/s at room temperature). Works by acoustic reflection and is affected by temperature, humidity, and surface texture.

---

## Key Differences: Optical vs. Acoustic Sensing

Although both the APDS9960 (optical proximity) and Grove Ultrasonic Ranger (acoustic distance) measure "closeness," they rely on very different physical principles and are suited to different applications:

| Aspect | APDS9960 (Optical) | Grove Ultrasonic (Acoustic) |
|--------|-------------------|----------------------------|
| **Sensing Method** | Infrared light reflection | Ultrasonic sound time-of-flight |
| **Range** | Very short (~0-20cm) | Long (2-400cm) |
| **Output** | Relative proximity (0-255) | Absolute distance (cm) |
| **Accuracy** | Relative/qualitative | Quantitative (cm precision) |
| **Best For** | Gesture detection, close proximity | Distance measurement, obstacle detection |
| **Affected By** | Ambient light, surface reflectivity | Temperature, humidity, soft surfaces |
| **Speed** | Very fast (<1ms) | Moderate (~30ms per reading) |
| **Directionality** | Narrow beam | Wide cone (~15° beam) |

**When to Use Optical (APDS9960):**
- Gesture recognition or swipe detection
- Quick proximity triggers (hand wave detection)
- Indoor applications with controlled lighting
- When you need very fast response

**When to Use Acoustic (Ultrasonic):**
- Precise distance measurements
- Long-range obstacle detection (robotics, parking sensors)
- Outdoor applications
- When measuring to soft or absorptive surfaces

---

### 3. `nano-accel` - Accelerometer Data
**Hardware:** Built-in LSM9DS1 IMU on Arduino Nano 33 BLE Sense (Rev1)

**Description:** Reads 3-axis acceleration data from the onboard IMU.

**Key Features:**
- Measures acceleration in X, Y, Z axes (in g-forces)
- Useful for motion detection, orientation, tilt sensing, vibration
- Outputs JSON: `{"accel_x": <x>, "accel_y": <y>, "accel_z": <z>}`
- Update rate: 200ms

**Applications:** Tap detection, orientation sensing, fall detection, activity recognition

---

### 4. `nano-noise1` - Continuous Sound Level Monitoring
**Hardware:** Built-in MP34DT05 PDM microphone on Arduino Nano 33 BLE Sense

**Description:** Continuously streams sound level measurements as mean absolute amplitude.

**Key Features:**
- 16 kHz sampling rate, mono channel
- Computes mean absolute amplitude as a loudness proxy
- Continuous output stream
- Outputs JSON: `{"sound_level": <value>}`
- Update rate: 50ms (~20 fps)

**Applications:** Sound level meters, noise monitoring, audio visualization

---

### 5. `nano-noise2` - Event-Driven Sound Trigger
**Hardware:** Built-in MP34DT05 PDM microphone on Arduino Nano 33 BLE Sense

**Description:** Smart sound trigger that only publishes when loud sounds exceed the adaptive noise floor.

**Key Features:**
- Adaptive noise floor using exponential moving average (EMA)
- Event-driven: only outputs when loud sounds detected
- Configurable trigger threshold and hysteresis
- 800ms cooldown between events to prevent spam
- Outputs JSON only on events: `{"event":"loud", "sound_level":<val>, "floor":<val>, "delta":<val>}`

**Applications:** Clap detection, knock detection, security alerts, smart home triggers

**Tunable Parameters:**
- `EMA_ALPHA`: How quickly the noise floor adapts (0.02 = slow)
- `TRIGGER_DELTA`: How much louder than floor triggers event (250)
- `HYSTERESIS`: Reset threshold to prevent bouncing (100)
- `COOLDOWN_MS`: Minimum time between events (800ms)

---

## Common Features

All examples output data in JSON format for easy integration with serial-to-MQTT bridges or other data pipelines.

**Serial Configuration:**
- Baud rate: 115200
- Format: One JSON object per line
- Compatible with Node.js serial bridges and Python parsers

## Hardware Requirements

- **Arduino Nano 33 BLE Sense (Rev1)** - All examples except `grove-ultrasonic`
- **Grove Ultrasonic Ranger** - Required for `grove-ultrasonic` example
- **Grove Shield or jumper wires** - To connect Grove sensor to D11 (or D12)

## Library Dependencies

- `Arduino_APDS9960` - Proximity example
- `Arduino_LSM9DS1` - Accelerometer example (Rev1 boards)
- `PDM` - Microphone examples
- `Ultrasonic` - Grove Ultrasonic library (install from Seeed Studio)

## Getting Started

1. Install the Arduino IDE
2. Add the required libraries via Library Manager
3. Select board: **Arduino Nano 33 BLE**
4. Upload the desired sketch
5. Open Serial Monitor at 115200 baud to see JSON output

## Notes

- The microphone examples use PDM (Pulse Density Modulation) with interrupt-driven callbacks
- All sensors output JSON for easy parsing and integration
- Adjust delays and parameters based on your application needs
- For `grove-ultrasonic`, change `SIG_PIN` to 12 if using the D12 Grove port
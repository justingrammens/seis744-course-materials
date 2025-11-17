#include <PDM.h>

// ====== Tunables ======
#define SAMPLE_RATE     16000     // 16 kHz mic
#define CHANNELS        1
#define FRAME_SAMPLES   256       // ~16ms at 16kHz
#define MIC_GAIN_DB     20        // adjust 0..50-ish

// Trigger logic
#define EMA_ALPHA       0.02f     // 0..1, lower = slower floor
#define TRIGGER_DELTA   250.0f    // how much above floor counts as “loud”
#define HYSTERESIS      100.0f    // drop below (delta - HYSTERESIS) to reset
#define COOLDOWN_MS     800       // min time between published events

// Debug prints (uncomment to watch levels continuously)
// #define DEBUG_STREAM

// ====== Buffers / State ======
int16_t sampleBuffer[FRAME_SAMPLES];
volatile size_t samplesReady = 0;

float noiseFloor = 200.0f;        // initial guess; will adapt
bool  triggered = false;
unsigned long lastPublishMs = 0;

void onPDMdata() {
  int bytesAvailable = PDM.available();
  if (bytesAvailable > (int)sizeof(sampleBuffer)) bytesAvailable = sizeof(sampleBuffer);
  PDM.read(sampleBuffer, bytesAvailable);
  samplesReady = bytesAvailable / sizeof(int16_t);
}

void setup() {
  Serial.begin(115200);
  delay(400);

  PDM.onReceive(onPDMdata);
  if (!PDM.begin(CHANNELS, SAMPLE_RATE)) {
    Serial.println("{\"error\":\"PDM begin failed\"}");
    while (1) { delay(1000); }
  }
  // Optional; remove if your core doesn’t expose it
  PDM.setGain(MIC_GAIN_DB);

  Serial.println("Mic loud-sound trigger → JSON (only on events)");
}

void loop() {
  size_t n = samplesReady;
  if (n == 0) { delay(1); return; }

  // Take local copy & clear flag quickly
  noInterrupts();
  size_t num = samplesReady;
  samplesReady = 0;
  interrupts();

  // Mean Absolute Amplitude (cheap loudness proxy)
  long sumAbs = 0;
  for (size_t i = 0; i < num; i++) sumAbs += abs(sampleBuffer[i]);
  float level = (num > 0) ? (float)sumAbs / (float)num : 0.0f;

  // Update rolling noise floor (only when not strongly triggered)
  if (!triggered) {
    noiseFloor = (1.0f - EMA_ALPHA) * noiseFloor + EMA_ALPHA * level;
  }

  float delta = level - noiseFloor;
#ifdef DEBUG_STREAM
  Serial.print("{\"level\":"); Serial.print(level,1);
  Serial.print(",\"floor\":");  Serial.print(noiseFloor,1);
  Serial.print(",\"delta\":");  Serial.print(delta,1);
  Serial.println("}");
#endif

  unsigned long now = millis();

  // Rising-edge trigger
  if (!triggered && delta > TRIGGER_DELTA && (now - lastPublishMs) > COOLDOWN_MS) {
    triggered = true;
    lastPublishMs = now;

    // Publish one compact JSON line (bridge will send to MQTT)
    Serial.print("{\"name\":\"sound_level\",\"value\":");
    Serial.print(level, 1);
    Serial.println("}");

  }

  // Reset trigger after we fall below hysteresis
  if (triggered && delta < (TRIGGER_DELTA - HYSTERESIS)) {
    triggered = false;
  }

  // Small pacing delay keeps ISR responsive yet smooths CPU use
  delay(10);
}

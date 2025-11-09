#include <PDM.h>

// ---- Config ----
#define SAMPLE_RATE   16000        // 16 kHz
#define CHANNELS      1            // mono
#define FRAME_SAMPLES 256          // samples per frame (int16_t)
#define MIC_GAIN_DB   20           // adjust 0..50-ish

// Audio buffer must be NON-volatile for PDM.read()
int16_t sampleBuffer[FRAME_SAMPLES];
volatile size_t samplesReady = 0;   // just a flag/counter

void onPDMdata() {
  // Read as many bytes as are available, but cap to our buffer size
  int bytesAvailable = PDM.available();
  if (bytesAvailable > (int)sizeof(sampleBuffer)) {
    bytesAvailable = sizeof(sampleBuffer);
  }
  // OK: sampleBuffer is non-volatile, so this matches void* signature
  PDM.read(sampleBuffer, bytesAvailable);

  // Convert bytes → samples
  samplesReady = bytesAvailable / sizeof(int16_t);
}

void setup() {
  Serial.begin(115200);
  delay(500);

  // Configure PDM
  PDM.onReceive(onPDMdata);
  if (!PDM.begin(CHANNELS, SAMPLE_RATE)) {
    Serial.println("{\"error\":\"PDM begin failed\"}");
    while (1) { delay(1000); }
  }
  // Optional: mic gain (some cores expose this; if not present, remove)
  PDM.setGain(MIC_GAIN_DB);

  Serial.println("Mic sound level → JSON");
}

void loop() {
  size_t n = samplesReady;
  if (n > 0) {
    // Take a local copy count, then clear the flag quickly
    noInterrupts();
    size_t num = samplesReady;
    samplesReady = 0;
    interrupts();

    // Compute simple mean absolute amplitude (cheap “loudness” proxy)
    long sumAbs = 0;
    for (size_t i = 0; i < num; i++) {
      sumAbs += abs(sampleBuffer[i]);
    }
    float meanAbs = (num > 0) ? (float)sumAbs / (float)num : 0.0f;

    // Optionally convert to “RMS”:
    // double sumSq = 0; for (size_t i=0;i<num;i++) { double s=sampleBuffer[i]; sumSq += s*s; }
    // float rms = (num>0) ? sqrt(sumSq/num) : 0.0f;

    // Print one compact JSON line (works with your Serial→MQTT bridge)
    Serial.print("{\"sound_level\":");
    Serial.print(meanAbs, 1);    // or print rms
    Serial.println("}");
  }

  // ~10–20 fps is plenty for “meter” demos
  delay(50);
}

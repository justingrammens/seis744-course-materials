#include "Ultrasonic.h"

#define SIG_PIN 4

Ultrasonic ultrasonic(SIG_PIN);

void setup() {
  Serial.begin(115200);
  delay(1000); // small warm-up; do NOT use while(!Serial)
  Serial.println(F("Ultrasonic → JSON output"));
}

void loop() {
  long cm = ultrasonic.MeasureInCentimeters();

  if (cm > 0 && cm < 400) {
    // One compact JSON line per reading:
    Serial.print(F("{\"distance_cm\":"));
    Serial.print(cm);
    Serial.println(F("}"));
  } else {
    Serial.println(F("{\"error\":\"out_of_range\"}"));
  }

  delay(5000); // 1 Hz
}

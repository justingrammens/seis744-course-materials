#include <Arduino_LSM9DS1.h>  // Rev1 IMU

void setup() {
  Serial.begin(115200);
  delay(500);
  if (!IMU.begin()) {
    Serial.println("{\"error\":\"IMU begin failed (Rev1)\"}");
    while (1) { delay(1000); }
  }
  Serial.println("IMU accel → JSON (Rev1)");
}

void loop() {
  float ax, ay, az;
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(ax, ay, az); // in g
    Serial.print("{\"accel_x\":"); Serial.print(ax, 3);
    Serial.print(",\"accel_y\":");  Serial.print(ay, 3);
    Serial.print(",\"accel_z\":");  Serial.print(az, 3);
    Serial.println("}");
  }
  delay(200);
}

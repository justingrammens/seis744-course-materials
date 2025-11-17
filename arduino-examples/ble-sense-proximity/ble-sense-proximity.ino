#include <Arduino_APDS9960.h>
void setup(){
  Serial.begin(115200); 
  delay(1000);
  if (!APDS.begin()) { Serial.println("{\"error\":\"APDS init failed\"}"); 
  while(1){} }
  Serial.println("APDS proximity demo");
}
void loop(){
  if (APDS.proximityAvailable()) {
    int p = APDS.readProximity();     // 0(far) .. 255(very close/saturated)
    Serial.print("{\"proximity\":"); Serial.print(p); Serial.println("}");
  }
  delay(500); // don't hammer it
}

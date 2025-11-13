void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
if (Serial.available()) {
    String line = Serial.readStringUntil('\n'); // matches the "\n" we send from Python
    Serial.print(line);
    if (line.equals("on")) {
      digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
    } else {
      digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW

    }
}

}

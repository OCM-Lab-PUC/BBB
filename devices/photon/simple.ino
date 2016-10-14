SYSTEM_MODE(AUTOMATIC);

void setup() {
  pinMode(D7, OUTPUT);
  WiFi.off();
}

void loop() {
  digitalWrite(D7, HIGH);
  delay(500);
  digitalWrite(D7, LOW);
  delay(500);
}																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																										
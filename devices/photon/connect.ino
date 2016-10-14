SYSTEM_MODE(SEMI_AUTOMATIC);
void setup() {
	Serial.begin(9600);
    //WiFi.off();
    //WiFi.useDynamicIP();  //persistente muy importante, si se pone dinámica la va a recordar para siempre y ocurren problemas de conexión
    //WiFi.on();
    WiFi.connect();
    //Particle.connect();
    waitUntil(WiFi.ready);
}





void loop(){
	delay(1000);
}

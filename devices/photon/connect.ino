void setup() {
    //WiFi.off();
    //WiFi.useDynamicIP();  //persistente muy importante, si se pone dinámica la va a recordar para siempre y ocurren problemas de conexión
    //WiFi.on();
    WiFi.connect();
    //Particle.connect();
    waitUntil(WiFi.ready);
}





void loop(){

}

#include <sstream>
#include <string>
//#include <iostream>
//using namespace std;

SYSTEM_MODE(SEMI_AUTOMATIC)
TCPClient client;
byte dome_IP[4] = {192,168,0,12};
int dome_Port = 8001;
int led = D7;
// ifconi

void setup() {

    Serial.begin(9600); //velocidad de lectura puerto
    pinMode(led,OUTPUT);    //habilitamos pines D7 para mostrar heartbeat
    digitalWrite(led,LOW);
    //WiFi.off();
    //WiFi.useDynamicIP();  //persistente muy importante, si se pone dinámica la va a recordar para siempre y ocurren problemas de conexión
    //WiFi.on();
    WiFi.connect();
    //Particle.connect();   // bloqueante. Conneción a la nube
    //waitUntil(WiFi.ready);
    //delay(5000);
}

void heartbeat(){

    digitalWrite(led,HIGH);
    delay(100);
    digitalWrite(led,LOW);
    delay(100);
    digitalWrite(led,HIGH);
    delay(100);
    digitalWrite(led,LOW);
    delay(600);

}

void send(){
    std::string data="{'msgId':1,'sourceId':4,'content':{'power':100,'state':0}}";
    std::stringstream aux;
    aux << data.size();                                                         
    std::string lenght = aux.str();          // important lengt must be 9<lenght<100
    //Serial.println((lenght+data).c_str());
    client.write((lenght+data).c_str());
    //char *intStr = itoa(lenght);
    //Serial.println(str)
    //string prueba=to_string(lenght)
    //std::string prueba=std::to_string(lenght);
    //Serial.println((prueba+data).c_str());
}

void loop(){
    if(!client.connected()){
        Serial.println("State: Not connected");
        Serial.println("Connecting...");
        client.connect(dome_IP,dome_Port);
    }
    else {
        heartbeat();
        Serial.println("State: Connected");
        send();
        //client.stop();
        delay(1000);                                        //wait for response
        std::string data="";
        while(client.available()){
            //Serial.println("Receiving state...");
            char c=client.read();

            data=data+c;
            //data = data+aux;
        }
        Serial.println(data.c_str());
        //client.stop();

    }
}

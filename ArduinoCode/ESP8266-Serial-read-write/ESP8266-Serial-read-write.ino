#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>

SoftwareSerial pi(13, 15); // RX, TX

char data; //Initialized variable to store recieved data
String line;

void setup() {
  Serial.begin(115200);
  pi.begin(115200);

  while (!Serial) {
    Serial.print('.');
    delay(500); 
  }
}


void loop() {
//    if(pi.readBytesUntil('\n',data ,2)>0)
//      Serial.println(data);
//    delay(1000);
    if( pi.available() >= 2) {
        for (int i = 0; i< 2; i++ ) {
            data = pi.read();
            line += data;
        }
        delay(1000);
    }


    Serial.print(line);

}

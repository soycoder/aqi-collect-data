#include <ESP8266WiFi.h>

#include <FirebaseESP8266.h>

extern "C"
{
#include "user_interface.h"
#include "wpa2_enterprise.h"
#include "c_types.h"
}

// SSID to connect to
char ssid[] = "..@TUwifi";
char username[] = "6109700077";
char identity[] = "6109700077";
char password[] = "*apisith0707";

// ESP_9FEA5F - 84:f3:eb:9f:ea:5f
uint8_t target_esp_mac[6] = {0x84, 0xf3, 0xeb, 0x9f, 0xea, 0x5f};

#define FIREBASE_HOST "tu-airq-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "Ajm0irlBklW4aQXn0hJMMNLH0YJEQwsXRBsZh1Sn"

//Define Firebase Data object
FirebaseData fbdo;
String path = "/pollution";
String jsonStr = "";

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = { 0, -1 };
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }
  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void setup()
{

  WiFi.mode(WIFI_STA);
  Serial.begin(115200);
  delay(1000);
  Serial.setDebugOutput(true);

  // Setting ESP into STATION mode only (no AP mode or dual mode)
  wifi_set_opmode(STATION_MODE);

  struct station_config wifi_config;

  memset(&wifi_config, 0, sizeof(wifi_config));
  strcpy((char *)wifi_config.ssid, ssid);
  strcpy((char *)wifi_config.password, password);

  wifi_station_set_config(&wifi_config);
  wifi_set_macaddr(STATION_IF, target_esp_mac);

  wifi_station_set_wpa2_enterprise_auth(1);

  // Clean up to be sure no old data is still inside
  wifi_station_clear_cert_key();
  wifi_station_clear_enterprise_ca_cert();
  wifi_station_clear_enterprise_identity();
  wifi_station_clear_enterprise_username();
  wifi_station_clear_enterprise_password();
  wifi_station_clear_enterprise_new_password();

  wifi_station_set_enterprise_identity((uint8 *)identity, strlen(identity));
  wifi_station_set_enterprise_username((uint8 *)username, strlen(username));
  wifi_station_set_enterprise_password((uint8 *)password, strlen((char *)password));

  wifi_station_connect();

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(300);
    Serial.print(".");
  }

  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Begin Real-time Firebase
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);

  //Set the size of WiFi rx/tx buffers in the case where we want to work with large data.
  fbdo.setBSSLBufferSize(1024, 1024);

  //Set the size of HTTP response buffers in the case where we want to work with large data.
  fbdo.setResponseSize(1024);
}

String line = "";
void loop()
{
  while (Serial.available() > 0)
  {
    line = Serial.readString();

    String datetime = getValue(line, ':', 0);
    String pm1 = getValue(line, ':', 1);
    String pm25 = getValue(line, ':', 2);
    String pm10 = getValue(line, ':', 3);
    Serial.println(line);
////    Serial.println(datetime + " " + pm1+ " " + pm25+ " " + pm10);
    int n_datetime = datetime.toInt();
    int n_pm1 = pm1.toInt();
    int n_pm25 = pm25.toInt();
    int n_pm10 = pm10.toInt();
    
    if (line)
    {

      FirebaseJson data;
      data.set("/time", n_datetime);
      data.set("/pm1", n_pm1);
      data.set("/pm25", n_pm25);
      data.set("/pm10", n_pm10);

      if (Firebase.push(fbdo, path, data))
      {
        Serial.println("PASSED");
        Serial.println("PATH: " + fbdo.dataPath());
        Serial.println("TYPE: " + fbdo.dataType());
        Serial.print("VALUE: ");
        Serial.println(line);
        Serial.println("------------------------------------");
        Serial.println();
      }
      else
      {
        Serial.println("FAILED");
        Serial.println("REASON: " + fbdo.errorReason());
        Serial.println("------------------------------------");
        Serial.println();
      }
    }
  }
}
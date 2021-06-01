#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

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

String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = {0, -1};
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++)
    {
        if (data.charAt(i) == separator || i == maxIndex)
        {
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
    //  Serial.printf("SDK version: %s\n", system_get_sdk_version());
    //  Serial.printf("Free Heap: %4d\n",ESP.getFreeHeap());

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
        delay(1000);
        Serial.print(".");
    }

    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}
String line = "";

void loop()
{
    if (WiFi.status() == WL_CONNECTED)
    {
        // wait for WiFi connection
        while (Serial.available() > 0)
        {
            line = Serial.readString();
            String type = getValue(line, ':', 0);

            WiFiClient client;
            HTTPClient http;

            // get PM
            String pm25 = getValue(line, ':', 2);
            String pm10 = getValue(line, ':', 3);
            // get Meteo
            String light = getValue(line, ':', 4);
            String temp = getValue(line, ':', 5);
            String humi = getValue(line, ':', 6);
            String pressure = getValue(line, ':', 7);
            String rain = getValue(line, ':', 8);
            String O3 = getValue(line, ':', 9);
            String NO2 = getValue(line, ':', 10);
            String CO = getValue(line, ':', 11);
            String SO2 = getValue(line, ':', 12);
            String WS = getValue(line, ':', 13);
            String WDI = getValue(line, ':', 14);

            if (type != "hourly")
            {
                Serial.print("[HTTP] POST...\n");
                // configure traged server and url
                http.begin(client, "http://express-nodejs-firebase.herokuapp.com/api/createRecord"); //HTTP
                http.addHeader("Content-Type", "application/json");

                // start connection and send HTTP header and body
                int httpCode = http.POST("{\"pm25\": " + pm25 + ",\"pm10\": " + pm10 + ",\"light\": " + light + ",\"temp\": " + temp + ",\"humi\":" + humi + ",\"pressure\":" + pressure + ",\"rain\":" + rain + ",\"O3\":" + O3 + ",\"NO2\":" + NO2 + ",\"CO\":" + CO + ",\"SO2\":" + SO2 + ",\"WS\":" + WS + ",\"WDI\":" + WDI + "}");

                // httpCode will be negative on error
                if (httpCode > 0)
                {
                    // HTTP header has been send and Server response header has been handled
                    Serial.printf("[HTTP] POST... code: %d\n", httpCode);

                    // file found at server
                    if (httpCode == HTTP_CODE_OK)
                    {
                        const String &payload = http.getString();
                        Serial.println("received payload:\n<<");
                        Serial.println(payload);
                        Serial.println(">>");
                    }
                }
                else
                {
                    Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
                }
                http.end();
            }
            else
            {
                // Hourly

                Serial.print("[HTTP] POST...\n");
                // configure traged server and url
                http.begin(client, "http://express-nodejs-firebase.herokuapp.com/api/hourly/createRecord"); //HTTP
                http.addHeader("Content-Type", "application/json");

                // start connection and send HTTP header and body
                int httpCode = http.POST("{\"pm25\": " + pm25 + ",\"pm10\": " + pm10 + ",\"light\": " + light + ",\"temp\": " + temp + ",\"humi\":" + humi + ",\"pressure\":" + pressure + ",\"rain\":" + rain + ",\"O3\":" + O3 + ",\"NO2\":" + NO2 + ",\"CO\":" + CO + ",\"SO2\":" + SO2 + ",\"WS\":" + WS + ",\"WDI\":" + WDI + "}");

                // httpCode will be negative on error
                if (httpCode > 0)
                {
                    // HTTP header has been send and Server response header has been handled
                    Serial.printf("[HTTP] POST... code: %d\n", httpCode);

                    // file found at server
                    if (httpCode == HTTP_CODE_OK)
                    {
                        const String &payload = http.getString();
                        Serial.println("received payload:\n<<");
                        Serial.println(payload);
                        Serial.println(">>");
                    }
                }
                else
                {
                    Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
                }
                http.end();
            }
        }
    }else{
        wifi_station_connect();
        while (WiFi.status() != WL_CONNECTED)
        {
            delay(1000);
            Serial.print(".");
        }
    }
}

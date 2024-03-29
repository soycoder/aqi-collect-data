
/**
 * Created by K. Suwatchai (Mobizt)
 * 
 * Email: k_suwatchai@hotmail.com
 * 
 * Github: https://github.com/mobizt
 * 
 * Copyright (c) 2020 mobizt
 *
*/

//This example shows how to set complex json data through FirebaseJson object then read the data back and parse them.

#include <ESP8266WiFi.h>
#include <FirebaseESP8266.h>

#define WIFI_SSID "Apis"
#define WIFI_PASSWORD "12345678"

#define FIREBASE_HOST "tu-airq-default-rtdb.firebaseio.com/"

/** The database secret is obsoleted, please use other authentication methods, 
 * see examples in the Authentications folder. 
*/
#define FIREBASE_AUTH "Ajm0irlBklW4aQXn0hJMMNLH0YJEQwsXRBsZh1Sn"

//Define Firebase Data object
FirebaseData fbdo;
 String path = "/Test/Json";

 String jsonStr = "";

 FirebaseJson json1;

 FirebaseJsonData jsonObj;
 
void setDataFirebase (int num);
void getData(FirebaseData &fbdo1);
void printResult(FirebaseData &data);

void setup()
{

    Serial.begin(115200);
    Serial.println();
    Serial.println();

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connecting to Wi-Fi");
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(300);
    }
    Serial.println();
    Serial.print("Connected with IP: ");
    Serial.println(WiFi.localIP());
    Serial.println();

    Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
    Firebase.reconnectWiFi(true);

    //Set the size of WiFi rx/tx buffers in the case where we want to work with large data.
    fbdo.setBSSLBufferSize(1024, 1024);

    //Set the size of HTTP response buffers in the case where we want to work with large data.
    fbdo.setResponseSize(1024);

}

void setDataFirebase (int num){
    json1.set("Hi/myInt", num);
    json1.set("Hi/myDouble", 0.0023);
    json1.set("Who/are/[0]", "you");
    json1.set("Who/are/[1]", "they");
    json1.set("Who/is/[0]", "she");
    json1.set("Who/is/[1]", "he");
    json1.set("This/is/[0]", false);
    json1.set("This/is/[1]", true);
    json1.set("This/is/[2]", "my house");
    json1.set("This/is/[3]/my", "world");

    Serial.println("------------------------------------");
    Serial.println("JSON Data");
    json1.toString(jsonStr, true);
    Serial.println(jsonStr);
    Serial.println("------------------------------------");

    Serial.println("------------------------------------");
    Serial.println("Set JSON test...");

    if (Firebase.pushJSON(fbdo, path, json1))
    {
        Serial.println("PASSED");
        Serial.println("PATH: " + fbdo.dataPath());
        Serial.println("TYPE: " + fbdo.dataType());
        Serial.print("VALUE: ");
        printResult(fbdo);
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

void getData(FirebaseData &fbdo1){
  Serial.println("------------------------------------");
    Serial.println("Get JSON test...");

    if (Firebase.get(fbdo1, path))
    {
        Serial.println("PASSED");
        Serial.println("PATH: " + fbdo1.dataPath());
        Serial.println("TYPE: " + fbdo1.dataType());
        Serial.print("VALUE: ");
        if (fbdo1.dataType() == "json")
        {
            printResult(fbdo1);
        }

        Serial.println("------------------------------------");
        Serial.println();
    }
    else
    {
        Serial.println("FAILED");
        Serial.println("REASON: " + fbdo1.errorReason());
        Serial.println("------------------------------------");
        Serial.println();
    }

    Serial.println("------------------------------------");
    Serial.println("Try to parse return data and get value..");

    json1 = fbdo1.jsonObject();

    json1.get(jsonObj, "This/is/[3]/my");

    Serial.println("This/is/[3]/my: " + jsonObj.stringValue);

    json1.get(jsonObj, "Hi/myDouble");
    Serial.print("Hi/myDouble: ");
    Serial.println(jsonObj.doubleValue, 4);

    Serial.println("------------------------------------");
    Serial.println();
}

void printResult(FirebaseData &data)
{

    if (data.dataType() == "int")
        Serial.println(data.intData());
    else if (data.dataType() == "float")
        Serial.println(data.floatData(), 5);
    else if (data.dataType() == "double")
        printf("%.9lf\n", data.doubleData());
    else if (data.dataType() == "boolean")
        Serial.println(data.boolData() == 1 ? "true" : "false");
    else if (data.dataType() == "string")
        Serial.println(data.stringData());
    else if (data.dataType() == "json")
    {
        Serial.println();
        FirebaseJson &json = data.jsonObject();
        //Print all object data
        Serial.println("Pretty printed JSON data:");
        String jsonStr;
        json.toString(jsonStr, true);
        Serial.println(jsonStr);
        Serial.println();
        Serial.println("Iterate JSON data:");
        Serial.println();
        size_t len = json.iteratorBegin();
        String key, value = "";
        int type = 0;
        for (size_t i = 0; i < len; i++)
        {
            json.iteratorGet(i, type, key, value);
            Serial.print(i);
            Serial.print(", ");
            Serial.print("Type: ");
            Serial.print(type == FirebaseJson::JSON_OBJECT ? "object" : "array");
            if (type == FirebaseJson::JSON_OBJECT)
            {
                Serial.print(", Key: ");
                Serial.print(key);
            }
            Serial.print(", Value: ");
            Serial.println(value);
        }
        json.iteratorEnd();
    }
    else if (data.dataType() == "array")
    {
        Serial.println();
        //get array data from FirebaseData using FirebaseJsonArray object
        FirebaseJsonArray &arr = data.jsonArray();
        //Print all array values
        Serial.println("Pretty printed Array:");
        String arrStr;
        arr.toString(arrStr, true);
        Serial.println(arrStr);
        Serial.println();
        Serial.println("Iterate array values:");
        Serial.println();
        for (size_t i = 0; i < arr.size(); i++)
        {
            Serial.print(i);
            Serial.print(", Value: ");

            FirebaseJsonData &jsonData = data.jsonData();
            //Get the result data from FirebaseJsonArray object
            arr.get(jsonData, i);
            if (jsonData.typeNum == FirebaseJson::JSON_BOOL)
                Serial.println(jsonData.boolValue ? "true" : "false");
            else if (jsonData.typeNum == FirebaseJson::JSON_INT)
                Serial.println(jsonData.intValue);
            else if (jsonData.typeNum == FirebaseJson::JSON_FLOAT)
                Serial.println(jsonData.floatValue);
            else if (jsonData.typeNum == FirebaseJson::JSON_DOUBLE)
                printf("%.9lf\n", jsonData.doubleValue);
            else if (jsonData.typeNum == FirebaseJson::JSON_STRING ||
                     jsonData.typeNum == FirebaseJson::JSON_NULL ||
                     jsonData.typeNum == FirebaseJson::JSON_OBJECT ||
                     jsonData.typeNum == FirebaseJson::JSON_ARRAY)
                Serial.println(jsonData.stringValue);
        }
    }
    else if (data.dataType() == "blob")
    {

        Serial.println();

        for (int i = 0; i < data.blobData().size(); i++)
        {
            if (i > 0 && i % 16 == 0)
                Serial.println();

            if (i < 16)
                Serial.print("0");

            Serial.print(data.blobData()[i], HEX);
            Serial.print(" ");
        }
        Serial.println();
    }
    else if (data.dataType() == "file")
    {

        Serial.println();

        File file = data.fileStream();
        int i = 0;

        while (file.available())
        {
            if (i > 0 && i % 16 == 0)
                Serial.println();

            int v = file.read();

            if (v < 16)
                Serial.print("0");

            Serial.print(v, HEX);
            Serial.print(" ");
            i++;
        }
        Serial.println();
        file.close();
    }
    else
    {
        Serial.println(data.payload());
    }
}

int n =0;
void loop()
{
  Serial.println("Round #"+n);
  setDataFirebase(n);
  n+=1;
  delay(2000);
//  getData(fbdo);
  
}

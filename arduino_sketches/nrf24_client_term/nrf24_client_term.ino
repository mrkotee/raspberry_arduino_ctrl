
#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"
#include "DHT.h"
//

#define PIN_TERM_IN A1
#define PIN_TERM_OUT A2
#define DHTPIN 2
#define DHTTYPE DHT11

RF24 radio(9,10); // "создать" модуль на пинах 9 и 10 Для Уно
//RF24 radio(9,53); // для Меги

byte address[][6] = {"1Node","2Node","3Node","4Node","5Node","6Node"};  //возможные номера труб


long timer_now;
long timer_prev = millis();
long timer_relay_ping = millis();

float temp_in;
float humid;
float temp_dht;

String incoming = "";
char character;

DHT dht(DHTPIN, DHTTYPE);

void setup(){
  delay(5000);
  
  pinMode(PIN_TERM_OUT, OUTPUT);
  dht.begin();
  
  radio.begin(); //активировать модуль
  radio.setAutoAck(1);         //режим подтверждения приёма, 1 вкл 0 выкл
  radio.setRetries(1,15);     //(время между попыткой достучаться, число попыток)
  radio.enableAckPayload();    //разрешить отсылку данных в ответ на входящий сигнал
  radio.setPayloadSize(64);     //размер пакета, в байтах

  radio.openReadingPipe(1,address[0]);      //хотим слушать трубу 0
  radio.openWritingPipe(address[1]);      
  // radio.setChannel(0x70);  //выбираем канал (в котором нет шумов!)
  radio.setChannel(3);

  radio.setPALevel (RF24_PA_HIGH); //уровень мощности передатчика. На выбор RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX
  radio.setDataRate (RF24_250KBPS); //скорость обмена. На выбор RF24_2MBPS, RF24_1MBPS, RF24_250KBPS
  //должна быть одинакова на приёмнике и передатчике!
  //при самой низкой скорости имеем самую высокую чувствительность и дальность!!
  
  radio.powerUp(); //начать работу
  radio.startListening();  //начинаем слушать эфир, мы приёмный модуль
  
  Serial.begin(9600); //открываем порт для связи с ПК
}

void loop() {

    timer_now = millis();
    byte pipeNo, gotByte;           
    int gotInt;               
    while( radio.available(&pipeNo)){    // слушаем эфир со всех труб
      //radio.read( &gotByte, sizeof(gotByte) );         // чиатем входящий сигнал
      radio.read( &gotInt, sizeof(gotInt) );
      //Serial.print("Recieved: "); Serial.println(gotInt);
      if (gotInt == 1000) {
        Serial.print("{\"relay work\": "); Serial.print(1); Serial.println("}");
      }
      else if (gotInt == 200) {
        Serial.println("send");
      }
      else {
        // float Temp = float(gotByte);
        float Temp = Therm(gotInt);
        Serial.print("{\"temp out\": "); Serial.print(Temp); Serial.println("}");
      }
   }
   int timer = timer_now - timer_prev;
   if ( timer > 10000 ){
     digitalWrite(PIN_TERM_OUT, HIGH);
     temp_in = Therm(analogRead(PIN_TERM_IN));
     digitalWrite(PIN_TERM_OUT, LOW);
     Serial.print("{\"temp in\": "); Serial.print(temp_in); Serial.println("}");
     //Serial.print("Temp in: ");     Serial.println(temp_in);
     humid = dht.readHumidity();
     temp_dht = dht.readTemperature();
     Serial.print("{\"humidity\": "); Serial.print(humid); Serial.println("}");
     //Serial.print("Humidity: ");     Serial.println(humid);
     Serial.print("{\"temp dht\": "); Serial.print(temp_dht); Serial.println("}");
     //Serial.print("Temp dht: ");     Serial.println(temp_dht);
     timer_prev = timer_now;
   }
   int timer_rel = timer_now - timer_relay_ping;
   if ( timer_rel > 25000 ) {
        nrf_send(999);
        timer_relay_ping = timer_now;
    
    }
   while (Serial.available() > 0) {
    character = Serial.read();
      incoming.concat(character);
      if (incoming == "light on\n" or incoming == "light on") {
        nrf_send(3000);
        //Serial.println("send");
        incoming = "";
        }
      if (incoming == "light off\n" or incoming == "light off") {
        nrf_send(4000);
        //Serial.println("send");
        incoming = "";
        }
      if (incoming == "relay on\n" or incoming == "relay on") {
        nrf_send(1000);
        //Serial.println("send");
        incoming = "";
        }
      if (incoming == "relay off\n" or incoming == "relay off") {
        nrf_send(2000);
        //Serial.println("send");
        incoming = "";
        }
      }
     if (incoming) {incoming = "";};
   delay(100);
}

double Therm(int RawADC) {
  double Temp;
  Temp = log(((10240000/RawADC) - 10000));
  Temp = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * Temp * Temp)) * Temp);
  Temp = Temp - 273.15;
  delay(500);
  return Temp;

}

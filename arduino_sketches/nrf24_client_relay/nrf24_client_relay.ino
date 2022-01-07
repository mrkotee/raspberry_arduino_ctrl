
#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"
//

#define RELAY_PIN A0
#define LIGHT_PIN A3

int light_str = 130; // гирлянда включается на 130


RF24 radio(9,10); // "создать" модуль на пинах 9 и 10 Для Уно

byte address[][6] = {"1Node","2Node","3Node","4Node","5Node","6Node"};  //возможные номера труб


long timer_now;
long timer_prev = millis();


void setup(){
  
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LIGHT_PIN, OUTPUT);
  
  radio.begin(); //активировать модуль
  radio.setAutoAck(1);         //режим подтверждения приёма, 1 вкл 0 выкл
  radio.setRetries(1,15);     //(время между попыткой достучаться, число попыток)
  radio.enableAckPayload();    //разрешить отсылку данных в ответ на входящий сигнал
  radio.setPayloadSize(64);     //размер пакета, в байтах

  radio.openReadingPipe(1,address[1]);      //хотим слушать трубу 0
  radio.openWritingPipe(address[1]);      
  // radio.setChannel(0x70);  //выбираем канал (в котором нет шумов!)
  radio.setChannel(3);

  radio.setPALevel (RF24_PA_LOW); //уровень мощности передатчика. На выбор RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX
  radio.setDataRate (RF24_250KBPS); //скорость обмена. На выбор RF24_2MBPS, RF24_1MBPS, RF24_250KBPS
  //должна быть одинакова на приёмнике и передатчике!
  //при самой низкой скорости имеем самую высокую чувствительность и дальность!!
  
  radio.powerUp(); //начать работу
  radio.startListening();  //начинаем слушать эфир, мы приёмный модуль
  
//  Serial.begin(9600); //открываем порт для связи с ПК
}

void loop() {

    timer_now = millis();
    byte pipeNo, gotByte;           
    int gotInt;               
    while( radio.available(&pipeNo)){    // слушаем эфир со всех труб
      //radio.read( &gotByte, sizeof(gotByte) );         // чиатем входящий сигнал
      radio.read( &gotInt, sizeof(gotInt) );
//      Serial.println(gotInt);
      if (gotInt == 1000) {
        digitalWrite(RELAY_PIN, HIGH);
        nrf_send(200);
      }
      if (gotInt == 2000) {
        digitalWrite(RELAY_PIN, LOW);
        nrf_send(200);
      
      }
      if (gotInt == 3000) {
        analogWrite(LIGHT_PIN, light_str);
        nrf_send(200);
      
      }
      if (gotInt == 4000) {
        analogWrite(LIGHT_PIN, 0);
        nrf_send(200);
      
      }
      if (gotInt == 999) {
        nrf_send(1000);
      
      }
   }
   
   long timer = timer_now - timer_prev;
   if ( timer > 30000 ){
    nrf_send(1000);
    timer_prev = timer_now;
    }
  
   delay(10);
}

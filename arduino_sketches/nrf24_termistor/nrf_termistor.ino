
#include <SPI.h>          // библиотека для работы с шиной SPI
#include "nRF24L01.h"     // библиотека радиомодуля
#include "RF24.h"         // ещё библиотека радиомодуля



#define PIN_TERM_OUT A1

RF24 radio(9, 10); // "создать" модуль на пинах 9 и 10 Для Уно

byte address[][6] = {"1Node", "2Node", "3Node", "4Node", "5Node", "6Node"}; //возможные номера труб

long timer_now;
long timer_prev = 0;

//float temp_out;



void setup() {

  radio.begin(); //активировать модуль
  radio.setAutoAck(1);         //режим подтверждения приёма, 1 вкл 0 выкл
  radio.setRetries(1, 15);    //(время между попыткой достучаться, число попыток)
  radio.enableAckPayload();    //разрешить отсылку данных в ответ на входящий сигнал
  radio.setPayloadSize(64);     //размер пакета, в байтах

  radio.openWritingPipe(address[0]);   //мы - труба 0, открываем канал для передачи данных
  // radio.setChannel(0x70);  //выбираем канал (в котором нет шумов!)
  radio.setChannel(3);

  radio.setPALevel (RF24_PA_MAX); //уровень мощности передатчика. На выбор RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX
  radio.setDataRate (RF24_250KBPS); //скорость обмена. На выбор RF24_2MBPS, RF24_1MBPS, RF24_250KBPS
  //должна быть одинакова на приёмнике и передатчике!
  //при самой низкой скорости имеем самую высокую чувствительность и дальность!!

  // radio.powerUp(); //начать работу
  // radio.stopListening();  //не слушаем радиоэфир, мы передатчик

  //Serial.begin(9600); //открываем порт для связи с ПК
}

void loop() {

  timer_now = millis();
  //Serial.println(analogRead(PIN_TERM_OUT));
  if (timer_now > timer_prev){
    timer_prev = timer_now + 60000;

    //temp_out = Therm(analogRead(PIN_TERM_OUT));
    nrf_send(analogRead(PIN_TERM_OUT));
    }
  delay(300);
    
  }

  

double Therm(int RawADC) {
  double Temp;
  Temp = log(((10240000/RawADC) - 10000));
  Temp = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * Temp * Temp)) * Temp);
  Temp = Temp - 273.15;
  delay(500);
  return Temp;

}

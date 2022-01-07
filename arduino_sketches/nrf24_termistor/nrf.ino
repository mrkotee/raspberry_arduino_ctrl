


void nrf_send(int Temp) {
  // byte sendData = byte(Temp);
  //Serial.println(sendData);
  radio.powerUp(); //начать работу
  radio.stopListening();  //не слушаем радиоэфир, мы передатчик
  radio.write(&Temp, sizeof(Temp));
  //radio.write(&sendData, sizeof(sendData));
  radio.powerDown();
  delay(10);
  
}


void nrf_send(int msg) {
  radio.stopListening();  //не слушаем радиоэфир, мы передатчик
  radio.write(&msg, sizeof(msg));
  radio.startListening();
  delay(10);
  
}

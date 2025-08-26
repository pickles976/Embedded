#include <Arduino.h>
#include <VirtualWire.h>

#define TX_PIN 12
#define RX_PIN 11
#define BITRATE 2000

// #define TRANSMITTER true

# ifdef TRANSMITTER

void setup() {
  Serial.begin(9600);
  Serial.println("Starting...");
  vw_set_tx_pin(TX_PIN);
  vw_setup(BITRATE); // bits/sec
}

void loop() {
  const char *msg = "hello";

  digitalWrite(13, true); // Flash a light to show transmitting
  vw_send((uint8_t *)msg, strlen(msg));
  vw_wait_tx(); // Wait until the whole message is gone
  digitalWrite(13, false);
  delay(1000);
}

# else

#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

void setup() {
  Serial.begin(9600);
  Serial.println("Starting");
  vw_set_rx_pin(RX_PIN);
  vw_setup(BITRATE); // bits/sec
  vw_rx_start();
}

void print_hex(uint8_t *buf, uint8_t buflen) {
    // Message with a good checksum received, dump it.
	  int i;
    Serial.print("Got: ");
  
    for (i = 0; i < buflen; i++)
    {
      Serial.print(buf[i], HEX);
      Serial.print(" ");
    }
    Serial.println("");
}

void print_string(uint8_t *buf, uint8_t buflen) {
  // Null-terminate the received message
  buf[buflen] = '\0';  // Safe because VW_MAX_MESSAGE_LEN is 80 by default

  // Cast to char* and print as string
  Serial.print("Got string: ");
  Serial.println((char *)buf);  // or: Serial.println((char*)buf);
}

void loop() {
  uint8_t buf[VW_MAX_MESSAGE_LEN];
  uint8_t buflen = VW_MAX_MESSAGE_LEN;

  if (vw_get_message(buf, &buflen)) // Non-blocking
  {
    digitalWrite(13, true); // Flash a light to show received good message

    print_hex(buf, buflen);
    print_string(buf, buflen);

    digitalWrite(13, false);
  }

}

# endif

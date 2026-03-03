#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 mfrc522(SS_PIN, RST_PIN);
Servo doorServo;

String authorizedUID = "F416B5a";   

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();

  doorServo.attach(6);
  doorServo.write(0);  

  Serial.println("Scan RFID...");
}

void loop() {

  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  String content = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    content += String(mfrc522.uid.uidByte[i], HEX);
  }

  content.toUpperCase();
  Serial.println(content);

  if (content == authorizedUID) {
    Serial.println("VALID");
    doorServo.write(90);   // Unlock
    delay(3000);
    doorServo.write(0);    // Lock again
  }
  else {
    Serial.println("INVALID");
  }

  delay(1000);
}
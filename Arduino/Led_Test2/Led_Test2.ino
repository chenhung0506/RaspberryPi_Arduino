// 控制站
const int RELAY_PIN_1 = 9;
const int RELAY_PIN_2 = 10;
const int RELAY_PIN_3 = 11;
const int RELAY_PIN_4 = 12;
const int SLEEP = 500;

void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN_1, OUTPUT);
  pinMode(RELAY_PIN_2, OUTPUT);
  pinMode(RELAY_PIN_3, OUTPUT);
  pinMode(RELAY_PIN_4, OUTPUT);
}

void loop() {
  if(Serial.available() > 0) {
    char c = Serial.read();
    Serial.print(c);  // 電腦顯示
    switch(c){
      case '1':
        digitalWrite(RELAY_PIN_1, HIGH);
        digitalWrite(RELAY_PIN_2, LOW);
        digitalWrite(RELAY_PIN_3, LOW);
        digitalWrite(RELAY_PIN_4, LOW);
        break;
      case '2':
        digitalWrite(RELAY_PIN_1, LOW);
        digitalWrite(RELAY_PIN_2, HIGH);
        digitalWrite(RELAY_PIN_3, LOW);
        digitalWrite(RELAY_PIN_4, LOW);
        break;
      case '4':
        digitalWrite(RELAY_PIN_1, LOW);
        digitalWrite(RELAY_PIN_2, LOW);
        digitalWrite(RELAY_PIN_3, HIGH);
        digitalWrite(RELAY_PIN_4, LOW);
        break;
      case '8':
        digitalWrite(RELAY_PIN_1, LOW);
        digitalWrite(RELAY_PIN_2, LOW);
        digitalWrite(RELAY_PIN_3, LOW);
        digitalWrite(RELAY_PIN_4, HIGH);
        break;
    }
  }
  
}
// 蜂鳴器
const int BUZEER_PIN = 8;
// 控制站
const int RELAY_PIN_1 = 9;
const int RELAY_PIN_2 = 10;
const int RELAY_PIN_3 = 11;
const int RELAY_PIN_4 = 12;
// 休息
const int SLEEP = 500;
const int BUZEER_SLEEP = 100;

void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN_1, OUTPUT);
  pinMode(RELAY_PIN_2, OUTPUT);
  pinMode(RELAY_PIN_3, OUTPUT);
  pinMode(RELAY_PIN_4, OUTPUT);
  pinMode(BUZEER_PIN, OUTPUT);
}

void loop() {
  if(Serial.available() > 0) {
    int c = Serial.parseInt();
    //String c = Serial.readStringUntil('\n');
    Serial.println(c);  // 電腦顯示
    switch(c){
      case 1:
        digitalWrite(RELAY_PIN_1, HIGH);
        digitalWrite(RELAY_PIN_2, LOW);
        digitalWrite(RELAY_PIN_3, LOW);
        digitalWrite(RELAY_PIN_4, LOW);
        sound();
        break;
      case 2:
        digitalWrite(RELAY_PIN_1, LOW);
        digitalWrite(RELAY_PIN_2, HIGH);
        digitalWrite(RELAY_PIN_3, LOW);
        digitalWrite(RELAY_PIN_4, LOW);
        sound();
        break;
      case 4:
        digitalWrite(RELAY_PIN_1, LOW);
        digitalWrite(RELAY_PIN_2, LOW);
        digitalWrite(RELAY_PIN_3, HIGH);
        digitalWrite(RELAY_PIN_4, LOW);
        sound();
        break;
      case 8:
        digitalWrite(RELAY_PIN_1, LOW);
        digitalWrite(RELAY_PIN_2, LOW);
        digitalWrite(RELAY_PIN_3, LOW);
        digitalWrite(RELAY_PIN_4, HIGH);
        sound();
        break;
    }
    
  }
}

void sound() {
    digitalWrite(BUZEER_PIN, HIGH);                       // 蜂鳴器 開
    delay(BUZEER_SLEEP);                                     // 發音時間
    digitalWrite(BUZEER_PIN, LOW);                        // 蜂鳴器 關
}
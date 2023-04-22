#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SimpleDHT.h>
#include <ezButton.h>

// 设置 LiquidCrystal_I2C 对象并指定 I2C 地址
LiquidCrystal_I2C lcd(0x27, 16, 2);

const int pinDHT11 = 7;

ezButton button(2);
SimpleDHT11 dht11; // DHT 11 測量溫濕度
byte temperature = 0; // 溫度
byte humidity = 0; // 濕度
boolean buttonState = 0; // button 電壓

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

  randomSeed(analogRead(0)); // 隨機種子
  
  // 初始化 I2C 总线
  Wire.begin();
  // 初始化 LCD
  lcd.init();
  
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("TEMP:   HUMD:");
  lcd.setCursor(0, 1);
  lcd.print("Data:   Mode:");
  
}

void loop() {
  // 接收命令
  rec();
  // 傳送資料
  send();
}

void send() {
  button.loop(); // 一定加上

  if(button.isPressed())
    buttonState = !buttonState;
  
  // 讀取溫濕度
  if (dht11.read(pinDHT11, &temperature, &humidity, NULL) == SimpleDHTErrSuccess) {
    lcd.setCursor(5, 0);
    lcd.print("   ");
    lcd.setCursor(5, 0);
    lcd.print((int)temperature);
    lcd.setCursor(13, 0);
    lcd.print("   ");
    lcd.setCursor(13, 0);
    lcd.print((int)humidity);
  }
    
  int random_num = random(0, 100); // 0~99 亂數
  
  if (buttonState) {
    lcd.setCursor(13, 1);
    lcd.print("OFF");
  } else {
    lcd.setCursor(13, 1);
    lcd.print("   ");
    lcd.setCursor(13, 1);
    lcd.print("ON");
    lcd.setCursor(5, 1);
    lcd.print("  ");
    lcd.setCursor(5, 1);
    lcd.print(random_num);

    // 傳送
    Serial.print(random_num);
    Serial.print(",");
    Serial.print((int)temperature);
    Serial.print(",");
    Serial.println((int)humidity);
    
  }
  delay(100);
}

void rec() {
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


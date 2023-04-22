#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// 设置 LiquidCrystal_I2C 对象并指定 I2C 地址
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(115200);

  // 初始化 I2C 总线
  Wire.begin();

  // 初始化 LCD
  lcd.init();

  // 在第一行上显示一条消息
  lcd.backlight();
  lcd.setCursor(0, 1);
  lcd.print("Hello");
}

void loop() {
  // 如果串口有数据可用
  if (Serial.available() > 0) {
    // 读取数据并显示在 LCD 的第二行上
    lcd.setCursor(0, 0);
    String data = Serial.readStringUntil('\n');
    //Serial.println(data);
    lcd.print(data);
  }
}

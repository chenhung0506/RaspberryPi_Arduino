void setup() {
  Serial.begin(115200);
  randomSeed(analogRead(0)); // 隨機種子
}

void loop() {
  int random_num = random(0, 100); // 0~99 亂數
  Serial.println(random_num);
  delay(1000);
}

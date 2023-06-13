#define SCLK 7 
#define RCLK 6
#define DIO 5
#define redPin 8
#define greenPin 9

byte digits[4] = {0, 1, 2, 3}; 
byte i = 3;

bool isWarn = false;
int showSeg = 0;
int val1;  
int val2; 

const byte cabinet[7][4] = {
  { 0b11000110, 0b10001000, 0b00000000, 0b11000000 },
  { 0b11000110, 0b10001000, 0b00000000, 0b11111001 },
  { 0b11000110, 0b10001000, 0b00000000, 0b10110000 },
  { 0b11000110, 0b10001000, 0b00000000, 0b10100100 },
  { 0b11000110, 0b10001000, 0b00000000, 0b10011001 },
  { 0b11000110, 0b10001000, 0b00000000, 0b10010010 },
  { 0b11000110, 0b10001000, 0b00000000, 0b10000010 }
};

const byte chr[] = { 
  0b00001000,
  0b00000100,
  0b00000010,
  0b00000001
};

unsigned long previousTime = 0;
const unsigned long interval = 0.1; 

void setup() {
  pinMode(RCLK, OUTPUT);
  pinMode(SCLK, OUTPUT);
  pinMode(DIO, OUTPUT);
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  unsigned long currentTime = millis();

  if (currentTime - previousTime >= interval) {
    previousTime = currentTime;

    showDisplay(cabinet[showSeg]);

    if (isWarn == true){
      digitalWrite(redPin, HIGH);
      digitalWrite(greenPin, LOW);
    } else {
      digitalWrite(redPin, LOW);
      digitalWrite(greenPin, HIGH);
    }
  }

  if (Serial.available() >= 2){
    char data[3];
    Serial.readBytes(data, 2);  
    data[2] = '\0';  

    // val1과 val2 값을 각각 파싱
    val1 = data[0] - '0';  
    val2 = data[1] - '0';  

    if (val1 == 1){
      isWarn = true;
    } else if (val1 == 0){
      isWarn = false;
    }

    switch(val2){
      case 0 : 
        showSeg = 0;
        break;
      case 1 : 
        showSeg = 1;
        break;
      case 2 : 
        showSeg = 2;
        break;
      case 3 : 
        showSeg = 3;
        break;
      case 4 : 
        showSeg = 4;
        break;
      case 5 : 
        showSeg = 5;
        break;
    }
  }
}

void showDisplay(const byte* caninet) {
  digitalWrite(RCLK, LOW); 
  shiftOut(DIO, SCLK, MSBFIRST, caninet[digits[i]]); 
  shiftOut(DIO, SCLK, MSBFIRST, chr[i]); 
  digitalWrite(RCLK, HIGH); 
  i++;
  if (i > 3) i = 0;
}

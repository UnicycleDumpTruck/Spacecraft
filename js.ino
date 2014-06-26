#include <SPI.h>
#include <SoftwareSerial.h>

//#define xmas_color_t uint16_t // typedefs can cause trouble in the Arduino environment  
#define XMAS_LIGHT_COUNT          (25) //I only have a 36 light strand. Should be 50 or 36  
#define XMAS_CHANNEL_MAX          (0xF)  
#define XMAS_DEFAULT_INTENSITY     (0xCC)  
#define XMAS_HUE_MAX               ((XMAS_CHANNEL_MAX+1)*6-1)  
#define XMAS_COLOR(r,g,b)     ((r)+((g)<<4)+((b)<<8))  
#define XMAS_COLOR_WHITE     XMAS_COLOR(XMAS_CHANNEL_MAX,XMAS_CHANNEL_MAX,XMAS_CHANNEL_MAX)  
#define XMAS_COLOR_BLACK     XMAS_COLOR(0,0,0)  
#define XMAS_COLOR_RED          XMAS_COLOR(XMAS_CHANNEL_MAX,0,0)  
#define XMAS_COLOR_OFFRED          XMAS_COLOR(XMAS_CHANNEL_MAX,0,(XMAS_CHANNEL_MAX / 4))  
#define XMAS_COLOR_GREEN     XMAS_COLOR(0,XMAS_CHANNEL_MAX,0)  
#define XMAS_COLOR_BLUE          XMAS_COLOR(0,0,XMAS_CHANNEL_MAX)  
#define XMAS_COLOR_CYAN          XMAS_COLOR(0,XMAS_CHANNEL_MAX,XMAS_CHANNEL_MAX)  
#define XMAS_COLOR_MAGENTA     XMAS_COLOR(XMAS_CHANNEL_MAX,0,XMAS_CHANNEL_MAX)  
#define XMAS_COLOR_YELLOW     XMAS_COLOR(XMAS_CHANNEL_MAX,XMAS_CHANNEL_MAX,0)  
   
// Pin setup  
#define XMASPIN 7 // I drive the LED strand from pin #4  
//#define XMASPINTWO 4
#define STATUSPIN 13 // The LED  

#define LEDTOP    10
#define LEDBOTTOM  3
#define LEDLEFT    9
#define LEDRIGHT  11 // Correct

//Defined Colors (different RGB (red, green, blue) values for colors
const byte RED[] = {0, 255, 255}; 
const byte ORANGE[] = {172, 251, 255}; 
const byte YELLOW[] = {0, 200, 255}; 
const byte GREEN[] = {255, 0, 255}; 
const byte BLUE[] = {255, 255, 0}; 
const byte CYAN[] = {255, 0, 0}; 
const byte MAGENTA[] = {0, 255, 200}; 
const byte WHITE[] = {0, 50, 150}; 
const byte WARMWHITE[] = {0, 170, 240};
const byte BLACK[] = {255, 255, 255}; //?
const byte PURPLE[] = {100, 255, 160}; 

static uint16_t c;
String lastCommandString = "";
byte lastCommand[] = {255, 255, 255};

uint8_t strandIntensity = 0x0;
uint8_t ledTopLevel     = 0;
uint8_t ledBottomLevel  = 0;
uint8_t ledLeftLevel    = 0;
uint8_t ledRightLevel   = 0;


// The delays in the begin, one, and zero functions look funny, but they give the correct  
// pulse durations when checked with a logic analyzer. Tested on an Arduino Uno.  
   
 void xmas_begin(int pin)  
 {  
  digitalWrite(pin,1);  
  delayMicroseconds(7); //The pulse should be 10 uS long, but I had to hand tune the delays. They work for me  
  digitalWrite(pin,0);   
 }  
   
 void xmas_one(int pin)  
 {  
  digitalWrite(pin,0);  
  delayMicroseconds(11); //This results in a 20 uS long low  
  digitalWrite(pin,1);  
  delayMicroseconds(7);   
  digitalWrite(pin,0);  
 }  
   
 void xmas_zero(int pin)  
 {  
  digitalWrite(pin,0);  
  delayMicroseconds(2);   
  digitalWrite(pin,1);  
  delayMicroseconds(20-3);   
  digitalWrite(pin,0);  
 }  
   
 void xmas_end(int pin)  
 {  
  digitalWrite(pin,0);  
  delayMicroseconds(40); // Can be made shorter  
 }  
   
   
 // The rest of Robert's code is basically unchanged  
   
 void xmas_fill_color(uint8_t begin,uint8_t count,uint8_t intensity,uint16_t color)  
 {  
      uint8_t led = count;
      while(led--)  
      {  
           xmas_set_color(XMASPIN,begin++,intensity,color);
           //delay(100);
      }
//      delay(100);
//      led = count;
//      while(led--)  
//      {  
//           xmas_set_color(XMASPINTWO,begin++,intensity,color);
//           delay(100);
//      }      
 }  
   
 void xmas_fill_color_same(uint8_t begin,uint8_t count,uint8_t intensity,uint16_t color)  
 {  
      while(count--)  
      {  
           xmas_set_color(XMASPIN,0,intensity,color);  
      }  
 }  
   
   
 void xmas_set_color(uint8_t pin,uint8_t led,uint8_t intensity,uint16_t color) {  
      uint8_t i;  

      xmas_begin(pin);  
      for(i=6;i;i--,(led<<=1))  
           if(led&(1<<5))  
                xmas_one(pin);  
           else  
                xmas_zero(pin);  
      for(i=8;i;i--,(intensity<<=1))  
           if(intensity&(1<<7))  
                xmas_one(pin);  
           else  
                xmas_zero(pin);  
      for(i=12;i;i--,(color<<=1))  
           if(color&(1<<11))  
                xmas_one(pin);  
           else  
                xmas_zero(pin);  
      xmas_end(pin);  
}  
   
   
uint16_t xmas_color(uint8_t r,uint8_t g,uint8_t b) {  
      return XMAS_COLOR(r,g,b);  
 }  
   
uint16_t xmas_color_hue(uint8_t h) {  
      switch(h>>4) {  
           case 0:     h-=0; return xmas_color(h,XMAS_CHANNEL_MAX,0);  
           case 1:     h-=16; return xmas_color(XMAS_CHANNEL_MAX,(XMAS_CHANNEL_MAX-h),0);  
           case 2:     h-=32; return xmas_color(XMAS_CHANNEL_MAX,0,h);  
           case 3:     h-=48; return xmas_color((XMAS_CHANNEL_MAX-h),0,XMAS_CHANNEL_MAX);  
           case 4:     h-=64; return xmas_color(0,h,XMAS_CHANNEL_MAX);  
           case 5:     h-=80; return xmas_color(0,XMAS_CHANNEL_MAX,(XMAS_CHANNEL_MAX-h));  
      }  
 }  


// Serial
String command; // Used for debugging to print the chars to the Serial Monitor
int commandValue = 0;
char charIn;
int rxCmnd[5];

void processSerial (void)
{
  uint8_t cmndPos = 0;
  commandValue = 0;
  if (Serial.available()) {
    delay(5); // wait for all data to come in
    while(Serial.available() > 0) {
      charIn = Serial.read();
      if (charIn == '\n') {
        decodeCommand();
      } else {
        if (charIn == ',') {
          //rxCmnd[cmndPos] = commandValue;
          //commandValue = 0;
          cmndPos++;
        } else {
          //if( isDigit(charIn) )// is this an ascii digit between 0 and 9?
          //{
            rxCmnd[cmndPos] = (charIn - '0');
            //commandValue = (commandValue * 10) + (charIn - '0'); // yes, accumulate the value
          //}          
        }
      }
    }
  }
}

void decodeCommand(void)
{
  strandIntensity = (rxCmnd[0] * 20);
  ledTopLevel     = (rxCmnd[1] * 28);
  ledBottomLevel  = (rxCmnd[2] * 28);
  ledLeftLevel    = (rxCmnd[3] * 28);
  ledRightLevel   = (rxCmnd[4] * 28);
  
  analogWrite(LEDTOP, ledTopLevel);
  analogWrite(LEDBOTTOM, ledBottomLevel);
  analogWrite(LEDLEFT, ledLeftLevel);
  analogWrite(LEDRIGHT, ledRightLevel);
  
//  strandIntensity = (50);

//  strandIntensity = XMAS_DEFAULT_INTENSITY;
  
  /*if (rxCmnd[0] == 1) {
    switch (rxCmnd[1]) {
      case 4:      
      //ledOn(matrixE, EBuffer, rxCmnd[3], rxCmnd[4]);
      break;
    }
  } else if (rxCmnd[0] == 0) {
    switch (rxCmnd[1]) {
      case 4:      
      //ledOff(matrixE, EBuffer, rxCmnd[3], rxCmnd[4]);
      break;
    }
    
  } else if (rxCmnd[0] == 2) { // Set bargraphs
      //cBarDisp(matrixC, CBuffer, cryoCats, cryoAns, rxCmnd[1],rxCmnd[2]);
  }
  */
  for (uint8_t i=0; i<5; i++) {
    rxCmnd[i] = 0;
  }
}


void setup ()
{
  Serial.begin (115200);  // for debugging via serial terminal on computer
  
  pinMode(XMASPIN, OUTPUT);  
  pinMode(STATUSPIN, OUTPUT);  
  xmas_fill_color(0,XMAS_LIGHT_COUNT,XMAS_DEFAULT_INTENSITY,XMAS_COLOR_BLACK); //Enumerate all the lights  
  xmas_fill_color(0,XMAS_LIGHT_COUNT,XMAS_DEFAULT_INTENSITY,XMAS_COLOR_RED);
  strandIntensity = XMAS_DEFAULT_INTENSITY;
  randomSeed(analogRead(0));
}

void loop() {
  processSerial();
  xmas_fill_color(0,XMAS_LIGHT_COUNT,strandIntensity,XMAS_COLOR_RED);
  delay(20);
  for(int i=0; i<24; i++) {
      xmas_set_color(XMASPIN,random(0,24),strandIntensity,XMAS_COLOR_OFFRED);
  }
  //processSerial();
  xmas_set_color(XMASPIN,random(0,24),strandIntensity,XMAS_COLOR_YELLOW);
}

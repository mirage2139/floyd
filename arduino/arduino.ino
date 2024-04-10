#include <SoftwareSerial.h>
#include <DFPlayerMini_Fast.h>  
#include <Arduino.h>
#include <Ds1302.h>

#define led0 2
#define led1 3
#define led2 4
#define module 5
#define butt 8
#define micro A5
#define photo A0
#define clck 35
#define dat 37
#define rst 39
#define wemosrx 42
#define wemostx 40

SoftwareSerial myMP3(52, 53);
SoftwareSerial wemos(wemosrx, wemostx);
DFPlayerMini_Fast myMP3; 
Ds1302 rtc(rst, clck, dat);



bool flag = 0;
bool time = 1;
bool mic = 1;
float volt = 0;
int value, modval, value1;

void setup() {
  Serial.begin(9600);
  pinMode(led0, OUTPUT);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(butt, INPUT_PULLUP);
  pinMode(module, INPUT);
  mySerial.begin(9600); 
  myMP3.begin(myMP3); 
  myMP3.volume(30);
  rtc.init();
}

int timeget(){
  return now.hour;
}
void lights(){
  modval = digitalRead(module);
  value = analogRead(photo);
  hrs = ;
  if ((value < 40 && modval) || (time && (hrs > 19 || hrs < 7))) {
    for (int x = 0; x < 1500; x++){
      digitalWrite(led0, HIGH);
      digitalWrite(led1, HIGH);
      digitalWrite(led2, HIGH);
      alarm();
      delay(100);
      value = analogRead(photo);
      hrs = ;
      if ((value > 40)||(time && (hrs < 19 || hrs > 7))){
        digitalWrite(led0, LOW);
        digitalWrite(led1, LOW);
        digitalWrite(led2, LOW);
        break;
      }
    }
  } else if ((value < 40 && !modval)||(value > 40)||(time && (hrs < 19 || hrs > 7))){
    digitalWrite(led0, LOW);
    digitalWrite(led1, LOW);
    digitalWrite(led2, LOW);
  }
  alarm();
}

void alarm() {
  value1  = !digitalRead(butt);
  volt = analogRead(micro) * 5 / 1024
  if ((value1 == 1 && flag == 0)|||| (volt > 2.2 && mic)){
    flag = 1;
  }else if ((value1 == 1 && flag == 1)||(volt <  2.2 && mic)){
    flag = 0;
  }
  if ((flag == 1 && value1 == 1) || (mic && volts > 2.2)){
    digitalWrite(led0, LOW);
    digitalWrite(led1, LOW);
    digitalWrite(led2, LOW);
    myMP3.play(2);
    delay(3000);
    myMP3.play(1);
    for (int x = 0; x < 20; x++){
      digitalWrite(led2, LOW);
      digitalWrite(led1, HIGH);
      delay(270);
      digitalWrite(led1, LOW);
      digitalWrite(led2, HIGH);
      delay(270);
    }
    myMP3.stop();
  }
}

void alarmeter(){
      char wms = wemos.read();
      digitalWrite(led0, LOW);
      digitalWrite(led1, LOW);
      digitalWrite(led2, LOW);
      myMP3.play(2);
      delay(3000);
      myMP3.play(1);
      for (int x = 0; x < 20; x++){
        digitalWrite(led2, LOW);
        digitalWrite(led1, HIGH);
        delay(270);
        digitalWrite(led1, LOW);
        digitalWrite(led2, HIGH);
        delay(270);
      }
      myMP3.stop();
}

void etlights(){
  char wms = wemos.read();
  while (wms != 't'){
      digitalWrite(led0, HIGH);
      digitalWrite(led1, HIGH);
      digitalWrite(led2, HIGH);
      alarm();
      delay(100);
      char wms = wemos.read();
      char srl = Serial.read();
      if (wms == 't' or srl == 't'){// light no
          break;
      }else if (wms == 'o' or srl == 'o'){//light yes
          etlights();
      }else if (wms == 'a' or srl == 'a'){//alarm
          alarmeter();
      }else if (wms == 'v' or srl == 'v'){//microon
        mic = true;
      }else if (wms == 'w'  or srl == 'w'){//microoff
        mic = true;
      }else if (wms == 'r' or srl == 'r'){//rtc
        time = false;
      }else if (wms == 'e' or srl == 'e'){//rtc
        time = true;
      }
      wms = ' '; srl = ' ';
  }
    digitalWrite(led0, LOW);
    digitalWrite(led1, LOW);
    digitalWrite(led2, LOW);
}

void loop() {
  char wms = wemos.read();
  char srl = Serial.read();
  Serial.println(wms);
  Serial.write(wms);
  wemos.println(srl);
  wemos.write(srl);
  if (wms == 't' or srl == 't'){// light no
    lights();
  }else if (wms == 'o' or srl == 'o'){//light yes
    etlights();
  }else if (wms == 'a' or srl == 'a'){//alarm
    alarmeter();
  }else if (wms == 'v' or srl == 'v'){//microon
    mic = true;
  }else if (wms == 'w' or srl == 'w'){//microoff
    mic = true;
  }else if (wms == 'r' or srl == 'r'){//rtc
    time = false;
  }else if (wms == 'e' or srl == 'e'){//rtc
    time = true;
  }
  wms = ' '; srl = ' ';
}
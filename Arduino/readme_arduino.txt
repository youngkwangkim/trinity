아두이노도 소스코드가 아닌 .ino 파일을 첨부했습니다. 혹시 아두이노가 설치가 안됐을 수도 있기 때문에

txt 파일에 소스코드를 따로 올리겠습니다.

#include <SoftwareSerial.h>
SoftwareSerial BTSerial(2,3); //RX TX

int relay = 4;

int button1Pin = 5;                // choose the pin for the LED
int button2Pin = 7;
int redPin = 13;
int greenPin = 12;
int bluePin = 11;  

int pirPin = 8;  // choose the input pin (for PIR sensor)
int waterPin = A5;
int lightPin = A3;

int button1Count = 0;  
int button2Count = 0;
int pir = 0;
int water =0;
int light =0;                 // variable for reading the pin status
int button1 =0;
int button2 =0;
char inSerial[15];

int pirValue = 0;
 
void setup() 
{
  Serial.begin(9600);
  BTSerial.begin(9600);
  
  pinMode(relay, OUTPUT);

  pinMode(pirPin, INPUT);
  pinMode(waterPin, INPUT);
  pinMode(lightPin, INPUT);
         
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  pinMode(button1Pin, INPUT);    
  pinMode(button2Pin, INPUT);    
}

void setColor(int red, int green, int blue) 
{
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);
}

void loop()
{
  int i=0;
  int m=0;
  //delay(500);
  
  if(BTSerial.available() > 0) 
  {
    while(BTSerial.available() > 0) 
    {
      inSerial[i]=BTSerial.read();
      i++;
    }
    inSerial[i]='\0';
    Check_Protocol(inSerial);
  }

  pir = digitalRead(pirPin);         
  water = analogRead(waterPin);
  light = analogRead(lightPin);
  button1 = digitalRead(button1Pin);
  button2 = digitalRead(button2Pin);

  if(button1 == 0)
  {
    button1Count++;
  }

  if(button1Count %2 != 0)
  {
    setColor(255,255,255); //white
  }
  else
  {
    setColor(0,0,0); // off
  }

  if(button2 == 0)
  { 
    button2Count++; 
  }

  if(button2Count %2 != 0)
  {
    digitalWrite(relay, HIGH);
  }
  else
  {
    digitalWrite(relay, LOW);
  }
  
   
  Serial.print(pir);  
  Serial.print(" ");
  Serial.print(water);
  Serial.print(" ");
  Serial.print(light);
  Serial.print(" ");
  Serial.print(button1Count);
  Serial.print(" ");
  Serial.println(button2Count);
  delay(1000);
}

void Check_Protocol(char inStr[]) 
{
  int i=0;
  int m=0;
  //Serial.println(inStr);

//PUMP OFF
  if(!strcmp(inStr, "1off")) 
  {
    if(button2Count %2 ==0) { }
    else {
    button2Count++;
    
    for(m=0; m<11; m++) 
    {
      inStr[m]=0;
    }
    i=0;
    }
  }
  
//PUMP ON 
  if(!strcmp(inStr, "1on")) 
  {
    if(button2Count %2 !=0) { }
    else {
    button2Count++;

    for(m=0; m<11; m++) 
    {
      inStr[m]=0;
    }
    i=0;
    }
  }

//LED OFF
  if(!strcmp(inStr, "2off")) 
  {
    if(button1Count %2 == 0) { }
    else {
    button1Count++;
    
    for(m=0; m<11; m++) 
    {
      inStr[m]=0;
    }
    i=0;
    }
  }
//LED ON
  if(!strcmp(inStr, "2on")) 
  {
    if(button1Count %2 != 0) { }
    else {
    button1Count++;

    for(m=0; m<11; m++) 
    {
      inStr[m]=0;
    }
    i=0;
    }
  } 
  else 
  {
    for(m=0; m<11; m++) 
    {
      inStr[m]=0;
    }
    i=0;
  }
}
  

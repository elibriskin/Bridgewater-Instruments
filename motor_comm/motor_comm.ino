

#define directionPin 2
#define stepPin 3

int stepsPerRevolution = 1600;

void rotate(int degrees){
  if(degrees > 0){
    int turn = (degrees * 1600L)/360;
      for (int i = 0; i < turn; i++){
        digitalWrite(directionPin, HIGH);
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(140);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(140);
      }
  } else if (degrees < 0) {
    int turn = ((-1*degrees) * 1600L)/360;
      for (int i = 0; i < turn; i++){
        digitalWrite(directionPin, LOW);
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(140);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(140);
      }
  }
  

}


void setup()
{
  //An LED is Connected Pin12 
  pinMode(directionPin, OUTPUT);
  pinMode(stepPin, OUTPUT);

  Serial.begin(115200); // opens serial port, sets data rate to 9600 bps 8N1

}

void loop()
{
  String degreeString = "";
  int degrees = 0;

 if (Serial.available()) 
    {
      
      degreeString = Serial.readString();
      degrees = degreeString.toInt();
      rotate(degrees);
       

    }//endof if 
}
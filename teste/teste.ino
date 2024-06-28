char input = '0'; //serial input is stored in this variable
int x = 90;
int y = 90;

int buzzer = 9;

int upLed = 10;
int rightLed = 11;
int downLed = 13;
int leftLed = 12;// branco (up), vermelho (right), verde (down), amarelo (left)

void setup() {
  Serial.begin(9600);
  pinMode(upLed, OUTPUT);
  pinMode(rightLed, OUTPUT);
  pinMode(downLed, OUTPUT);
  pinMode(leftLed, OUTPUT);
  pinMode(buzzer, OUTPUT);
}

void onLed(int pin) {
  digitalWrite(pin, HIGH);
  delay(50);
  digitalWrite(pin, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
 if(Serial.available()){ //checks if any data is in the serial buffer
  input = Serial.read(); //reads the data into a variable

  if (input == '1') {
    tone(buzzer, 5);
    delay(500);
    noTone(buzzer);
  }
  // } else if(input == 'U'){
  //  onLed(upLed);    //adjusts the servo angle according to the input
  //  y += 1;               //updates the value of the angle
  // }
  // else if(input == 'D'){ 
  //  onLed(downLed);
  //  y -= 1;
  // }
  
  else if(input == 'L'){
   onLed(leftLed);
  x -= 1;
  } else if(input == 'R'){
  onLed(rightLed);
  x += 1;
  }
  else{
  Serial.println(x);
  }
  input = '0';           //clears the variable
 }
 //process keeps repeating!! :)
}

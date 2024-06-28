#include <Servo.h>

Servo servoH; // Servo Horizontal

int ledPin = 13;           // Pino do LED
int buzzerPin = 9;         // Pino do Buzzer
int servoHPin = 10;        // Pino do Servo Horizontal
int servoHAngle = 90;      // Ângulo que o servo horizontal vai girar
int rotationItensity = 5; // Intensidade da rotação

int leftLed = 11;
int rightLed = 12;

void setup()
{
  pinMode(ledPin, OUTPUT);    // Configura o pino do LED como saída
  pinMode(leftLed, OUTPUT);
  pinMode(rightLed, OUTPUT);
  pinMode(buzzerPin, OUTPUT); // Configura o pino do Buzzer como saída
  servoH.attach(servoHPin);   // Configura a conexão do Servo Horizontal com o pino;
  Serial.begin(9600);         // Inicializa a comunicação serial
}

void loop()
{
  if (Serial.available() > 0)
  {
    char command = Serial.read(); // Lê o comando enviado pelo Python
    if (command == '1')
    {
      digitalWrite(buzzerPin, HIGH);
    } if (command == '0') {
      digitalWrite(buzzerPin, LOW);
    } if (command == 'L')
    {
      // servoHAngle -= rotationItensity;
      digitalWrite(leftLed, HIGH);
      digitalWrite(rightLed, LOW);
    }
    if (command == 'R')
    {
      // servoHAngle += rotationItensity;
      digitalWrite(rightLed, HIGH);
      digitalWrite(leftLed, LOW);
    }
    command = '0'; // clears the variable
  }

servoH.write(servoHAngle);
}

#include <Servo.h>

Servo servoH, servoV; // Servo Horizontal e vertical

int ledPin = 13;

int servoHPin = 10;   // Pino do Servo Horizontal
int servoHAngle = 90; // Ângulo que o servo horizontal vai girar

int servoVPin = 9;
int servoVAngle = 90;

int rotationItensity = 10; // Intensidade da rotação

void blinkLed(int ledPin) {
  digitalWrite(ledPin, HIGH);
  delay(300); // ms
  digitalWrite(ledPin, LOW);
}

void setup()
{
  pinMode(ledPin, OUTPUT);

  servoH.attach(servoHPin); // Configura a conexão do Servo Horizontal com o pino;
  servoH.write(servoHAngle);

  servoV.attach(servoVPin);
  servoV.write(servoVAngle);

  Serial.begin(9600); // Inicializa a comunicação serial
}

void loop()
{
  if (Serial.available() > 0)
  {
    char command = Serial.read(); // Lê o comando enviado pelo Python
    
    if (command == 'L')
    {
      servoHAngle = servoHAngle <= rotationItensity + 5 ? servoHAngle : servoHAngle - rotationItensity; // Configurando rotação para esquerda
    }
    else if (command == 'R')
    {
      servoHAngle = servoHAngle >= 180 - rotationItensity - 5 ? servoHAngle : servoHAngle + rotationItensity; // Configurando rotação para direita
    }

    if (command == 'D')
    {
      servoVAngle = servoVAngle <= rotationItensity + 5 ? servoVAngle : servoVAngle - rotationItensity;
    }
    else if (command == 'U')
    {
      servoVAngle = servoVAngle >= 180 - rotationItensity ? servoVAngle : servoVAngle + rotationItensity;
    } 
    
    if (command == '1') {
      blinkLed(ledPin);
    }
  }

  servoH.write(servoHAngle);
  servoV.write(servoVAngle);
}
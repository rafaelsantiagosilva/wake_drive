#include <Servo.h>

Servo servoH; // Servo Horizontal

int ledPin = 13;           // Pino do LED
int buzzerPin = 9;         // Pino do Buzzer
int servoHPin = 10;        // Pino do Servo Horizontal
int servoHAngle = 90;      // Ângulo que o servo horizontal vai girar
int rotationItensity = 25; // Intensidade da rotação

void setup()
{
  pinMode(ledPin, OUTPUT);    // Configura o pino do LED como saída
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
      digitalWrite(ledPin, HIGH); // Acende o LED
      tone(buzzerPin, 1000);      // Liga o Buzzer a uma frequência de 1000Hz
      delay(500);                 // Mantém o LED e o Buzzer ligados por 500ms
      digitalWrite(ledPin, LOW);  // Apaga o LED
      noTone(buzzerPin);          // Desliga o Buzzer
    }
    else if // put your main code here, to run repeatedly:
      if (command == 'U')
      {
        Serial.println(y + 1); // adjusts the servo angle according to the command
        y += 1;                // updates the value of the angle
      }
      else if (command == 'D')
      {
        Serial.println(y - 1);
        y -= 1;
      }
      else
      {
        Serial.println(y);
      }
    if (command == 'L')
    {
      Serial.println(x - 1);
      x -= 1;
    }
    else if (command == 'R')
    {
      Serial.println(x + 1);
      x += 1;
    }
    else
    {
      Serial.println(x);
    }
    command = ""; // clears the variable
  }
}

servoH.write(servoHAngle);
}

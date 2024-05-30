int ledPin = 13; // Pino do LED
int buzzerPin = 9; // Pino do Buzzer

void setup() {
  pinMode(ledPin, OUTPUT); // Configura o pino do LED como saída
  pinMode(buzzerPin, OUTPUT); // Configura o pino do Buzzer como saída
  Serial.begin(9600); // Inicializa a comunicação serial
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read(); // Lê o comando enviado pelo Python
    if (command == '1') {
      digitalWrite(ledPin, HIGH); // Acende o LED
      tone(buzzerPin, 1000); // Liga o Buzzer a uma frequência de 1000Hz
      delay(500); // Mantém o LED e o Buzzer ligados por 500ms
      digitalWrite(ledPin, LOW); // Apaga o LED
      noTone(buzzerPin); // Desliga o Buzzer
    }
  }
}

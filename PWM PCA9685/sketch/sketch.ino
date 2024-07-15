#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// INSTANCIANDO OBJETOS
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// DECLARAÇÃO DE FUNÇÕES
void writeServo(int posicao);
void beginServo();

// VARIÁVEIS GLOBAIS
int posicaoAtual = 90; // Posição inicial do servo

void setup() {
  Serial.begin(9600); // Inicializa a comunicação serial para depuração
  Serial.println("Iniciando...");

  pinMode(12, INPUT_PULLUP); // Botão para mover para a esquerda
  pinMode(13, INPUT_PULLUP); // Botão para mover para a direita

  beginServo(); // INICIA O SERVO
  delay(300);

  // Movendo o servo para posições específicas para testar
  Serial.println("Movendo servo para posição 90");
  writeServo(90);
  delay(1000);
  Serial.println("Movendo servo para posição 180");
  writeServo(180);
  delay(1000);
  Serial.println("Movendo servo para posição 0");
  writeServo(0);
  delay(1000);
}

void loop() {
  // Verifica se o botão do pino 13 foi pressionado
  if (digitalRead(13) == LOW) {
    Serial.println("Botão 13 pressionado");
    posicaoAtual += 10; // Move para a direita
    if (posicaoAtual > 180) posicaoAtual = 180; // Limita a posição máxima a 180 graus
    writeServo(posicaoAtual);
    delay(300); // Debounce delay
  }

  // Verifica se o botão do pino 12 foi pressionado
  if (digitalRead(12) == LOW) {
    Serial.println("Botão 12 pressionado");
    posicaoAtual -= 10; // Move para a esquerda
    if (posicaoAtual < 0) posicaoAtual = 0; // Limita a posição mínima a 0 graus
    writeServo(posicaoAtual);
    delay(300); // Debounce delay
  }
}

// IMPLEMENTO DE FUNÇÕES
void writeServo(int posicao) {
#define SERVOMIN  205 // VALOR PARA UM PULSO MAIOR QUE 1 mS
#define SERVOMAX  409 // VALOR PARA UM PULSO MENOR QUE 2 mS

  int pos = map(posicao, 0, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(7, 0, pos); // O número 0 indica o primeiro canal PWM, que é onde o servo está conectado.
  Serial.print("Servo na posição: ");
  Serial.println(posicao);
}

void beginServo() {
#define Frequencia 50 // VALOR DA FREQUENCIA DO SERVO 

  pwm.begin(); // INICIA O OBJETO PWM
  pwm.setPWMFreq(Frequencia); // DEFINE A FREQUENCIA DE TRABALHO DO SERVO
  Serial.println("Servo iniciado");
}

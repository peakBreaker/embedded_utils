#define ENABLE_PIN 13
int incomingByte = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Initialized the arduino tester for modem");
  pinMode(ENABLE_PIN, OUTPUT);
  digitalWrite(ENABLE_PIN, LOW);
}

static void reset_modem(){
    digitalWrite(ENABLE_PIN, LOW);
    delay(1000);
    digitalWrite(ENABLE_PIN, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
        // read the incoming byte:
        incomingByte = Serial.read();

        // say what you got:
        Serial.print("I received: 0x");
        Serial.println(incomingByte, HEX);
        if (incomingByte == 0x52){
            Serial.println("Resetting devices!");
            reset_modem();
            Serial.println("Done!");
        } else {
            Serial.println("Invalid command.  Send R to reset devices!");  
        }
    }
}

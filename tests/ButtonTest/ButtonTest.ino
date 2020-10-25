// A test for input controls to AudNauseum

#include <SerialFlash.h>
#include <Bounce.h>
#include <Encoder.h>


Encoder selector(25, 26);

Bounce rotaryButton = Bounce(24, 15);
Bounce shiftButton = Bounce(27, 15);
Bounce recButton = Bounce(28, 15);
Bounce playButton = Bounce(29, 15);
Bounce stopButton = Bounce(30, 15);
Bounce metButton = Bounce(31, 15);
Bounce addRemButton = Bounce(32, 15);
Bounce newButton = Bounce(33, 15);
Bounce soloButton = Bounce(34, 15);
Bounce fxButton = Bounce(35, 15);
long selectorPosition = 0;

void setup() {
  
  pinMode(13, OUTPUT); // LED on pin 13
  pinMode(24, INPUT_PULLUP);
  pinMode(27, INPUT_PULLUP);
  pinMode(28, INPUT_PULLUP);
  pinMode(29, INPUT_PULLUP);
  pinMode(30, INPUT_PULLUP);
  pinMode(31, INPUT_PULLUP);
  pinMode(32, INPUT_PULLUP);
  pinMode(33, INPUT_PULLUP);
  pinMode(34, INPUT_PULLUP);  
  pinMode(35, INPUT_PULLUP);  
  delay(1000);
}

elapsedMillis blinkTime;

void loop() {
  
  // blink the LED without delays
  if (blinkTime < 250) {
    digitalWrite(13, LOW);
  } else if (blinkTime < 500) {
    digitalWrite(13, HIGH);
  } else {
    blinkTime = 0; // start blink cycle over again
  }

  // read selector

  long newSelectorPosition = 0;
  newSelectorPosition = selector.read();
  if(newSelectorPosition != selectorPosition){
      selectorPosition = newSelectorPosition;
      Serial.print("SELECTOR VALUE: ");
      Serial.println(selectorPosition);
    } 
  
  
  // read pushbuttons
  
  rotaryButton.update();
  if(rotaryButton.fallingEdge()){
    Serial.println("ROTARY BOOP");
  }
  
  shiftButton.update();
  if (shiftButton.fallingEdge()) {
    Serial.println("SHIFT BOOP");
  }
  playButton.update();
  if (playButton.fallingEdge()) {
    Serial.println("PLAY BOOP");
  }

  recButton.update();
  if(recButton.fallingEdge()){
      Serial.println("REC BOOP");
    }
    
  stopButton.update();
  if(stopButton.fallingEdge()){
      Serial.println("STOP BOOP");
  }

  metButton.update();
  if(metButton.fallingEdge()){
      Serial.println("MET BOOP");
    }

  addRemButton.update();
  if(addRemButton.fallingEdge()){
      Serial.println("ADD/REM BOOP");
    }

  newButton.update();
  if(newButton.fallingEdge()){
      Serial.println("NEW BOOP");
    }

  soloButton.update();
  if(soloButton.fallingEdge()){
      Serial.println("SOLO BOOP");
    }
  fxButton.update();
  if(fxButton.fallingEdge()){
      Serial.println("FX BOOP");
    }

}

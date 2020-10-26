// A test for input controls to AudNauseum


#include <Bounce.h>
#include <Encoder.h>
#include <Audio.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <SerialFlash.h>

// Use these with the Teensy 3.5 & 3.6 SD card
#define SDCARD_CS_PIN    BUILTIN_SDCARD
#define SDCARD_MOSI_PIN  11  // not actually used
#define SDCARD_SCK_PIN   13  // not actually used

// GUItool: begin automatically generated code
AudioInputI2S            i2s1;           //xy=78,48
AudioPlaySdWav           playSdWav2;     //xy=79,214
AudioPlaySdWav           playSdWav1;     //xy=81,159
AudioMixer4              mixer1;         //xy=398,157
AudioOutputI2S           i2s2;           //xy=649,128
AudioConnection          patchCord1(i2s1, 0, mixer1, 2);
AudioConnection          patchCord2(i2s1, 1, mixer1, 3);
AudioConnection          patchCord3(playSdWav2, 0, mixer1, 1);
AudioConnection          patchCord4(playSdWav1, 0, mixer1, 0);
AudioConnection          patchCord5(mixer1, 0, i2s2, 0);
AudioConnection          patchCord6(mixer1, 0, i2s2, 1);
AudioControlSGTL5000     sgtl5000_1;     //xy=421,496
// GUItool: end automatically generated code




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

  Serial.begin(9600);
  AudioMemory(8);
  sgtl5000_1.enable();
  sgtl5000_1.volume(0.9);
  sgtl5000_1.inputSelect(AUDIO_INPUT_LINEIN);
  sgtl5000_1.micGain(36);
  SPI.setMOSI(SDCARD_MOSI_PIN);
  SPI.setSCK(SDCARD_SCK_PIN);
  if (!(SD.begin(SDCARD_CS_PIN))) {
    while (1) {
      Serial.println("Unable to access the SD card");
      delay(500);
    }
  }
  
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
  mixer1.gain(0, 0.25);
  mixer1.gain(1, 0.25);
  mixer1.gain(2, 0.25);
  mixer1.gain(3, 0.25);
  delay(1000);
}

int filenumber = 0; //while file to play
const char * filelist[4] = { "00000003.wav", "00000004.wav"};
  
elapsedMillis blinkTime;

void loop() {

    if (playSdWav1.isPlaying() == false) {
    const char *filename = filelist[0];
    Serial.print("Start playing ");
    Serial.println(filename);
    playSdWav1.play(filename);
    delay(10); // wait for library to parse WAV info
  }

  if(playSdWav2.isPlaying() == false) {
    const char *filename = filelist[1];
    Serial.print("Start playing ");
    Serial.println(filename);
    playSdWav2.play(filename);
    delay(10);
    }
  
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
      playSdWav1.stop();
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

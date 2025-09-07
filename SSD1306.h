#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Frames included from all_frames.h
#include "all_frames.h"

const unsigned char* frames[] = {
  frame_000_bits,
  frame_001_bits,
  frame_002_bits,
  frame_003_bits,
  frame_004_bits,
  frame_005_bits,
  frame_006_bits,
};
const int frameCount = sizeof(frames) / sizeof(frames[0]);

void setup() {
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    for (;;); // Halt if screen not found
  }
  display.clearDisplay();
  display.display();
}

void loop() {
  // Play animation in a loop
  for (int i = 0; i < frameCount; i++) {
    display.clearDisplay();
    display.drawBitmap(0, 0, frames[i], SCREEN_WIDTH, SCREEN_HEIGHT, SSD1306_WHITE);
    display.display();
    delay(200); // slower so you can see it
  }
}

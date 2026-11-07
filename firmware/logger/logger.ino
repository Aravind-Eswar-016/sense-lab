#define PIN        4       // ADC1 channel 3
#define N_AVG      8       // reads summed per sample (1 = no averaging)
#define PERIOD_US  4000    // time between samples: 4000 us = 250 kHz

void setup() {
  Serial.begin(921600);
  analogReadResolution(12);
  analogSetPinAttenuation(PIN, ADC_11db);
}

void loop() {
  static uint32_t next = micros();
  next += PERIOD_US;
  uint32_t sum_raw = 0, sum_mv = 0;
  for (int i = 0; i < N_AVG; i++) {
    sum_raw += analogRead(PIN);               // log sums instead of avg for exact int values and avg is offloaded to py script
    sum_mv += analogReadMilliVolts(PIN);
  }
  Serial.printf("%lu,%lu,%lu\n", (unsigned long)micros(), (unsigned long)sum_raw, (unsigned long)sum_mv);
  while ((int32_t)(micros() - next) < 0) { }   // signed micros(current time) - next(target time) to wait until target time //represents Time remaining
}
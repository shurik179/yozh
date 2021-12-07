#include "motors.h"
#include "pid.h"
#include "regmap.h"

//
int32_t volatile encoderTimestamp[]={0,0};     // time of last encoder update, in micros
int32_t prevEncoder[]={0,0};          // to hold previous values of encoders - for computing speed
int32_t prevEncoderTimestamp[]={0,0}; // time of previous encoder update, in micros
//volatile int8_t   motorDirection[]={1,1}; // motor directions: +1 for forward, -1 for backwards
uint32_t lastUpdate = 0;

//motor speed controllers
PIDcontroller SpeedControllerL, SpeedControllerR, SpeedControllerDiff;

void setupTimers () {
  //setup the clock
  REG_GCLK_GENDIV = GCLK_GENDIV_DIV(3) |          // Divide the 48MHz clock source by divisor 3: 48MHz/3=16MHz
                    GCLK_GENDIV_ID(4);            // Select Generic Clock (GCLK) 4
  while (GCLK->STATUS.bit.SYNCBUSY);              // Wait for synchronization

  REG_GCLK_GENCTRL = GCLK_GENCTRL_IDC |           // Set the duty cycle to 50/50 HIGH/LOW
                   GCLK_GENCTRL_GENEN |         // Enable GCLK4
                   GCLK_GENCTRL_SRC_DFLL48M |   // Set the 48MHz clock source
                   GCLK_GENCTRL_ID(4);          // Select GCLK4
  while (GCLK->STATUS.bit.SYNCBUSY);              // Wait for synchronization
  //feed GCLK4 to TCC0, TCC1
  REG_GCLK_CLKCTRL = GCLK_CLKCTRL_CLKEN |          // Enable GCLK
                       GCLK_CLKCTRL_GEN_GCLK4 |    // Select GCLK4
                       GCLK_CLKCTRL_ID_TCC0_TCC1;  // Feed GCLK4 to TCC0 and TCC1
  while (GCLK->STATUS.bit.SYNCBUSY);              // Wait for synchronization

  REG_GCLK_CLKCTRL = GCLK_CLKCTRL_CLKEN |          // Enable GCLK
                       GCLK_CLKCTRL_GEN_GCLK4 |    // Select GCLK4
                       GCLK_CLKCTRL_ID_TCC2_TC3;  // Feed GCLK4 to TCC2 and TC3
  while (GCLK->STATUS.bit.SYNCBUSY);              // Wait for synchronization


  //configure TCC0 timer for motors
  // Normal (single slope) PWM operation: timers countinuously count up to PER register value and then is reset to 0
  REG_TCC0_WAVE |= TCC_WAVE_WAVEGEN_NPWM;        // Setup single slope PWM on TCC0
  while (TCC0->SYNCBUSY.bit.WAVE);               // Wait for synchronization
  REG_TCC0_PER = 500;                            // period = 501 ticks, so freq is  16Mhz/501 approx 32 Khz
  while(TCC0->SYNCBUSY.bit.PER);
   // Set prescaler and enable the outputs
  REG_TCC0_CTRLA |= TCC_CTRLA_PRESCALER_DIV1 |    // Divide GCLK4 by 1
                        TCC_CTRLA_ENABLE;         // Enable the TCC0 output
  while (TCC0->SYNCBUSY.bit.ENABLE);              // Wait for synchronization

  //configure TCC1 timer for servos
  // Normal (single slope) PWM operation: timers countinuously count up to PER register value and then is reset to 0
 /* REG_TCC1_WAVE |= TCC_WAVE_WAVEGEN_NPWM;        // Setup single slope PWM on TCC1
  while (TCC1->SYNCBUSY.bit.WAVE);               // Wait for synchronization
  REG_TCC1_PER = 19999;                          // period = 20 000 us, so freq is  50 hz
  while(TCC1->SYNCBUSY.bit.PER);*/
  //configure TCC2 timer for servos
  // Normal (single slope) PWM operation: timers countinuously count up to PER register value and then is reset to 0
  REG_TCC2_WAVE |= TCC_WAVE_WAVEGEN_NPWM;        // Setup single slope PWM on TCC2
  while (TCC2->SYNCBUSY.bit.WAVE);               // Wait for synchronization
  REG_TCC2_PER = 19999;                          // period = 20 000 us, so freq is  50 hz
  while(TCC2->SYNCBUSY.bit.PER);


/*
  // Set prescaler and enable the outputs
  REG_TCC1_CTRLA |= TCC_CTRLA_PRESCALER_DIV16 |    // Divide GCLK4 by 16
                        TCC_CTRLA_ENABLE;          // Enable the TCC1 output
  while (TCC1->SYNCBUSY.bit.ENABLE);               // Wait for synchronization
*/
  // Set prescaler and enable the outputs
  REG_TCC2_CTRLA |= TCC_CTRLA_PRESCALER_DIV16 |    // Divide GCLK4 by 16
                        TCC_CTRLA_ENABLE;          // Enable the TCC2 output
  while (TCC2->SYNCBUSY.bit.ENABLE);               // Wait for synchronization

}
void setupMotorPins(){
    pinPeripheral(PIN_SERVO1, PIO_TIMER);
    pinPeripheral(PIN_SERVO2, PIO_TIMER);
    pinPeripheral(PIN_MOTOR1A, PIO_TIMER_ALT);
    pinPeripheral(PIN_MOTOR1B, PIO_TIMER_ALT);
    pinPeripheral(PIN_MOTOR2A, PIO_TIMER_ALT);
    pinPeripheral(PIN_MOTOR2B, PIO_TIMER_ALT);
    pinMode(PIN_ENC1_DIR, INPUT);
    pinMode(PIN_ENC2_DIR, INPUT);
    //attachInterrupt(digitalPinToInterrupt(PIN_ENC1_DIR), ISR_enc1_dir, CHANGE);
    attachInterrupt(digitalPinToInterrupt(PIN_ENC1_SPEED), ISR_enc1_speed, CHANGE);
    //attachInterrupt(digitalPinToInterrupt(PIN_ENC2_DIR), ISR_enc2_dir, CHANGE);
    attachInterrupt(digitalPinToInterrupt(PIN_ENC2_SPEED), ISR_enc2_speed, CHANGE);
}

void resetEncoders(){
    encoder[0]=0;
    encoder[1]=0;
    //also, reset previous value, otherwise speed computation will go haywire
    prevEncoder[0]=0;
    prevEncoder[1]=0;
    lastUpdate = micros();
}


//computes what power to give to motors
//and actually sets motors to this power
// If necessary, also start PID controllers
void setMotors(){
  int16_t powerL=0, powerR=0;
  // determine powers
  if   ((motorPower[0] == 0) && (motorPower[1] == 0) ){
    //stop both motors and disable all PID controllers.
    setMotorsPower(0, 0);
    SpeedControllerL.reset();
    SpeedControllerR.reset();
    SpeedControllerDiff.reset();
    return;
  }
  //in all other cases, carry on
  switch (*motorMode){
    case MOTOR_MODE_POWER:
      powerL=motorPower[0];
      powerR=motorPower[1];
      //Serial.print("Setting motor 1 in MOTOR_MODE_POWER to power "); Serial.println(power1);
      //now, disabl all pid controllers
      SpeedControllerL.reset();
      SpeedControllerR.reset();
      SpeedControllerDiff.reset();
      break;
    /*case MOTOR_MODE_COAST:
      powerL=POWER_COAST;
      powerR=POWER_COAST;
      break;//special value to indicate that it should be floating
      //Serial.println("Setting motor 1 to coast ");
    */
    case MOTOR_MODE_SPEEDPID:
      //set up the PID controllers for left and right motor
      //each of them will take  as input speed (in ticks/s) and outputs a value between -1..1 - it will be later multiplied by MOTOR_MAX_POWER
      float Kp= (*motorKp)*0.0000001; //10^7
      float Ti=(*motorTi)*0.001; //time constant for integral term
      float Td=(*motorTd)*0.001; //time constant for derivative term
      float Ilim = (*motorIlim); //integral limit, in ticks*s
      SpeedControllerL.configure(Kp,Kp/Ti,Kp*Td,Ilim); //Ki=Kp/Ti, Kd=Kp*Td, Ilim = Ti/Kp
      SpeedControllerL.setTarget( (float)motorPower[0]* (*motorMaxspeed)/MOTOR_MAX_POWER); //converting the value on-500...500 scale to ticks/s
      SpeedControllerR.configure(Kp,Kp/Ti,Kp*Td,Ilim);
      SpeedControllerR.setTarget( (float)motorPower[1]* (*motorMaxspeed)/MOTOR_MAX_POWER); //converting the value on-500...500 scale to ticks/s
      //set initial power, as 0th approximation
      powerL=motorPower[0];
      powerR=motorPower[1];
      /*Serial.println((*motorMaxspeed));
      Serial.print("Kp="); Serial.println(Kp,5);
      Serial.print("Ti="); Serial.println(Ti,2);
      Serial.print("Td="); Serial.println(Td,2);
      Serial.print("Ilim="); Serial.println(Ilim,2);
      Serial.print("TargetL="); Serial.println((float)motorPower[0]* (*motorMaxspeed)/MOTOR_MAX_POWER,5);
      Serial.print("TargetR="); Serial.println((float)motorPower[1]* (*motorMaxspeed)/MOTOR_MAX_POWER,5);
      */
      //set the difference speed controller
      if (motorPower[0] == motorPower[1]){
          float KpDiff=0.3*Kp;
          SpeedControllerDiff.configure(KpDiff, KpDiff/Ti,0,200);
          SpeedControllerDiff.setTarget(encoder[0]-encoder[1]); //keep current difference
          Serial.println("Enabling motor sync");
      }
      break;
  }
  //finally, use the found values to set motor powers
  setMotorsPower(powerL, powerR);
}

//setting motors to given power, -500 ... 500 for each motor
//special value of power POWER_COAST is used to indicate float state
void setMotorsPower(int16_t power1, int16_t power2){
  //check if directions should be reversed
  if ((*motorConfig & 0x01) && (power1 != POWER_COAST)) power1=-power1;
  if ((*motorConfig & 0x02) && (power2 != POWER_COAST)) power2=-power2;


  //motor1; controlled by registers REG_TCC0_CCB2, REG_TCC0_CCB3:
  // pin duty pode is REG_TCC0_CCBx/500
  if (power1==POWER_COAST) {
    //motor shoudl be coasted
    REG_TCC0_CCB2=0;
    REG_TCC0_CCB3=0;
  } else  if (power1 >= 0) {
    REG_TCC0_CCB3=MOTOR_MAX_POWER;
    REG_TCC0_CCB2=MOTOR_MAX_POWER-power1;
    //pin A should be always HIGH, pin B duty cycle should be 1- (power/500)
  } else {  //speed<0; pin B high, pin A duty cycle 1 - (|power|/500)=1+(power/500)
    REG_TCC0_CCB3=MOTOR_MAX_POWER+power1;
    REG_TCC0_CCB2=MOTOR_MAX_POWER;
  }
  //motor2; controlled by registers REG_TCC0_CCB0, REG_TCC0_CCB1:
  // pin duty pode is REG_TCC0_CCBx/500
  if (power2==POWER_COAST) {
    REG_TCC0_CCB0=0;
    REG_TCC0_CCB1=0;
  } else if (power2 >= 0) {
    //pin A should be always HIGH, pin B duty cycle should be 1- (power/500)
    REG_TCC0_CCB0=MOTOR_MAX_POWER;
    REG_TCC0_CCB1=MOTOR_MAX_POWER-power2;
  } else {  //speed<0; pin B high, pin A duty cycle 1 - (|power|/500)=1+(power/500)
    REG_TCC0_CCB0=MOTOR_MAX_POWER+power2;
    REG_TCC0_CCB1=MOTOR_MAX_POWER;
  }
  //Serial.print("Motor powers: "); Serial.print( power1); Serial.print(", "); Serial.println(power2);
}

//update computed speed.
//when running in PID mode, also compute and apply PID corrections to the motors
void updateSpeed(){
    uint32_t delta=micros()- lastUpdate;
    if (delta<40000) return; //only run the cycle once every 40 ms, or 25hz
    lastUpdate=micros();
    int32_t count0=encoder[0]; uint32_t timestamp0=encoderTimestamp[0];
    int32_t count1=encoder[1]; uint32_t timestamp1=encoderTimestamp[1];

    speed[0] = ((count0-prevEncoder[0])*1000000.0)/(timestamp0-prevEncoderTimestamp[0]);
    speed[1] = ((count1-prevEncoder[1])*1000000.0)/(timestamp1-prevEncoderTimestamp[1]);
    //Serial.print(count1); Serial.print(" "); Serial.print(prevEncoder[1]); Serial.print(" ");
    //Serial.print(timestamp1-prevEncoderTimestamp[1]); Serial.print(" ");
    //Serial.println(speed[1]);
    prevEncoder[0]=count0; prevEncoderTimestamp[0]=timestamp0;
    prevEncoder[1]=count1; prevEncoderTimestamp[1]=timestamp1;
    //now, deal with PID if necessary
    if (*motorMode == MOTOR_MODE_SPEEDPID) {
      int16_t powerL = motorPower[0] + (int16_t) (MOTOR_MAX_POWER*SpeedControllerL.update((float)speed[0]));
      int16_t powerR = motorPower[1] + (int16_t) (MOTOR_MAX_POWER*SpeedControllerR.update((float)speed[1]));
      //now, compute and apply differential correction
      if (SpeedControllerDiff.is_active()) {
        float difference=encoder[0]-encoder[1];
        int16_t diffCorrection = (int16_t) (MOTOR_MAX_POWER*SpeedControllerDiff.update(difference));
        powerL+=diffCorrection;
        powerR-=diffCorrection;
      }
      //Serial.print(speed[0]);Serial.print("     "); Serial.println(powerL);
      if (powerL>MOTOR_MAX_POWER) powerL=MOTOR_MAX_POWER;
      else if (powerL<-MOTOR_MAX_POWER) powerL=-MOTOR_MAX_POWER;

      if (powerR>MOTOR_MAX_POWER) powerR=MOTOR_MAX_POWER;
      else if (powerR<-MOTOR_MAX_POWER) powerR=-MOTOR_MAX_POWER;

      setMotorsPower(powerL, powerR);

    }
}

//setting servo positions
void setServos(){
  REG_TCC2_CCB1=servoPosition[0]; //servo1
  REG_TCC2_CCB0=servoPosition[1]; //servo2
}

/* ISR for encoders */
void ISR_enc1_speed() {
    bool dir = (REG_PORT_IN0 & PORT_PA15); //read ENC1_DIR pin = PA15
    if (dir) {
       encoder[0]++;
    } else {
       encoder[0]--;
    }
    encoderTimestamp[0]=micros();
}
void ISR_enc2_speed() {
    bool dir = (REG_PORT_IN0 & PORT_PA20); //read ENC2_DIR pin = PA20
    if (dir) {
       encoder[1]++;
    } else {
       encoder[1]--;
    }
    encoderTimestamp[1]=micros();
}

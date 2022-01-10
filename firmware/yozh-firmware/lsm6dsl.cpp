#include "i2c.h"
#include "lsm6dsl.h"
#include "regmap.h"

//variable ofr offsets stored in flash memory


//for keeping track of time
float IMUdeltat = 0.0f;                              // integration time interval
uint32_t IMUlastUpdate=0;
float quat[]={1.0f, 0.0f, 0.0f, 0.0f};              //orientation as a quaternion
int16_t gyroOffset[3];
int16_t accelOffset[3];
uint32_t lastIMUregUpdate=0;

// Reserve a portion of flash memory to store a "offsets_t" data  and
// call it "offsets_flash_storage".
FlashStorage(offsets_flash_storage, offsets_t);



bool IMUisAvailable(){
    uint8_t c = i2cMasterReadByte(LSM6DSL_ADDRESS, LSM6DSL_REG_WHO_AM_I);  // Read WHO_AM_I register for LSM6DSL
    return (bool) (c == LSM6DSL_WHO_AM_I);
}

bool IMUbegin() {

  offsets_t savedOffsets;

  quat[0]=1.0f; quat[1]=0.0f;  quat[2]=0.0f; quat[3]=0.0f;
  if (!IMUisAvailable()) {
    Serial.println("Failed to connect to IMU");
    *imuStatus = IMU_ERROR;
    return false;
  }

  //Initialize
  // set the control register for accelerometer
  i2cMasterWriteByte(LSM6DSL_ADDRESS, LSM6DSL_REG_CTRL1_XL, ACCEL_CTRL1_INIT);
  //same for gyro
  i2cMasterWriteByte(LSM6DSL_ADDRESS, LSM6DSL_REG_CTRL2_G, GYRO_CTRL2_INIT);
  i2cMasterWriteByte(LSM6DSL_ADDRESS, LSM6DSL_REG_CTRL6_C, GYRO_CTRL6_INIT);



  //now, get the offsets from flash memory
  savedOffsets=offsets_flash_storage.read();

  //and copy them to accelOffset, gyroOffset
  for (int i=0; i<3; i++){
      accelOffset[i]=savedOffsets.accel[i];
      gyroOffset[i]=savedOffsets.gyro[i];
  }

  //finishing up
  *imuStatus = IMU_OK;
  Serial.println("IMU inited");
  return true;
}


void readAccelData() {
    uint8_t rawData[6];  // x/y/z accel register data stored here
    i2cMasterReadBytes(LSM6DSL_ADDRESS, LSM6DSL_REG_OUT_XL, 6, &rawData[0]);    // Read the six raw data registers into data array
    accel[0] = (int16_t)((rawData[1] << 8) | rawData[0]) - accelOffset[0];  // Turn the MSB and LSB into a signed 16-bit value
    accel[1] = (int16_t)((rawData[3] << 8) | rawData[2]) - accelOffset[1];
    accel[2] = (int16_t)((rawData[5] << 8) | rawData[4]) - accelOffset[2];
}
void readGyroData() {
    uint8_t rawData[6];  // x/y/z gyro register data stored here
    i2cMasterReadBytes(LSM6DSL_ADDRESS, LSM6DSL_REG_OUT_G, 6, &rawData[0]);  // Read the six raw data registers sequentially into data array
    gyro[0] = (int16_t)((rawData[1] << 8) | rawData[0]) - gyroOffset[0];  // Turn the MSB and LSB into a signed 16-bit value
    gyro[1] = (int16_t)((rawData[3] << 8) | rawData[2]) - gyroOffset[1];
    gyro[2] = (int16_t)((rawData[5] << 8) | rawData[4]) - gyroOffset[2];
}

void IMUcalibrate(){
    uint16_t ii;
    offsets_t savedOffsets;

    int32_t gyro_bias[3] = {0, 0, 0}, accel_bias[3] = {0, 0, 0};
    *imuStatus = IMU_CALIBRATING;
    //Serial.println("Calibrating IMU");
    //zero the offsets
    for (ii=0; ii<3;ii++){
        accelOffset[ii]=0;
        gyroOffset[ii]=0;
    }

    for (ii = 0; ii < 1024; ii++) {
        readAccelData();
        accel_bias[0] += accel[0];
        accel_bias[1] += accel[1];
        accel_bias[2] += accel[2];
        readGyroData();
        gyro_bias[0] += gyro[0];
        gyro_bias[1] += gyro[1];
        gyro_bias[2] += gyro[2];
        delay(20);
    }
    //Serial.println("Data collected");
    accel_bias[0] /= 1024; // Normalize sums to get average count biases
    accel_bias[1] /= 1024;
    accel_bias[2] /= 1024;
    //Serial.print("Accel bias (z): "); Serial.println(accel_bias[2]);
    gyro_bias[0] /= 1024;
    gyro_bias[1] /= 1024;
    gyro_bias[2] /= 1024;
    /*Serial.print("Gyro bias (x): "); Serial.println(gyro_bias[0]);
    Serial.print("Gyro bias (y): "); Serial.println(gyro_bias[1]);
    Serial.print("Gyro bias (z): "); Serial.println(gyro_bias[2]);
    */

    //remove gravity
    if (accel_bias[2] > G/2)  {
        accel_bias[2] -= G; // Remove gravity from the z-axis accelerometer bias calculation
    } else if (accel_bias[2] < -G/2) {
        accel_bias[2] += G; // Remove gravity from the z-axis accelerometer bias calculation
    }


    //save offsets
    for (ii=0; ii<3; ii++){
        accelOffset[ii]=accel_bias[ii];
        gyroOffset[ii]=gyro_bias[ii];
        //and prepare data for saving  to flash memory
        savedOffsets.accel[ii]=accel_bias[ii];
        savedOffsets.gyro[ii]=gyro_bias[ii];
    }
    //save to flash memory
    offsets_flash_storage.write(savedOffsets);
    *imuStatus = IMU_OK;

}

void IMUupdate(){
    uint32_t Now; //timestamp in us
    // If data ready bit set, at least some  registers have new data
    if(i2cMasterReadByte(LSM6DSL_ADDRESS, LSM6DSL_REG_STATUS)) {  // check  data ready interrupt
        readAccelData();  // Read the x/y/z adc values into register map
        readGyroData();  // Read the x/y/z adc values
    }

    Now = micros();
    IMUdeltat = ((Now - IMUlastUpdate) / 1000000.0f); // set integration time by time elapsed since last filter update
    IMUlastUpdate = Now;
    _MadgwickQuaternionUpdate(IMUdeltat);
    if (Now - lastIMUregUpdate> 40000) {
        //more than 40 ms since we last updated output registers
        lastIMUregUpdate = Now;
        for (int i=0; i<4; i++){
            quat_converted[i]=(int32_t) (quat[i]*(1<<30));
        }
        *yaw = (int16_t)(10.0*getYaw());
        *pitch =(int16_t)(10.0*getPitch());
        *roll = (int16_t)(10.0*getRoll());
    }
}

float getYaw() {
  float a;
  a=  - atan2f(2.0f * (quat[1] * quat[2] + quat[0] * quat[3]), quat[0] * quat[0] + quat[1] * quat[1] - quat[2] * quat[2] - quat[3] * quat[3]);
  return (a*radToDeg);
}
float getPitch() {
  float a;
  a = -asinf(2.0f * (quat[1] * quat[3] - quat[0] * quat[2]));
  return (a*radToDeg);
}
float getRoll(){
  float a, a_deg;
  a  = - atan2f(2.0f * (quat[0] * quat[1] + quat[2] * quat[3]), quat[0] * quat[0] - quat[1] * quat[1] - quat[2] * quat[2] + quat[3] * quat[3]);
  a_deg= a*radToDeg+180;
  if (a_deg>180) a_deg-=360;

  return (a_deg);
}

void IMUprint(){
  /* Serial.print("Quat: ");
  Serial.print(quat[0]); Serial.print('\t');
  Serial.print(quat[1]); Serial.print('\t');
  Serial.print(quat[2]); Serial.print('\t');
  Serial.println(quat[3]); */

  Serial.println(" x\t  y\t  z  ");

  Serial.print((int)(1000.0f * accel[0]*aRes)); Serial.print('\t');
  Serial.print((int)(1000.0f * accel[1]*aRes)); Serial.print('\t');
  Serial.print((int)(1000.0f * accel[2]*aRes));
  Serial.println(" mg");

  Serial.print((int)(gyro[0]*gRes)); Serial.print('\t');
  Serial.print((int)(gyro[1]*gRes)); Serial.print('\t');
  Serial.print((int)(gyro[2]*gRes));
  Serial.println(" o/s");

  Serial.print((*yaw)/100.0f); Serial.print('\t');
  Serial.print((*pitch)/100.0f); Serial.print('\t');
  Serial.print((*roll)/100.0f);
  Serial.println(" ypr");
}

__attribute__((optimize("O3"))) void _MadgwickQuaternionUpdate(float deltat) {
  float q1 = quat[0], q2 = quat[1], q3 = quat[2], q4 = quat[3];         // short name local variable for readability
  float norm;                                               // vector norm
  float ax, ay, az, gx, gy, gz;     // accel in g/s; gyro in rad/s
  float f1, f2, f3;                                         // objetive funcyion elements
  float J_11or24, J_12or23, J_13or22, J_14or21, J_32, J_33; // objective function Jacobian elements
  float qDot1, qDot2, qDot3, qDot4;
  float hatDot1, hatDot2, hatDot3, hatDot4;
  float gerrx, gerry, gerrz, gbiasx, gbiasy, gbiasz;        // gyro bias error

  // Auxiliary variables to avoid repeated arithmetic
  float _halfq1 = 0.5f * q1;
  float _halfq2 = 0.5f * q2;
  float _halfq3 = 0.5f * q3;
  float _halfq4 = 0.5f * q4;
  float _2q1 = 2.0f * q1;
  float _2q2 = 2.0f * q2;
  float _2q3 = 2.0f * q3;
  float _2q4 = 2.0f * q4;
  float _2q1q3 = 2.0f * q1 * q3;
  float _2q3q4 = 2.0f * q3 * q4;

  ax = (float)accel[0]*aRes ;  // get actual g value, this depends on scale being set
  ay = (float)accel[1]*aRes ;
  az = (float)accel[2]*aRes ;

  gx = (float)gyro[0]*gResRad ;
  gy = (float)gyro[1]*gResRad ;
  gz = (float)gyro[2]*gResRad ;


  // Normalise accelerometer measurement
  float accnorm = sqrtf(ax * ax + ay * ay + az * az);
  if (accnorm == 0.0f) return; // handle NaN
  accnorm = 1.0f/accnorm;
  /*if (isnan(accnorm)){
    Serial.print("Accnorm is NAN!  acc : ");
    Serial.print(ax*1000); Serial.print('\t');
    Serial.print(ay*1000); Serial.print('\t');
    Serial.println(az*1000);
    Serial.print("Raw values: ");
    Serial.print(accel[0]); Serial.print('\t');
    Serial.print(accel[1]); Serial.print('\t');
    Serial.println(accel[2]);
    Serial.print("Recompute: ");
    ax = (float)accel[0]*aRes ;  // get actual g value, this depends on scale being set
    ay = (float)accel[1]*aRes ;
    az = (float)accel[2]*aRes ;
    Serial.print(ax*1000); Serial.print('\t');
    Serial.print(ay*1000); Serial.print('\t');
    Serial.println(az*1000);
  }*/
  ax *= accnorm;
  ay *= accnorm;
  az *= accnorm;

  // Compute the objective function and Jacobian
  f1 = _2q2 * q4 - _2q1 * q3 - ax;
  f2 = _2q1 * q2 + _2q3 * q4 - ay;
  f3 = 1.0f - _2q2 * q2 - _2q3 * q3 - az;
  J_11or24 = _2q3;
  J_12or23 = _2q4;
  J_13or22 = _2q1;
  J_14or21 = _2q2;
  J_32 = 2.0f * J_14or21;
  J_33 = 2.0f * J_11or24;

  // Compute the gradient (matrix multiplication)
  hatDot1 = J_14or21 * f2 - J_11or24 * f1;
  hatDot2 = J_12or23 * f1 + J_13or22 * f2 - J_32 * f3;
  hatDot3 = J_12or23 * f2 - J_33 *f3 - J_13or22 * f1;
  hatDot4 = J_14or21 * f1 + J_11or24 * f2;

  // Normalize the gradient
  float hatnorm = sqrtf(hatDot1 * hatDot1 + hatDot2 * hatDot2 + hatDot3 * hatDot3 + hatDot4 * hatDot4);

  hatDot1 /= hatnorm;
  hatDot2 /= hatnorm;
  hatDot3 /= hatnorm;
  hatDot4 /= hatnorm;

  // Compute estimated gyroscope biases
  gerrx = _2q1 * hatDot2 - _2q2 * hatDot1 - _2q3 * hatDot4 + _2q4 * hatDot3;
  gerry = _2q1 * hatDot3 + _2q2 * hatDot4 - _2q3 * hatDot1 - _2q4 * hatDot2;
  gerrz = _2q1 * hatDot4 - _2q2 * hatDot3 + _2q3 * hatDot2 - _2q4 * hatDot1;

  // Compute and remove gyroscope biases
  gbiasx += gerrx * deltat * zeta;
  gbiasy += gerry * deltat * zeta;
  gbiasz += gerrz * deltat * zeta;
  gx -= gbiasx;
  gy -= gbiasy;
  gz -= gbiasz;

  // Compute the quaternion derivative
  qDot1 = -_halfq2 * gx - _halfq3 * gy - _halfq4 * gz;
  qDot2 =  _halfq1 * gx + _halfq3 * gz - _halfq4 * gy;
  qDot3 =  _halfq1 * gy - _halfq2 * gz + _halfq4 * gx;
  qDot4 =  _halfq1 * gz + _halfq2 * gy - _halfq3 * gx;

  // Compute then integrate estimated quaternion derivative
  q1 += (qDot1 -(beta * hatDot1)) * deltat;
  q2 += (qDot2 -(beta * hatDot2)) * deltat;
  q3 += (qDot3 -(beta * hatDot3)) * deltat;
  q4 += (qDot4 -(beta * hatDot4)) * deltat;
  /*Serial.print("q1 : ");
  Serial.print(q1); Serial.print('\t');
  Serial.print(q2); Serial.print('\t');
  Serial.print(q3); Serial.print('\t');
  Serial.println(q4);*/
  /*if (isnan(q1)) {
    //stop now
    Serial.println("Not a number!!!");
    Serial.print("hatnorm: "); Serial.println(hatnorm*1000);
    Serial.print("qDot1: "); Serial.println(qDot1);

    Serial.print("hatDot1: "); Serial.println(hatDot1);
    //print all arguments

    Serial.print("acc*1000 : ");
    Serial.print(ax*1000); Serial.print('\t');
    Serial.print(ay*1000); Serial.print('\t');
    Serial.println(az*1000);

    Serial.print("gyro : ");
    Serial.print(gx); Serial.print('\t');
    Serial.print(gy); Serial.print('\t');
    Serial.println(gz);

    Serial.print("q : ");
    Serial.print(quat[0]); Serial.print('\t');
    Serial.print(quat[1]); Serial.print('\t');
    Serial.print(quat[2]); Serial.print('\t');
    Serial.println(quat[3]);

    Serial.print("Deltat: "); Serial.println(deltat*1000);
    while(1);
  } */
  // Normalize the quaternion
  norm = sqrtf(q1 * q1 + q2 * q2 + q3 * q3 + q4 * q4);    // normalise quaternion

  norm = 1.0f/norm;
  quat[0] = q1 * norm;
  quat[1] = q2 * norm;
  quat[2] = q3 * norm;
  quat[3] = q4 * norm;
}

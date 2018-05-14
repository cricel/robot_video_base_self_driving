#ifndef SENSING_H_
#define SENSING_H_

#define SONAR_BUFFER_SIZE   32

extern int lineR; 
extern int lineL;
extern int sonar;
extern int sonar2;

extern volatile long odometerR; 
extern volatile long odometerL; 

extern char sonarBuffer [SONAR_BUFFER_SIZE];


int updateSonar();
int updateSonar2();
void updateLineSensor();
void leftOdometer();
void rightOdometer();

#endif /* SENSING_H_ */

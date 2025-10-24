#include "main.h"

//Intake and Outtake
void setIntake(int intakePower);
void setOuttake(int outtakePower);

//Pneumatics
void setMatchLoader(bool extended); //bool= Boolean= True or false
void setBallBlocker(bool extended);
void setBallBlocker2(bool extended); //this is the lower ball blocker
void toggleMatchLoader();
void toggleBallBlocker();
void toggleBallBlocker2();
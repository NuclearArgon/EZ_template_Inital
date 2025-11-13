#include "main.h"

//Intake and Outtake
void setIntake(int intakePower);
void setOuttake(int outtakePower);
void setOuttakeTop(int power);
void setOuttakeMid(int power);

//Pneumatics
void setMatchLoader(bool extended); //bool= Boolean= True or false
void setBallBlocker(bool extended);
void setBallBlocker2(bool extended); //this is the lower ball blocker
void toggleMatchLoader();
void toggleBallBlocker();
void toggleBallBlocker2();
void setDescore(bool extended);
void toggleDescore();
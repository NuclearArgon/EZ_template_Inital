#include "main.h"

void setIntake(int intakePower){
    intake_motors.move(intakePower);
}

void setOuttake(int outtakePower){
    outtake_motor.move(outtakePower);
}
/* setIntake(127); to turn it on
setIntake(0); to turn it off)*/

void setMatchLoader(bool extended){
    if(extended){
        match_loader.extend(); //true = open/extended
    }
    else{
        match_loader.retract(); //false = closed/retracted
    }
}

void setBallBlocker(bool extended){
    if(extended){
        ball_blocker.extend();
    }
    else{
        ball_blocker.retract();
    }
}

void toggleMatchLoader(){
    match_loader.toggle();
}
void toggleBallBlocker(){
    ball_blocker.toggle();
}
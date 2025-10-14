#include "main.h"

void setIntake(int intakePower){
    intake_motors.move(intakePower);
}

void setOuttake(int outtakePower){
    outtake_motor.move(outtakePower);
}
/* setIntake(127); to turn it on
setIntake(0); to turn it off)*/
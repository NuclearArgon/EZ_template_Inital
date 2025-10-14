#include "main.h"

void setIntake(int intakePower){
    intake_motors.move(intakePower);
}

/* setIntake(127); to turn it on
setIntake(0; to turn it off)*/
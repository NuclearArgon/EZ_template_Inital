#include "main.h"


//intake and outtake
void setIntake(int intakePower){
    intake_motor.move(intakePower);
}




//combined function incase whatever reason ig
void setOuttake(int outtakePower){
    outtake_motor.move(outtakePower);
}
/* setIntake(127); to turn it on
setIntake(0); to turn it off)*/







//pneumatics
//match loader
void setMatchLoader(bool extended){
    if(extended){
        match_loader.extend(); //true = open/extended
    }
    else{
        match_loader.retract(); //false = closed/retracted
    }
}
void toggleMatchLoader(){
    match_loader.toggle();
}

//Mid goal pnematics
void setMidGoal(bool extended){
     if(extended){
        mid_goal.extend(); //true = open/extended
    }
    else{
        mid_goal.retract(); //false = closed/retracted
    }
}
void toggleMidGoal(){
    mid_goal.toggle();
}

// descore mech
void setDescore(bool extended){
    if(extended){
        Descore.extend(); //true = open/extended
    }
    else{
        Descore.retract(); //false = closed/retracted
    }
}

void toggleDescore(){
     Descore.toggle();
    
}
#include "main.h"


//motors
pros::Motor claw_motor(-17,pros::v5::MotorGears::blue); //Claw motor on port 17 - R2 toggle
pros::MotorGroup lift_motors({18, -8}, pros::v5::MotorGears::blue); // Lift motors on ports 18 and 8 synced - L1/L2 control

//Pneumatics
pros::adi::Pneumatics match_loader('B',false); // Match loader mechanism
pros::adi::Pneumatics mid_goal('C',false); // Match loader mechanism
pros::adi::Pneumatics Descore('A',false); // this is the desco
/*Funtions to use for pneumatics
match_loader.extend();
matchloader.retract();
match_loader.toggle();
If I need to know if pistion s..is up or down do
match_loader.is_extend();
*/
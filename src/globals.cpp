#include "main.h"


//motors
pros::Motor intake_motor(-8,pros::v5::MotorGears::blue); //For single intake motor on port 4- R1/R2 control
pros::Motor outtake_motor(9, pros::v5::MotorGears::blue); // Top outtake port 4

//Pneumatics
pros::adi::Pneumatics match_loader('B',false); // Match loader mechanism
pros::adi::Pneumatics mid_goal('C',false); // To stop the balls from coming out the top
pros::adi::Pneumatics Descore('A',false); // this is the desco
/*Funtions to use for pneumatics
match_loader.extend();
matchloader.retract();
match_loader.toggle();
If I need to know if pistion is up or down do
match_loader.is_extend();
*/
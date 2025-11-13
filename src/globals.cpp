#include "main.h"

//motors
pros::Motor intake_motor(5,pros::v5::MotorGears::blue); //For single intake motor on port 4- R1/R2 control
pros::Motor outtake_motor_top(4, pros::v5::MotorGears::blue); // Top outtake port 4
pros::Motor outtake_motor_mid(6,pros::v5::MotorGears::blue); //mid outtake port 6

//Pneumatics
pros::adi::Pneumatics match_loader('A',false); // Match loader mechanism
pros::adi::Pneumatics ball_blocker('B',false); // To stop the balls from coming out the top
pros::adi::Pneumatics ball_blocker2('c',false); // this is to stop the balls from coming out the bottom


/*Funtions to use for pneumatics
match_loader.extend();
matchloader.retract();
match_loader.toggle();
If I need to know if pistion is up or down do
match_loader.is_extend();
*/
#include "main.h"

//motors
pros::MotorGroup intake_motors({5,-6},pros::v5::MotorGears::blue); //For two intake motors on ports (5 and 6)
pros::Motor outtake_motor(4,pros::v5::MotorGears::blue); // For outtake motor on port (4)

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
#include "main.h"

//motors
extern pros::MotorGroup intake_motors; //For two intake motors on ports (5 and 6)
extern pros::Motor outtake_motor; // For outtake motor on port (4)

//Pneumatics
extern pros::adi::Pneumatics match_loader; // Match loader mechanism
extern pros::adi::Pneumatics ball_blocker; // To stop the balls from coming out the top
extern pros::adi::Pneumatics ball_blocker2; //to stop the balls from coming out the middle
#include "main.h"

//motors
extern pros::Motor intake_motor; //For tone intake motor on port 4 R1/R2
extern pros::MotorGroup outtake_motors; // For outtake motors on ports 5 and 6

//Pneumatics
extern pros::adi::Pneumatics match_loader; // Match loader mechanism
extern pros::adi::Pneumatics ball_blocker; // To stop the balls from coming out the top
extern pros::adi::Pneumatics ball_blocker2; //to stop the balls from coming out the middle
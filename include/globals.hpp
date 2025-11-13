#include "main.h"

//motors
extern pros::Motor intake_motor; //For tone intake motor on port 4 R1/R2
extern pros::Motor outtake_motor_top; // For outtake motor port 4
extern pros::Motor outtake_motor_mid; //mid outtake half motor port 6
//Pneumatics
extern pros::adi::Pneumatics match_loader; // Match loader mechanism
extern pros::adi::Pneumatics ball_blocker; // To stop the balls from coming out the top
extern pros::adi::Pneumatics ball_blocker2; //to stop the balls from coming out the middle
extern pros::adi::Pneumatics Descore; //descore mech
#include "main.h"

//motors
extern pros::Motor intake_motor; //For tone intake motor on port 4 R1/R2
extern pros::Motor outtake_motor; // For outtake motor port 4

//Pneumatics
extern pros::adi::Pneumatics match_loader; // Match loader mechanism
extern pros::adi::Pneumatics mid_goal; //to stop the balls from coming out the middle
extern pros::adi::Pneumatics Descore; //descore mech
#include "main.h"

//motors
extern pros::Motor claw_motor; //Claw motor on port 17 R2 toggle
extern pros::MotorGroup lift_motors; // Lift motors on ports 18 and 8 L1/L2

//Pneumatics
extern pros::adi::Pneumatics match_loader; // Match loader mechanism
extern pros::adi::Pneumatics mid_goal; //to stop the balls from coming out the middle
extern pros::adi::Pneumatics Descore; //descore mech


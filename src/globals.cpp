#include "main.h"

//motors
pros::MotorGroup intake_motors({5,-6},pros::v5::MotorGears::blue); //For two intake motors on ports (5 and 6)
pros::Motor outtake_motor(4,pros::v5::MotorGears::blue); // For outtake motor on port (4)
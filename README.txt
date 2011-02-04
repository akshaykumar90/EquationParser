INPUT FILE SPECIFICATIONS

The input file is broadly divided into four sections - one of which is optional - which are discussed below:
1. Variables
2. Constants
3. Objective Function
4. Constraints

VARIABLES
All variables need to be declared before using them in any equation. They have to be declared using the keyword VAR. Multiple declarations can happen on the same line or can be declared all on new lines. Multiple declarations should be comma-separated.

VAR var1, var2
VAR var3

CONSTANTS
All constants need to be declared before using them in any equation. They have to be declared using the keyword CONST. To declare a constant, use the keyword CONST followed by the variable name followed by equal sign and then the value,

CONST c1 = 1.67

Multiple declarations can happen on the same line or on new lines. Multiple declarations have to be comma-separated.

CONST c1 = 2, c2 = 1.67

Variables and constants can be declared in any order but all the constants and variables must be declared before any equation. Also variable and constants names must be unique. Names are case-sensitive. Reserved words cannot be used for variables and constants. For a list of reserved words, see appendix. 

OBJECTIVE FUNCTION
After all the variables and constants have been declared, the objective function must be declared. To define it, start a newline with either MAX or MIN if you want to maximize or minimize the function respectively, followed by the objective function separated by space. The objective function can be any valid mathematical equation using any or none of the variables/constants declared above. Also the equation can use any of the standard functions defined for the program. See the appendix for available functions.

MAX ax1+bx2+cx3-dx4

CONSTRAINTS
After the objective function, the constraints must be defined. There are three types of constraints: <=,>= and =. All three types of constraints can occur in any particular order, no predefined order is forced. The constraints can be any valid mathematical inequality using any or none of the variables/constants declared above. Also the equation can use all the standard functions defined for the program. See the appendix for available functions. But be sure of including only constants - either numeric or defined above - on the R.H.S. of the inequality.

2x-3y+5z<=8
c1x-c2x<=c3
2.2y+7z>=2y //WRONG, only constant values can appear on R.H.S.

APPENDIX

Supported Functions:
[NOTE: Functions names are case-insensitive. Exp(x) = exp(x) = eXp(x)]
exp(x) Return e**x.
log(x) Return the natural logarithm of x (that is, the logarithm to base e).
log10(x) Return the base-10 logarithm of x.
acos(x) Return the arc cosine of x, in radians.
asin(x) Return the arc sine of x, in radians.
atan(x) Return the arc tangent of x, in radians.
cos(x) Return the cosine of x radians.
sin(x) Return the sine of x radians.
tan(x) Return the tangent of x radians.
cosh(x) Return the hyperbolic cosine of x.
sinh(x) Return the hyperbolic sine of x.
tanh(x) Return the hyperbolic tangent of x.

RESERVED WORDS
VAR, CONST, MAX, MIN, exp, log, log10, acos, asin, atan, cos, sin, tan, cosh, sinh, tanh

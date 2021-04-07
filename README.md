# The-Peanuts-Programming-Language

This project is based on the tutorial "Make YOUR OWN Programming Language" on Youtube to create my own programming language called "Peanuts Programming Language" using Python. 

Git Clone this project and load into PyCharm. 

Run "main.py". 

Commands to type in the terminal to test the application:
# BINARY AND UNARY EXPRESSIONS
1 + 2 ^ 3

(3 * 2) % 6

-2

# VARIABLE NAMES
LET a = 5

a - 2

LET b = 0

12 / 0      <- Division by zero error 

# CONDITIONALS:

IF 6 == 6 AND 4 == 4 RETURN 1

IF 6 == 6 AND 4 == 4 RETURN "Snoopy is the bestest friend ever"

# FOR LOOP:
FROM i = 1 TO 9 RETURN i^2

FROM j = 1 TO 10 STEP 2 RETURN i^2

# WHILE LOOP:
LET i = 1
WHILE i < 5 RETURN LET i = i + 1

# FUNCTIONS:

BLOCKHEAD add(a, b) -> a + b
add(3, 4)

BLOCKHEAD sub(a, b) -> a - b
sub(5, 2)

BLOCKHEAD mul(a, b) -> a * b
sub(6, 5)

BLOCKHEAD div(a, b) -> a / b
sub(8, 2)

BLOCKHEAD mod(a, b) -> a % b
sub(4, 2)

# Strings

"Hello " + "World"

LET c = "Hello " + "World"
c * 3

I changed the naming conventions to be more readable and also structures the Python classes in multiple files in order to be organized. 

Problem I'd like to fix is in the Interpreter class there are two classes (Interpreter and Function). The Function uses the Interpreter class therefore putting the Function class as a separate file and importing the module would cause circular import. I'd like to find a better way to structure this and avoid circular import. 

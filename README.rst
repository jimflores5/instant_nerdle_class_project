# Instant Nerdle Project

Many students are/were into the Wordle fad, and one adaptation of this
game is Nerdle. Nerdle works just like Wordle, but instead of letters,
players must arrange numbers and mathematical operators (`+-*/`) to create
a true expression (e.g. 9 - 12/4 = 6).

An adaptation to the adaptation is Instant Nerdle 
(https://instant.nerdlegame.com/). In this case, players know all the
numbers and operators, but not their correct order, and players only get
one attempt to enter the correct equation.

Instant Nerdle is a *great* example of algorithmic thinking! This could
serve as a nice culminating project for your coding class.

If possible, play a round of Instant Nerdle with your students, then
identify the goal of the project - to write a program that solves any
Instant Nerdle puzzle!

Ask your students to brainstorm ideas about what steps their program needs
to take, the order for those steps, how to collect user input, etc.

**Note**: Python has an `eval()` function that can be used to evaluate an
equation entered as a string (e.g. `'2 + 3 * 5'`). However, spend time in
class emphasizing why using `eval()` is a BAD idea, since it severely
compromises the security of the program.

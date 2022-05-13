Instant Nerdle Project
######################

This repository contains two applications: A console app and a Flask
application. The ``main`` branch contains the web app, while the
``console-app`` branch contains the terminal application.

Many students are/were into the Wordle fad, and one adaptation of this
game is Nerdle. Nerdle works just like Wordle, but instead of letters,
players must arrange numbers and mathematical operators (``+-*/``) to create
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

**Note**: Python has an ``eval()`` function that can be used to evaluate an
equation entered as a string (e.g. ``'2 + 3 * 5'``). However, spend time in
class emphasizing why using ``eval()`` is a BAD idea, since it severely
compromises the security of the program.

This repository provides a rough solution for the project. To run the Flask
application, you will need to create a virtual environment, activate it,
and then install Flask.

Flask Setup
-----------

After cloning this repo, use the command line interface to navigate into
the project folder, then enter the following commands. (Be sure to
replace ``environment_name`` with a name of your choice).

*Mac*

::
  python3 -m venv environment_name
  . environment_name/bin/activate
  pip3 install Flask

*Windows (GitBash)*

::
  py -3 -m venv environment_name
  . environment_name/Scripts/activate
  pip install Flask

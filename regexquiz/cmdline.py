#!/usr/bin/env python

__author__ = 'Cam Moore'

import re
import sys
import cmd
import os
from quiz import RegExQuiz

def main():
    quiz = RegExQuiz()

    WELCOME = """RegExQuiz! ICS 215 RegEx quizzer.
Type #question to see the quiz question. Then type in the regular
expression that solves the question. When you hit return the quizzer
will show you lines that match that regex, or nothing if nothing matches.
Type #quit to quit."""

    if len(sys.argv) >= 2:
        if sys.argv[1] != '':
            quiz.load_quiz(sys.argv[1])

    #        if len(sys.argv) == 3:
    #            quiz.load_script(sys.argv[2])
    #    else:
    #        quiz.setup_readline()
    print WELCOME
    print
    if len(sys.argv) == 1 or sys.argv[1] == '':
        print "No quiz loaded."
        print "Load the quiz using '#load_quiz <quiz code>'"
        print

    quiz.setup_readline()
    quiz.run_input_loop()


if __name__ == '__main__':
    main()

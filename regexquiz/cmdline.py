#!/usr/bin/env python

__author__ = 'Cam Moore'

import re
import sys
import cmd
import os
from regexquiz.quiz import RegExQuiz

def main():
    quiz = RegExQuiz()

    WELCOME = """RegExQuiz! ICS 215 RegEx quizzer.
Type #quiz to see the quiz question. Then type in the regular
expression that solves the question. When you hit return the quizzer
will show you lines that match that regex, or nothing if nothing matches.
Hit CTRL-d to quit (CTRL-c on windows)."""

    #    if len(sys.argv) >= 2:
    #        quiz.load_input_file(sys.argv[1])

    #        if len(sys.argv) == 3:
    #            quiz.load_script(sys.argv[2])
    #    else:
    #        quiz.setup_readline()
    print WELCOME
    quiz.run_input_loop()


if __name__ == '__main__':
    main()

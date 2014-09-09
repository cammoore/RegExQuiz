#! /usr/bin/env python
"""RegExQuiz is the class that handles loading ICS 215 regular expression quizzes. It provides a shell they can
evaluate different regular expressions against the quiz data.

RegExQuiz is based upon Zed A. Shaw's regetron http://gitorious.org/regetron.
"""
import datetime
import getpass
import os
import re
import urllib2

__author__ = 'Cam Moore'

CMD_PATTERN = re.compile("^#([a-z_]+)\s*(.*)$")


class RegExQuiz(object):
    """Regular Expression Quiz. Supports getting quizzes from the internet and allowing the student to create a
        retular expression that answers the quiz."""

    def __init__(self):
        """Create a new RegExQuiz instance."""
        self.question = None
        self.quiz_url = None
        self.quiz_code = None
        self.data = None
        self.match_mode = False
        self.answer = None
        self.prompt = "quiz >"
        self.last = None
        self.is_grading = False

    @staticmethod
    def setup_readline():
        """Sets up readline module, if available. readline allows for scrolling back in the shell."""
        try:
            import readline

            import atexit

            histfile = os.path.join(os.path.expanduser("~"), ".regexquiznhist")

            try:
                readline.read_history_file(histfile)
            except IOError:
                pass

            atexit.register(readline.write_history_file, histfile)

            readline.parse_and_bind("TAB: complete")
        except ImportError:
            try:
                import pyreadline as readline
            except ImportError:
                print "No readline support, so no scroll back for you."

    def handle_command(self, command, args):
        if command == "load_quiz":
            self.load_quiz(args)
        elif command == "grade_quiz":
            self.grade_quiz(args)
        elif command == "question":
            self.show_quiz()
        elif command == "show_data":
            self.show_data()
        elif command == "help":
            print "Commands:\n  #load_quiz <quiz code> - loads the given quiz,\n  #question - shows the quiz " \
                  "question,\n  #show_data - shows the data that the question is about,\n  #help - shows the " \
                  "commands,\n  #save - saves the results to a file for submission," \
                  "\n  #quit - exits RegExQuiz"
#        elif command == "data":
#            self.set_data(args)
        elif command == "parse":
            sample = open(args).read()
            return re.compile(sample, re.X)
        elif command == "match":
            self.match_mode = not self.match_mode
            print "Match mode: %s" % (self.match_mode and "match" or "search")
        elif command == "rep":
            self.replace_regex(args)
        elif command == "save":
            self.save_answer()
        elif command == "quit":
            exit(0)
        else:
            print "Invalid command, use #help for a list of commands."

    def load_quiz(self, args):
        """Loads a RegEx quiz with the given code from the ICS 215 web site."""
        self.quiz_code = args
        question_url = "http://cammoore.github.io/ics215f14/morea/020.regular-expressions/experience-quiz-" + \
                       self.quiz_code + ".txt"
        data_url = "http://cammoore.github.io/ics215f14/morea/020.regular-expressions/experience-quiz-" + \
                   self.quiz_code + ".data"
        try:
            response = urllib2.urlopen(question_url)
            self.question = response.read()
            response = urllib2.urlopen(data_url)
            self.data = response.readlines()
            print "Loaded Quiz " + str(args)
            self.show_quiz()
        except urllib2.HTTPError:
            print "Invalid Quiz code (" + str(args) + ")"

    def grade_quiz(self, args):
        """Loads a RegEx quiz from the hard drive with the given code."""
        self.quiz_code = args
        self.is_grading = True
        question_filename = "experience-quiz-" + self.quiz_code + ".txt"
        question_dataname = "experience-quiz-" + self.quiz_code + ".data"
        with open(question_filename, "r") as question_file:
            self.question = question_file.read()
        with open(question_dataname, "r") as question_data:
            self.data = question_data.readlines()
        print "Grading Quiz " + self.quiz_code
        print
        print self.question
        print()
        print self.data

    def print_matches(self, regex):
        """Prints out the data that matches the regular expression."""
        if not self.data:
            print "Quiz data is empty. Use #load_quiz <quiz code> to load a quiz."
            return

        for i, line in enumerate(self.data):
            res = self.test_regex(regex, line)
            if res:
                if res.groups():
                    print "%.4d: %r" % (i, regex.findall(line))
                else:
                    print "%.4d: %s" % (i, line),
        print

    def read_input(self):
        """Reads in a command, regular expression or regular expression in verbose mode."""
        while True:
            try:
                exp = self.read_line(self.prompt)

                command = CMD_PATTERN.match(exp)

                if exp == "":
                    return self.read_verbose()
                if command:
                    result = self.handle_command(*command.groups())
                    if result:
                        return result
                else:
                    if not self.is_grading:
                        self.answer = exp
                        self.save_answer()
                    return re.compile(exp)
            except Exception, e:
                print "ERROR", e

    @staticmethod
    def read_line(prompt=""):
        """Reads a line from the prompt."""
        exp = raw_input(prompt)
        return exp

    def read_verbose(self):
        """Reads multiple line input and creates the Regular Expression."""
        exp = []
        l = self.read_line()

        while l:
            exp.append(l)
            l = self.read_line()

        return re.compile("\n".join(exp), re.X)

    def replace_regex(self, args):
        """Shows the data with the regular expression replacement."""
        bound_char = args[0]
        pattern = args.split(bound_char)
        if len(pattern) != 4:
            print "ERROR, format is: !reg /REGEX/REPLACE/ and / can be any char."
        else:
            reg, rep = pattern[1], pattern[2]
            regex = re.compile(reg)
            self.save_replace(args)
            for i, line in enumerate(self.data):
                if self.test_regex(regex, line):
                    print re.sub(regex, rep, line),

    def run_input_loop(self):
        """Main commandline loop."""
        regex = self.read_input()
        while regex:
            self.print_matches(regex)
            regex = self.read_input()

    def save_answer(self):
        """Saves out the current quiz answer to a file, appending the results to the end of the file."""
        if self.quiz_code:
            f = open(getpass.getuser() + self.quiz_code + ".txt", "a")
            f.write(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
            f.write("\n")
            f.write("{\n")
            f.write("  code: ")
            f.write(self.quiz_code)
            f.write(",\n  answer: ")
            f.write(str(self.answer))
            f.write("\n}\n")
            f.close()
        else:
            print "No quiz loaded. Please run #load_quiz <quiz code>"

    def save_replace(self, replace):
        """Saves out the current replace string, appending the results to the end of the file."""
        if self.quiz_code:
            f = open(getpass.getuser() + self.quiz_code + ".txt", "a")
            f.write(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
            f.write("\n")
            f.write("{\n")
            f.write("  code: ")
            f.write(self.quiz_code)
            f.write(",\n  answer: ")
            f.write(str(replace))
            f.write("\n}\n")
            f.close()
        else:
            print "No quiz loaded. Please run #load_quiz <quiz code>"


    def show_data(self):
        """Shows the quiz data to the student."""
        if self.data and self.data != "":
            print self.data
        else:
            print "No quiz loaded. Please run #load_quiz <quiz code>"

    def show_quiz(self):
        """Shows the quiz question to the student."""
        if self.question and self.question != "":
            print self.question
        else:
            print "No quiz loaded. Please run #load_quiz <quiz code>"

    def test_regex(self, regex, line):
        """Tests the regex against the line of data, depending on match_mode."""
        if self.match_mode:
            return regex.match(line)
        else:
            return regex.search(line)

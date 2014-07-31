
import re
import os

__author__ = 'Cam Moore'

CMD_PATTERN = re.compile("^#([a-z]+)\s*(.*)$")

class RegExQuiz(object):
    """Regular Expression Quiz. Supports getting quizzes from the internet and allowing the student to create a
        retular expression that answers the quiz."""

    def __init__(self):
        """Create a new RegExQuiz instance."""
        self.question = None
        self.quiz_url = None
        self.data = None
        self.match_mode = False
        self.prompt = "quiz >"

    def setup_readline(self):
        try:
            import readline

            import atexit

            histfile = os.path.join(os.path.expanduser("~"), ".regetronhist")

            try:
                readline.read_history_file(histfile)
            except IOError:
                pass

            atexit.register(readline.write_history_file, histfile)

            readline.parse_and_bind("TAB: complete")
        except:
            print "No readline support, so no scroll back for you."

    def read_line(self, prompt=""):
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

    def handle_command(self, command, args):
        if command == "load":
            self.load_input_file(args)
        elif command == "help":
            print "Commands: !load !match !data !rep"
        elif command == "data":
            self.set_data(args)
        elif command == "parse":
            sample = open(args).read()
            return re.compile(sample, re.X)
        elif command == "match":
            self.match_mode = not self.match_mode
            print "Match mode: %s" % (self.match_mode and "match" or "search")
        elif command == "rep":
            self.replace_regex(args)
        else:
            print "Invalid command, only !load and !help is available."

    def read_input(self):
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
                    return re.compile(exp)
            except Exception, e:
                print "ERROR", e

    def run_input_loop(self):
        regex = self.read_input()
        while regex:
            self.print_matches(regex)
            regex = self.read_input()


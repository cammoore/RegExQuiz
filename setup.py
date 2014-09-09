__author__ = 'Cam Moore'

config = {
    'description': 'regexquiz is the simple shell for answering regular expression quizzes for ICS 215',
    'author': 'Cam Moore',
    'author_email': 'cmoore@hawaii.edu',
    'version': '1.1',
    'install_requires': [],
    'packages': ['regexquiz'],
    'name': 'regexquiz'
}

try:
    from setuptools import setup

    config['entry_points'] = {
        'console_scripts' : [
            'regexquiz = regexquiz.cmdline:main'
        ],
        }

except ImportError:
    from distutils.core import setup

    config['scripts'] = ['bin/regexquiz', 'bin/regexquiz.bat']

setup(**config)

EXECUTOR = '/opt/ejudge/bin/ejudge-execute'
COMPILER = '/home/pestryakov/judges/compile/scripts/'
LANGS = {
  1: {
    'name': 'Free Pascal',
    'version': '2.6.2',
    'extension': 'pas',
    'command': 'fpc'
  },
  2: {
    'name': 'GNU C',
    'version': '4.9.0',
    'extension': 'с',
    'command': 'gcc'
  },
  3: {
    'name': 'GNU C++',
    'version': '4.9.0',
    'extension': 'cpp',
    'command': 'g++'
  },
  8: {
    'name': 'Borland Delphi 6',
    'version': '14.5',
    'extension': 'pas',
    'command': 'dcc'
  },
  18: {
    'name': 'Java JDK',
    'version': '1.7.0_45',
    'extension': 'java',
    'command': 'javac'
  },
  22: {
    'name': 'PHP',
    'version': '5.5.7',
    'extension': 'php',
    'command': 'php'
  },
  23: {
    'name': 'Python',
    'version': '2.7.5',
    'extension': 'py',
    'command': 'python'
  },
  24: {
    'name': 'Perl',
    'version': '5.16.3',
    'extension': 'pl',
    'command': 'perl'
  },
  25: {
    'name': 'Mono C#',
    'version': '2.10.8.0',
    'extension': 'cs',
    'command': 'mcs'
  },
  26: {
    'name': 'Ruby',
    'version': '2.0.0p353',
    'extension': 'rb',
    'command': 'ruby'
  },
  27: {
    'name': 'Python',
    'version': '3.3.2',
    'extension': 'py',
    'command': 'python3'
  },
  28: {
    'name': 'Haskell GHC',
    'version': '7.4.2',
    'extension': 'hs',
    'command': 'ghc'
  },
  29: {
    'name': 'Free Basic',
    'version': '0.90.1',
    'extension': 'bas',
    'command': 'fbc'
  },
  30: {
    'name': 'Pascal ABC.NET',
    'version': '1.8.0.513',
    'extension': 'pas',
    'command': 'pasabc-linux'
  },
}
STATUS = ['OK', 'Compiling', 'Running']
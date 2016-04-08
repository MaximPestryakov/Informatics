from subprocess import Popen, PIPE

class Status:
  OK = 0
  Compiling = 1
  Running = 2
  CE = 3
  TL = 4
  RT = 5
  ML = 6
  Queue = 7
  CF = 8

  def __setattr__(self, name, value):
    raise ValueError('assignment of read-only variable \'%s\'' % name)
Status = Status()

def run_process(args):
  proc = Popen(args, stdout=PIPE, stderr=PIPE, shell=True)
  return tuple(val.decode() for val in proc.communicate())

def create_file(file_path, text):
  with open(file_path, 'w') as file:
    file.write(text)

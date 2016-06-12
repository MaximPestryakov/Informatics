from subprocess import Popen, PIPE
import gzip
import os

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
  return tuple(map(lambda s: s.decode(), proc.communicate()))

def create_file(file_path, text):
  with open(file_path, 'w') as file:
    file.write(text)

def serve_path(contest_id):
  return os.path.join('/home/judges/', '{:0>6}'.format(contest_id), 'conf/serve.cfg')

def submit_path(contest_id, submit_id):
  return os.path.join('/home/judges/', '{:0>6}'.format(contest_id), 'var/archive/runs', to32(submit_id // 32 // 32 // 32 % 32), to32(submit_id // 32 // 32 % 32), to32(submit_id // 32 % 32), '{:0>6}'.format(submit_id))

def read_file(path):
  try:
    with open(path, 'r') as file:
      return file.read()
  except FileNotFoundError:
    try:
      with gzip.open(path + '.gz', 'r') as file:
        return file.read().decode()
    except FileNotFoundError:
      pass
  return str()

def to32(num):
  if num < 10:
    return str(num)
  else:
    return chr(ord('A') + num - 10)

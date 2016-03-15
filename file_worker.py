from .config import *
from os import mkdir
from subprocess import Popen, PIPE
import json
import os.path

class Status:
  OK = 0
  Compiling = 1
  Running = 2
  CE = 3

  def __setattr__(self, name, value):
    raise ValueError('assignment of read-only variable \'%s\'' % name)
Status = Status()


def run_process(args):
  proc = Popen(args, stdout=PIPE, stderr=PIPE, shell=True)
  return tuple(val.decode() for val in proc.communicate())

def make_info(solution_id, lang_id, status):
  info = json.dumps({'id': solution_id, 'lang_id': lang_id, 'status': status})
  create_file('{solutions}/{solution_id}/info.json'.format(solutions=SOLUTIONS, solution_id=solution_id), info)

def get_info(solution_id):
  with open('{solutions}/{solution_id}/info.json'.format(solutions=SOLUTIONS, solution_id=solution_id), 'r') as file:
    info = json.load(file)
    info['lang'] = LANGS[info['lang_id']]['name'] + ' ' + LANGS[info['lang_id']]['version']
    info['extension'] = LANGS[info['lang_id']]['extension']
    return info

def create_solution(source_code, test, solution_id, lang_id):
  path = '{solutions}/{solution_id}'.format(solutions=SOLUTIONS, solution_id=solution_id)
  mkdir(path)
  create_file('{path}/main.{extension}'.format(path=path, extension=LANGS[lang_id]['extension']), source_code)
  create_file('{path}/stdin.txt'.format(path=path), test)

def create_file(file_path, text):
  with open(file_path, 'w') as file:
    file.write(text)

def compile_solution(solution_id, lang_id):
  make_info(solution_id, lang_id, Status.Compiling)
  path = '{solutions}/{solution_id}'.format(solutions=SOLUTIONS, solution_id=solution_id)
  command = '{compiler}{command} {path}/main.{extension} {path}/main'.format(compiler=COMPILER, command=LANGS[lang_id]['command'], path=path, extension=LANGS[lang_id]['extension'])
  return run_process(command)

def run_solution(solution_id, lang_id):
  out, err = compile_solution(solution_id, lang_id)
  create_file('{solutions}/{solution_id}/c_stdout.txt'.format(solutions=SOLUTIONS, solution_id=solution_id), out)
  create_file('{solutions}/{solution_id}/c_stderr.txt'.format(solutions=SOLUTIONS, solution_id=solution_id), err)
  make_info(solution_id, lang_id, Status.Running)
  path = '{solutions}/{solution_id}'.format(solutions=SOLUTIONS, solution_id=solution_id)
  if os.path.isfile('{path}/main'.format(path=path)):
    command = '{executor} --time-limit=5 --stdin={path}/stdin.txt --stdout={path}/r_stdout.txt --stderr={path}/r_stderr.txt {path}/main'.format(executor=EXECUTOR, path=path)
    out, err = run_process(command)
    make_info(solution_id, lang_id, Status.OK)
  else:
    make_info(solution_id, lang_id, Status.CE)

def get_last_id():
  command = 'ls {solutions} | grep ^[1-9][0-9]*$ | sort -n | tail -1'.format(solutions=SOLUTIONS)
  out, err = run_process(command)
  try:
    return int(out)
  except ValueError:
    return 0
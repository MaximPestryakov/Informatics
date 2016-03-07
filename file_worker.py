from os import mkdir
from subprocess import Popen, PIPE


EXECUTOR = '/opt/ejudge/bin/ejudge-execute'
COMPILER = '/home/pestryakov/judges/compile/scripts/'
LANGS = ['g++', 'javac', 'python3']

def create_solution(source_code, test, solution_id, lang_id):
  mkdir('solutions/{solution_id}'.format(solution_id=solution_id))
  create_file('solutions/{solution_id}/main.cpp'.format(solution_id=solution_id), source_code)
  create_file('solutions/{solution_id}/input.txt'.format(solution_id=solution_id), test)

def create_file(file_path, text):
  file = open(file_path, 'w')
  file.write(text)
  file.close()

def compile_solution(solution_id, lang_id):
  command = '{compiler}{lang} solutions/{solution_id}/main.cpp solutions/{solution_id}/main'.format(compiler=COMPILER, lang=LANGS[lang_id-1], solution_id=solution_id)
  proc = Popen(command, shell=True)
  out, err = proc.communicate()
  errcode = proc.returncode

def run_solution(solution_id, lang_id):
  compile_solution(solution_id, lang_id)
  command = '{executor} --stdin=solutions/{solution_id}/input.txt --stdout=solutions/{solution_id}/output.txt ./solutions/{solution_id}/main'.format(executor=EXECUTOR, solution_id=solution_id)
  proc = Popen(command, stdout=PIPE, shell=True)
  out, err = proc.communicate()
  errcode = proc.returncode
  #create_file('solutions/{solution_id}/log.txt'.format(solution_id=solution_id), out.decode())

def get_last_id():
  command = 'ls solutions | grep ^[1-9][0-9]*$ | sort -n | tail -1'
  proc = Popen(command, stdout=PIPE, shell=True)
  out, err = proc.communicate()
  errcode = proc.returncode
  if out == b'':
    return 0
  return int(out)
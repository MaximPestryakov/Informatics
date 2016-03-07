from .config import *
from json import dumps, loads
from os import mkdir
from subprocess import getstatusoutput

def make_info(solution_id, lang_id, status, code = 0, output = ''):
  info = dumps({'id': solution_id, 'lang': lang_id, 'status': 0})
  create_file('solutions/{solution_id}/info.json'.format(solution_id=solution_id), info)

def get_info(solution_id):
  file = open('solutions/{solution_id}/info.json'.format(solution_id=solution_id), 'r')
  info = file.read()
  file.close()
  info = loads(info)
  info['lang'] = LANGS[info['lang']]['name'] + ' ' + LANGS[info['lang']]['version']
  return info

def create_solution(source_code, test, solution_id, lang_id):
  mkdir('solutions/{solution_id}'.format(solution_id=solution_id))
  create_file('solutions/{solution_id}/main.{extension}'.format(solution_id=solution_id, extension=LANGS[lang_id]['extension']), source_code)
  create_file('solutions/{solution_id}/input.txt'.format(solution_id=solution_id), test)

def create_file(file_path, text):
  file = open(file_path, 'w')
  file.write(text)
  file.close()

def compile_solution(solution_id, lang_id):
  make_info(solution_id, lang_id, 1)
  command = '{compiler}{command} solutions/{solution_id}/main.{extension} solutions/{solution_id}/main'.format(compiler=COMPILER, command=LANGS[lang_id]['command'], solution_id=solution_id, extension=LANGS[lang_id]['extension'])
  return getstatusoutput(command)

def run_solution(solution_id, lang_id):
  code, output = compile_solution(solution_id, lang_id)
  make_info(solution_id, lang_id, 2, code, output)
  command = '{executor} --time-limit=5 --stdin=solutions/{solution_id}/input.txt --stdout=solutions/{solution_id}/output.txt ./solutions/{solution_id}/main'.format(executor=EXECUTOR, solution_id=solution_id)
  code, output = getstatusoutput(command)
  make_info(solution_id, lang_id, 0, code, output)

def get_last_id():
  command = 'ls solutions | grep ^[1-9][0-9]*$ | sort -n | tail -1'
  code, output = getstatusoutput(command)
  if output.isdecimal():
    return int(output)
  if output != '':
    mkdir('solutions')
  return 0
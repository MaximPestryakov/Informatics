from .config import *
from .file_worker import *
from .redis_connect import redis_db as r
from os import mkdir
import json
import os.path

class Solution:
  def __init__(self,  source_code, test, lang_id, time_limit, memory_limit):
    self.id = r.incr('solution:id')
    self.source_code = source_code
    self.test = test
    self.lang_id = lang_id
    self.time_limit = time_limit
    self.memory_limit = memory_limit
    self.path = '{solutions}/{solution_id}'.format(solutions=SOLUTIONS, solution_id=self.id)
    self.set_status(Status.Queue)
    self.set_lang()
    mkdir(self.path)
    create_file('{path}/main.{extension}'.format(path=self.path, extension=LANGS[self.lang_id]['extension']), self.source_code)
    create_file('{path}/stdin.txt'.format(path=self.path), self.test)

  def compile(self):
    self.set_status(Status.Compiling)
    command = '{compiler}{command} {path}/main.{extension} {path}/main'.format(compiler=COMPILER, command=LANGS[self.lang_id]['command'], path=self.path, extension=LANGS[self.lang_id]['extension'])
    return run_process(command)

  def run(self):
    out, err = self.compile()
    create_file('{path}/c_stdout.txt'.format(path=self.path), out)
    create_file('{path}/c_stderr.txt'.format(path=self.path), err)
    self.set_status(Status.Running)
    if os.path.isfile('{path}/main'.format(path=self.path)):
      command = '{executor} --time-limit={time} --memory-limit --max-vm-size={memory}M --stdin={path}/stdin.txt --stdout={path}/r_stdout.txt --stderr={path}/r_stderr.txt {path}/main'.format(executor=EXECUTOR, path=self.path, time=self.time_limit, memory=self.memory_limit)
      out, err = run_process(command)
      create_file('{path}/log_out.txt'.format(path=self.path), out)
      create_file('{path}/log_err.txt'.format(path=self.path), err)
      self.set_status(Status.OK)
    else:
      self.set_status(Status.CE)

  def set_status(self, status):
    r.set('solution:{id}:status'.format(id=self.id), status)

  def set_lang(self):
    r.set('solution:{id}:lang'.format(id=self.id), self.lang_id)

  @staticmethod
  def get_info(solution_id):
    status = int(r.get('solution:{id}:status'.format(id=solution_id)))
    lang_id = int(r.get('solution:{id}:lang'.format(id=solution_id)))
    info = {'id': solution_id, 'lang_id': lang_id, 'status': status}
    info['lang'] = LANGS[info['lang_id']]['name'] + ' ' + LANGS[info['lang_id']]['version']
    info['extension'] = LANGS[info['lang_id']]['extension']
    return info
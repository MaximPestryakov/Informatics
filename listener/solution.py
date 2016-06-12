from config import *
from file_worker import *
from os import mkdir
from redis_connect import redis
import os.path

class Solution:
  def __init__(self, id):
    self.id = id
    self.lang_id = int(redis.get('solution:{id}:lang'.format(id=id)))
    self.cpu_time_limit = int(redis.get('solution:{id}:cpu-tl'.format(id=id)))
    self.real_time_limit = int(redis.get('solution:{id}:real-tl'.format(id=id)))
    self.memory_limit = int(redis.get('solution:{id}:memory'.format(id=id)))
    self.path = '{solutions}/{solution_id}'.format(solutions=SOLUTIONS, solution_id=id)
    mkdir(self.path)

    source_code = redis.get('solution:{id}:source'.format(id=id)).decode()
    test = redis.get('solution:{id}:test'.format(id=id)).decode()

    create_file('{path}/main.{extension}'.format(path=self.path, extension=LANGS[self.lang_id]['extension']), source_code)
    create_file('{path}/stdin.txt'.format(path=self.path), test)

  def compile(self):
    self.set_status(Status.Compiling)
    command = '{compiler}{command} {path}/main.{extension} {path}/main'.format(compiler=COMPILER, command=LANGS[self.lang_id]['command'], path=self.path, extension=LANGS[self.lang_id]['extension'])
    return run_process(command)

  def run(self):
    out, err = self.compile()
    create_file('{path}/c_stdout.txt'.format(path=self.path), out)
    create_file('{path}/c_stderr.txt'.format(path=self.path), err)
    redis.set('solution:{id}:c_stdout'.format(id=self.id), out)
    redis.set('solution:{id}:c_stderr'.format(id=self.id), err)
    self.set_status(Status.Running)
    if os.path.isfile('{path}/main'.format(path=self.path)):
      command = '{executor} --time-limit={cpu_time} --real-time-limit={real_time} --memory-limit --max-vm-size={memory}M --stdin={path}/stdin.txt --stdout={path}/r_stdout.txt --stderr={path}/r_stderr.txt {path}/main'.format(executor=EXECUTOR, path=self.path, cpu_time=self.cpu_time_limit, real_time=self.real_time_limit, memory=self.memory_limit)
      out, err = run_process(command)
      redis.set('solution:{id}:r_stdout'.format(id=self.id), read_file('{path}/r_stdout.txt'.format(path=self.path)))
      redis.set('solution:{id}:r_stderr'.format(id=self.id), read_file('{path}/r_stderr.txt'.format(path=self.path)))

      create_file('{path}/log_out.txt'.format(path=self.path), out)
      create_file('{path}/log_err.txt'.format(path=self.path), err)
      self.make_info(err)
    else:
      self.set_status(Status.CE)

  def make_info(self, log):
    for key, value in [line.split(':') for line in log.split('\n') if line.count(':') == 1]:
      key = key.strip().lower()
      value = value.strip()
      if key == 'status':
        value = {'OK': 0, 'CE': 3, 'TL': 4, 'RT': 5, 'ML': 6, 'CF': 8}[value]
      if key in ('status', 'cputime', 'realtime', 'vmsize'):
        redis.set('solution:{id}:{key}'.format(id=self.id, key=key), value)

  def set_status(self, status):
    redis.set('solution:{id}:status'.format(id=self.id), status)

  @staticmethod
  def create(params):
    lang = params.get('lang', '1')
    cpu_time_limit = params.get('cpu_time_limit', '10')
    real_time_limit = params.get('real_time_limit', '10')
    memory_limit = params.get('memory_limit', '512')
    source_code = params.get('source_code', '')
    test = params.get('test', '')

    if not lang.isdigit() or not cpu_time_limit.isdigit() or not real_time_limit.isdigit() or not memory_limit.isdigit():
      raise TypeError

    lang = int(lang)
    cpu_time_limit = int(cpu_time_limit)
    real_time_limit = int(real_time_limit)
    memory_limit = int(memory_limit)

    if not LANGS.get(lang) or 1 > cpu_time_limit < 10 or 1 > real_time_limit < 10 or 1 > memory_limit < 512:
      raise ValueError

    id = params.get('id') or redis.incr('solution:id')
    redis.set('solution:{id}:lang'.format(id=id), lang)
    redis.set('solution:{id}:cpu-tl'.format(id=id), cpu_time_limit)
    redis.set('solution:{id}:real-tl'.format(id=id), real_time_limit)
    redis.set('solution:{id}:memory'.format(id=id), memory_limit)
    redis.set('solution:{id}:status'.format(id=id), Status.Queue)
    redis.set('solution:{id}:source'.format(id=id), source_code)
    redis.set('solution:{id}:test'.format(id=id), test)
    return id

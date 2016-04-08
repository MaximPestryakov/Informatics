from os import mkdir
import os.path

if __name__ == 'solution':
  from config import *
  from file_worker import *
  from redis_connect import redis
else:
  from .config import *
  from .file_worker import *
  from .redis_connect import redis

class Solution:
  def __init__(self, id):
    self.id = id
    self.lang_id = int(redis.get('solution:{id}:lang'.format(id=id)))
    self.cpu_time_limit = int(redis.get('solution:{id}:cpu-tl'.format(id=id)))
    self.real_time_limit = int(redis.get('solution:{id}:real-tl'.format(id=id)))
    self.memory_limit = int(redis.get('solution:{id}:memory'.format(id=id)))
    self.path = '{solutions}/{solution_id}'.format(solutions=SOLUTIONS, solution_id=id)

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
      command = '{executor} --time-limit={cpu_time} --real-time-limit={real_time} --memory-limit --max-vm-size={memory}M --stdin={path}/stdin.txt --stdout={path}/r_stdout.txt --stderr={path}/r_stderr.txt {path}/main'.format(executor=EXECUTOR, path=self.path, cpu_time=self.cpu_time_limit, real_time=self.real_time_limit, memory=self.memory_limit)
      out, err = run_process(command)
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
  def get_info(solution_id):
    class Info:
      pass
    info = Info()
    info.id = solution_id
    info.status = int(redis.get('solution:{id}:status'.format(id=solution_id)))
    info.lang_id = int(redis.get('solution:{id}:lang'.format(id=solution_id)))
    info.cpu_time_limit = int(redis.get('solution:{id}:cpu-tl'.format(id=solution_id)))
    info.real_time_limit = int(redis.get('solution:{id}:real-tl'.format(id=solution_id)))
    info.memory_limit = int(redis.get('solution:{id}:memory'.format(id=solution_id)))
    info.cputime = int(redis.get('solution:{id}:cputime'.format(id=solution_id)) or 0)
    info.realtime = int(redis.get('solution:{id}:realtime'.format(id=solution_id)) or 0)
    info.vmsize = int(redis.get('solution:{id}:vmsize'.format(id=solution_id)) or 0)
    info.lang = LANGS[info.lang_id]['name'] + ' ' + LANGS[info.lang_id]['version']
    info.extension = LANGS[info.lang_id]['extension']
    return info

  @staticmethod
  def create(params):
    if not params['lang'].isdigit() or not params['cpu_time_limit'].isdigit() or not params['real_time_limit'].isdigit() or not params['memory_limit'].isdigit():
      raise TypeError

    lang = int(params.get('lang', 1))
    cpu_time_limit = int(params.get('cpu_time_limit', 10))
    real_time_limit = int(params.get('real_time_limit', 10))
    memory_limit = int(params.get('memory_limit', 512))

    if not LANGS.get(lang) or 1 > cpu_time_limit < 10 or 1 > real_time_limit < 10 or 1 > memory_limit < 512:
      raise ValueError

    id = redis.incr('solution:id')
    redis.set('solution:{id}:lang'.format(id=id), lang)
    redis.set('solution:{id}:cpu-tl'.format(id=id), cpu_time_limit)
    redis.set('solution:{id}:real-tl'.format(id=id), real_time_limit)
    redis.set('solution:{id}:memory'.format(id=id), memory_limit)
    redis.set('solution:{id}:status'.format(id=id), Status.Queue)
    path = '{solutions}/{id}'.format(solutions=SOLUTIONS, id=id)
    mkdir(path)
    create_file('{path}/main.{extension}'.format(path=path, extension=LANGS[lang]['extension']), params.get('source_code', ''))
    create_file('{path}/stdin.txt'.format(path=path), params.get('test', ''))
    return id

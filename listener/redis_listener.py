from config import *
from file_worker import read_file, submit_path, serve_path
from redis_connect import redis
from socket import gethostname
from solution import Solution
from threading import Thread
from utils.configparser import ConfigParser


class Listener(Thread):
  def __init__(self, redis, channels, name):
    Thread.__init__(self)
    self.redis = redis
    self.pubsub = self.redis.pubsub()
    self.pubsub.subscribe(channels)
    self.name = name

  def solution(self, solution_id):
    if not solution_id:
      return
    solution = Solution(solution_id)
    thread = Thread(target=solution.run)
    thread.daemon = True
    thread.start()
    self.redis.lpop(self.name + ':solution:queue')

  def hack(self, hack_id):
    if not hack_id:
      return
    contest_id = int(redis.get('hack:{id}:contest'.format(id=hack_id)))
    submit_id = int(redis.get('hack:{id}:submit'.format(id=hack_id)))
    solution_id = int(redis.get('hack:{id}:solution'.format(id=hack_id)))
    problem_id = int(redis.get('hack:{id}:problem'.format(id=hack_id)))
    hacking_test = redis.get('hack:{id}:test'.format(id=hack_id)).decode()
    lang = redis.get('hack:{id}:lang'.format(id=hack_id)).decode()
    path = submit_path(contest_id, submit_id)
    source_code = read_file(path)

    config = ConfigParser(allow_no_value = True, strict = False, interpolation = None)
    config.read(serve_path(contest_id))
    config = config._sections
    if config['problem'][0].get('time_limit'):
      cpu_time_limit = config['problem'][0].get('time_limit')[0]
    else:
      cpu_time_limit = '10'
    if config['problem'][0].get('real_time_limit'):
      real_time_limit = config['problem'][0].get('real_time_limit')[0]
    else:
      real_time_limit = '10'
    if config['problem'][0].get('max_vm_size'):
      memory_limit = config['problem'][0].get('max_vm_size')[0]
    else:
      memory_limit = '512'

    for problem in config['problem']:
      if problem.get('id') and int(problem.get('id')[0]) == problem_id:
        if problem.get('time_limit'):
          cpu_time_limit = problem.get('time_limit')[0] or cpu_time_limit
        if problem.get('real_time_limit'):
          real_time_limit = problem.get('real_time_limit')[0] or real_time_limit
        if problem.get('max_vm_size'):
          memory_limit = problem.get('max_vm_size')[0] or memory_limit
    if memory_limit[-1] == 'M':
      memory_limit = memory_limit[:-1]
    params = {
      'id': solution_id,
      'source_code': source_code,
      'test': hacking_test,
      'lang': lang,
      'cpu_time_limit': cpu_time_limit,
      'real_time_limit': real_time_limit,
      'memory_limit': memory_limit
    }
    try:
      Solution.create(params)
    except TypeError:
      return
    except ValueError:
      return
    redis.rpush('solution:queue', solution_id)
    redis.publish('run_solution', 'new_solution')
    self.redis.lpop(self.name + ':hack:queue')

  def run(self):
    while redis.llen(self.name + ':solution:queue'):
      solution_id = int(self.redis.lrange(self.name + ':solution:queue', 0, 0)[0] or 0)
      self.solution(solution_id)

    while redis.llen(self.name + ':hack:queue'):
      hack_id = int(self.redis.lrange(self.name + ':hack:queue', 0, 0)[0] or 0)
      self.hack(hack_id)

    for item in self.pubsub.listen():
      channel = item['channel'].decode()

      if channel == 'run_solution':
        while self.redis.llen('solution:queue'):
          solution_id = int(self.redis.rpoplpush('solution:queue', self.name + ':solution:queue') or 0)
          self.solution(solution_id)

      elif channel == 'hack_solution':
        while self.redis.llen('hack:queue'):
          hack_id = int(self.redis.rpoplpush('hack:queue', self.name + ':hack:queue') or 0)
          self.hack(hack_id)

if __name__ == '__main__':
  client = Listener(redis, ['run_solution', 'hack_solution'], gethostname())
  client.start()

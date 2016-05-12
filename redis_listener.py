from file_worker import read_file, submit_path
from redis_connect import redis
from solution import Solution
from threading import Thread
from config import *

class Listener(Thread):
  def __init__(self, redis, channels):
    Thread.__init__(self)
    self.redis = redis
    self.pubsub = self.redis.pubsub()
    self.pubsub.subscribe(channels)

  def run(self):
    for item in self.pubsub.listen():
      channel = item['channel'].decode()

      if channel == 'run_solution':
        while redis.llen('solution:queue'):
          solution_id = int(self.redis.lpop('solution:queue') or 0)
          if solution_id == 0:
            break
          solution = Solution(solution_id)
          thread = Thread(target=solution.run)
          thread.daemon = True
          thread.start()

      elif channel == 'hack_solution':
        while redis.llen('hack:queue'):
          hack_id = int(self.redis.lpop('hack:queue') or 0)
          if hack_id == 0:
            break
          contest_id = int(redis.get('hack:{id}:contest'.format(id=hack_id)))
          submit_id = int(redis.get('hack:{id}:submit'.format(id=hack_id)))
          solution_id = int(redis.get('hack:{id}:solution'.format(id=hack_id)))
          hacking_test = redis.get('hack:{id}:test'.format(id=hack_id)).decode()
          lang = redis.get('hack:{id}:lang'.format(id=hack_id)).decode()
          path = submit_path(contest_id, submit_id)
          source_code = read_file(path)
          params = {
            'id': solution_id,
            'source_code': source_code,
            'test': hacking_test,
            'lang': lang
          }
          try:
            Solution.create(params)
          except TypeError:
            break
          except ValueError:
            break

          redis.rpush('solution:queue', solution_id)
          redis.publish('run_solution', 'new_solution')



if __name__ == '__main__':
  client = Listener(redis, ['run_solution', 'hack_solution'])
  client.start()

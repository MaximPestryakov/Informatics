from redis_connect import redis
from solution import Solution
from threading import Thread

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

if __name__ == '__main__':
  client = Listener(redis, ['run_solution'])
  client.start()

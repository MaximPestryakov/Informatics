from redis import Redis
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
      data = item['data']

      if channel == 'run_solution':
        solution_id = int(data)
        if solution_id != 1:
          solution = Solution(solution_id)
          thread = Thread(target=solution.run)
          thread.daemon = True
          thread.start()

if __name__ == '__main__':
  redis = Redis()
  client = Listener(redis, ['run_solution'])
  client.start()

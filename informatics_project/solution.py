from .config import *
from .redis_connect import redis

def get_info(solution_id):
  info = {
    'id': solution_id,
    'status': int(redis.get('solution:{id}:status'.format(id=solution_id))),
    'lang_id': int(redis.get('solution:{id}:lang'.format(id=solution_id))),
    'cpu_time_limit': int(redis.get('solution:{id}:cpu-tl'.format(id=solution_id)) or 0),
    'real_time_limit': int(redis.get('solution:{id}:real-tl'.format(id=solution_id)) or 0),
    'memory_limit': int(redis.get('solution:{id}:memory'.format(id=solution_id)) or 0),
    'cputime': int(redis.get('solution:{id}:cputime'.format(id=solution_id)) or 0),
    'realtime': int(redis.get('solution:{id}:realtime'.format(id=solution_id)) or 0),
    'vmsize': int(redis.get('solution:{id}:vmsize'.format(id=solution_id)) or 0)
  }
  info['lang'] = LANGS[info['lang_id']]['name'] + ' ' + LANGS[info['lang_id']]['version']
  info['extension'] = LANGS[info['lang_id']]['extension']
  return info

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

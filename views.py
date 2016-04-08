from .config import *
from .file_worker import *
from .redis_connect import redis
from .solution import Solution
from os.path import isfile
from pyramid.response import FileResponse, Response
from pyramid.view import view_config


@view_config(route_name='home')
def my_view(request):
  return FileResponse('static/index.html', request=request)

@view_config(route_name='send-code')
def send_code(request):

  try:
    solution_id = Solution.create(request.params)
  except TypeError:
    return Response(json_body={'code': 1})
  except ValueError:
    return Response(json_body={'code': 2})

  redis.rpush('solution:queue', solution_id)
  redis.publish('run_solution', 'new_solution')

  if 'solutions' not in request.session:
    request.session['solutions'] = list()
  request.session['solutions'].append(solution_id)
  return Response(json_body={'code': 0})

@view_config(route_name='get-solutions')
def get_solutions(request):
  session = request.session
  if 'solutions' not in session:
    return Response()
  resp = [Solution.get_info(id).__dict__ for id in session['solutions']]
  return Response(json_body=resp)

@view_config(route_name='get-solution')
def get_solution(request):
  session = request.session
  if 'solutions' not in session:
    return Response('No session')
  id = int(request.matchdict['id'])
  file = request.matchdict['file']
  if id in session['solutions']:
    info = Solution.get_info(id)
    if file in ('stdin.txt', 'r_stdout.txt', 'r_stderr.txt', 'c_stdout.txt', 'c_stderr.txt', 'main.%s' % info.extension):
      if isfile('solutions/%d/%s' % (id, file)):
        return FileResponse('solutions/%d/%s' % (id, file), content_type='text/plain')
      return Response('File doesn\'t exists')
    return Response('Invalid file')
  return Response('No id in session')

@view_config(route_name='get-langs')
def get_langs(request):
  langs = list()
  for lang_id, lang in LANGS.items():
    langs.append({'id': lang_id, 'name': lang['name'], 'version': lang['version']})
  return Response(json_body=langs)

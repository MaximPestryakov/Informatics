from .file_worker import *
from os.path import isfile
from pyramid.response import FileResponse, Response
from pyramid.view import view_config
from threading import Thread

@view_config(route_name='home')
def my_view(request):
  return FileResponse('static/index.html', request=request)

@view_config(route_name='get-session')
def get_session(request):
  session = request.session
  return Response(json_body=session)

@view_config(route_name='send-code')
def send_code(request):
  session = request.session
  solution_id = get_last_id() + 1
  create_solution(request.params['source_code'], request.params['test'], solution_id, int(request.params['lang']))
  thread = Thread(target=run_solution, args=(solution_id, int(request.params['lang'])))
  thread.daemon = True
  thread.start()
  if 'solutions' not in session:
    session['solutions'] = list()
  session['solutions'].append(solution_id)
  return Response()

@view_config(route_name='get-solutions')
def get_solutions(request):
  session = request.session
  if 'solutions' not in session:
    return Response()
  resp = list()
  for solution_id in session['solutions']:
    resp.append(get_info(solution_id))
  return Response(json_body=resp)

@view_config(route_name='get-solution')
def get_solution(request):
  session = request.session
  if 'solutions' not in session:
    return Response('No session')
  id = int(request.matchdict['id'])
  file = request.matchdict['file']
  if id in session['solutions']:
    if file in ('input.txt', 'output.txt', 'main.cpp', 'log.txt'):
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
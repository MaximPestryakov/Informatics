from file_worker import *
from os.path import isfile
from pyramid.response import FileResponse, Response
from pyramid.view import view_config
from threading import Thread


def index(request):
  return FileResponse('index.html')

def get_session(request):
  session = request.session
  return Response(json_body=session)

def send_code(request):
  session = request.session
  solution_id = get_last_id() + 1
  create_solution(request.params['source_code'], request.params['test'], solution_id, request.params['lang'])
  '''thread = Thread(target=run_solution, args=(solution_id, request.params['lang']))
  thread.daemon = True
  thread.start()'''
  if 'solutions' not in session:
    session['solutions'] = list()
  session['solutions'].append(solution_id)
  return Response()

def get_solutions(request):
  session = request.session
  if 'solutions' not in session:
    return Response()
  resp = list()
  for sol in session['solutions']:
    resp.append({'id': sol, 'lang': 1, 'status': 1})
  return Response(json_body=resp)

def get_solution(request):
  session = request.session
  if 'solutions' not in session:
    return Response('No session')
  type = request.params['type']
  id = int(request.params['id'])
  if id in session['solutions']:
    if type == 'input':
      file = 'input.txt'
    elif type == 'output':
      file = 'output.txt'
    elif type == 'source':
      file = 'main.cpp'
    else:
      return Response('Invalid type')
    if isfile('solutions/%d/%s' % (id, file)):
      return FileResponse('solutions/%d/%s' % (id, file))
    return Response('File doesn\'t exists')
  return Response('No id in session')
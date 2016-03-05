from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from views import *
from wsgiref.simple_server import make_server

def main():
  session = SignedCookieSessionFactory(secret='mktmDndvkVMjXOGMOETLhxyFExJOdW', max_age=60*60*24*365*50)
  config = Configurator(session_factory=session)
  config.include('pyramid_chameleon')
  config.add_route('index', '/')
  config.add_view(index, route_name='index', request_method='GET')

  config.add_route('send-code', '/send-code')
  config.add_view(send_code, route_name='send-code', request_method='POST')

  config.add_route('get-solutions', '/get-solutions')
  config.add_view(get_solutions, route_name='get-solutions', request_method='GET')

  config.add_route('get-solution', '/get-solution')
  config.add_view(get_solution, route_name='get-solution', request_method='GET')

  config.add_route('get-session', '/get-session')
  config.add_view(get_session, route_name='get-session', request_method='GET')

  config.add_static_view(name='static', path='static')
  return config.make_wsgi_app()

if __name__ == '__main__':
  app = main()
  server = make_server('0.0.0.0', 80, app)
  server.serve_forever()
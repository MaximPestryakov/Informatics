from .config import *
from os import mkdir
from os.path import isdir
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

def main(global_config, **settings):
  if not isdir(SOLUTIONS):
    mkdir(SOLUTIONS)

  session = SignedCookieSessionFactory(secret='mktmDndvkVMjXOGMOETLhxyFExJOdW', max_age=60*60*24*365*50)
  config = Configurator(settings=settings, session_factory=session)

  config.add_static_view('static', 'static')
  config.add_static_view('solutions', 'solutions')

  config.add_route('get-session', '/get-session')
  config.add_route('get-solution', '/get-solution/{id}/{file}')
  config.add_route('get-solutions', '/get-solutions')
  config.add_route('get-langs', '/get-langs')
  config.add_route('home', '/')
  config.add_route('send-code', '/send-code')

  config.scan()
  return config.make_wsgi_app()
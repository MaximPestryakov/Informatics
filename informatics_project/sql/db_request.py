from .db_connect import db

def get_run_by(contest_id, run_id):
  request = 'SELECT prob_id, lang_id FROM runs WHERE contest_id={0} AND run_id={1}'.format(contest_id, run_id)
  db.execute(request)
  result = db.fetchall()
  if len(result):
    return result[0]
  raise ValueError


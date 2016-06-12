import oursql

config = {
  'host': 'informatics.mccme.ru',
  'user': 'py',
  'passwd': '729htw300',
  'db': 'ejudge'  
}

db_connection = oursql.connect(**config)
db = db_connection.cursor()

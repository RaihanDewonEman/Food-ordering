
import psycopg2

###---------------------	Connection with database	------------------------
def database_connection():
	connection = None
	try:
		connection = psycopg2.connect(database='postgres', user='postgres', password='password', host='127.0.0.1', port= '5432')
		print('Database connected!')
		return connection
	except:
    		print('Database is not connected!')
    		
    		
###----------------------   Connection with database using database name	-----------------------------
def database_connection2(dbname):
	connection = None
	try:
		connection = psycopg2.connect(database=dbname, user='postgres', password='password', host='127.0.0.1', port= '5432')
		print(f'{dbname} database connected!')
		return connection
	except:
    		print('Database is not connected!')

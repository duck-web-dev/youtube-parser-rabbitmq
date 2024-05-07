import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class DatabaseCore:
	def __init__(self, db_string: str):
		# self.dbname = dbname
		# self.user = user
		# self.password = password
		# self.host = host
		# self.port = port
		self.db_string = db_string
		self.connection = self.connect()
		self.create_tables()

	def connect(self):
		try:
			connection = psycopg2.connect(
				self.db_string
			)
			connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
			return connection
		except Exception as e:
			raise RuntimeError('Error connecting to database:', e)
		
	def cursor(self):
		return self.connection.cursor()

	def create_tables(self):
		cursor = self.cursor()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS videos (	
				video_id VARCHAR(11) PRIMARY KEY,
				channel_username TEXT,
				video_href TEXT
			);
		""")
		cursor.close()

	def close(self):
		self.connection.close()

	def __del__(self):
			self.close()
from typing import Any
from .core import DatabaseCore



class Database(DatabaseCore):
	#region Basic methods for querying 
	def _query(self, sql: str, vars: tuple | None, need_res = False):
		c = self.cursor()
		c.execute(sql, vars)
		if need_res:
			res = (c.lastrowid, c.fetchall())
		c.close()
		if need_res:
			return res
	
	def query(self, sql: str, vars: tuple = ()) -> None:
		self._query(sql, vars, False)

	def query_and_fetchall(self, sql: str, vars: tuple = ()) -> list[tuple[Any, ...]]:
		return self._query(sql, vars, True)[1]

	def query_and_fetchone(self, sql: str, vars: tuple = ()) -> tuple[Any, ...]:
		x = self._query(sql, vars, True)[1]
		if len(x):
			return x[0]
		else:
			return None
	
	def query_and_lastrowid(self, sql: str, vars: tuple = ()):
		return self._query(sql, vars, True)[0]
	#endregion

	#region Methods for videos table
	def create_video(self, video_id: str, channel_username: str, video_href: str) -> None:
		''' Create video entry in db. '''
		self.query(
			'''INSERT INTO videos (video_id, channel_username, video_href) VALUES (%s, %s, %s)
			ON CONFLICT (video_id) DO UPDATE SET channel_username = %s,  video_href = %s;''',
			(video_id, channel_username, video_href, channel_username, video_href)
		)
	#endregion
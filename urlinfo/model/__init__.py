from flask_sqlalchemy import SQLAlchemy
import urllib

db = SQLAlchemy()

class UrlInfoParams:
	def __init__(self, url_path, url_full_path, host_and_port, original_path_query_string=None):
		self.url_path = url_path
		self.host_and_port = host_and_port
		self.original_path_query_string = original_path_query_string
		self.url_full_path = url_full_path

		normalized_full_path = self.url_full_path if self.url_full_path[-1] != '?' else self.url_full_path[:-1]
		path_and_query_string = normalized_full_path.replace('/urlinfo/1/' + self.host_and_port + '/','')

		self.normalized_path_query_string = urllib.quote(path_and_query_string.encode('utf-8'), safe='')

	def to_urlinfo(self):
		url = "{0}/{1}".format(self.host_and_port, self.normalized_path_query_string if self.normalized_path_query_string is not None else '')
		urlinfo = UrlInfo(url, 0)
		return urlinfo

class UrlInfo(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String, unique=True, nullable=False)
	malware = db.Column(db.Integer, nullable=False)

	def __init__(self, url, malware):
		self.url = url
		self.malware = malware

	def __str__(self):
		s =  """
		id: [{0}],
		url: [{1}],
		malware: [{2}]
		""".format(self.id, self.url, self.malware)
		return s
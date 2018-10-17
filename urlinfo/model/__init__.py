from flask_sqlalchemy import SQLAlchemy
from flask import g
import urllib

class MultiTenantSQLAlchemy(SQLAlchemy):
    def choose_tenant(self, bind_key):
        if hasattr(g, 'tenant'):
        	pass
            #raise RuntimeError('Switching tenant in the middle of the request.')
        g.tenant = bind_key

    def get_engine(self, app=None, bind=None):
        if bind is None:
            if not hasattr(g, 'tenant'):
                raise RuntimeError('No tenant chosen.')
            bind = g.tenant
        return super(MultiTenantSQLAlchemy, self).get_engine(app=app, bind=bind)

db = MultiTenantSQLAlchemy() 

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
	__tablename__ = 'url_info'
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

class UrlInfoRepository:
	def __init__(self, db_session):
		self.session = db_session

	def add(self, url_info):
		self.session.add(url_info)
		self.session.commit()

	def add_all(self, url_infos):
		self.session.add_all(url_infos)
		self.session.commit()

	def get(self, url_info):
		return self.session.query(UrlInfo).filter_by(url=url_info.url).first_or_404()

	def delete_all(self):
		self.session.query(UrlInfo).delete()
		self.session.commit()
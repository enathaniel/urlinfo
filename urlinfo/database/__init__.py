from ..model import UrlInfo

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

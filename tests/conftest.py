import pytest, traceback
from urlinfo import create_app
from urlinfo.database import db


@pytest.fixture
def app():
	print('Prepare URLInfo Flask app')
	app = create_app('testing')
	app.testing = True
	with app.app_context():
		try:
			db.clear_db(app)
		except Exception as e:
			print("Failed db.clear_db: " + str(e))

		try:
			db.init_db(app)
		except Exception as e:
			print("Failed db.init_db")
			traceback.print_exc()

		try:
			db.seed_db(app)
		except Exception as e:
			print("Failed db.seed_db")
			traceback.print_exc()

	yield app

	# clean up once done
	with app.app_context():
		try:
			db.clear_db(app)
		except Exception as e:
			print("Failed db.clear_db")
			traceback.print_exc()


@pytest.fixture
def client(app):
	return app.test_client()
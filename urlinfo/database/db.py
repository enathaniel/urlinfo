import click
import os

from flask import current_app
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from ..model import db, UrlInfo
from . import UrlInfoRepository

def initialize(app):
	instance_db_path = os.path.join(app.instance_path, app.config['DATABASE'])

	# Windows: sqlite:/// vs non-Windows: sqlite:////
	db_connection_template =  '{0}:///{1}' if os.name == 'nt' else  '{0}:////{1}'
	app.config['SQLALCHEMY_DATABASE_URI'] = db_connection_template.format(app.config['DB_ENGINE'],instance_db_path)
	app.logger.info("SQLALCHEMY_DATABASE_URI: " + app.config['SQLALCHEMY_DATABASE_URI'])

	if app.config['SHARDS'] is not None:
		app.config['SQLALCHEMY_BINDS'] = {}
		for key, value in app.config['SHARDS'].iteritems():
			shard_db = db_connection_template.format(app.config['DB_ENGINE'] ,instance_db_path + '.' + value )
			app.config['SQLALCHEMY_BINDS'][key] = shard_db

	db.init_app(app)
	register_command(app)
	return db;

def register_command(app):
	app.cli.add_command(init_db_command)
	app.cli.add_command(seed_db_command)
	app.cli.add_command(clear_db_command)

@click.command('init-db')
@with_appcontext
def init_db_command():
	init_db(current_app)
	register_command(current_app)

@click.command('seed-db')
@with_appcontext
def seed_db_command():
	seed_db(current_app)

@click.command('clear-db')
@with_appcontext
def clear_db_command():
	clear_db(current_app)

def init_db(app):
	app.logger.info("DB -- Initializing Database")
	db = initialize(app)
	from ..model import UrlInfo

	binds = app.config['SQLALCHEMY_BINDS']

	if binds is not None:
		for key, value in binds.iteritems():
			db.choose_tenant(key)
			db.create_all()
			db.session.commit()
			db.session.close()
			db.session.remove()
	app.logger.info("DB -- Database is created")

def seed_db(app):
	app.logger.info("DB -- Seeding Database")
	repository = UrlInfoRepository(db.session)
	repository.add_all([
		UrlInfo("www.google.com:8080/index.html", 0),
		UrlInfo("www.google.com:8080/index.html%3Fname%3Dedwin", 1),
		UrlInfo("example.com/%E5%BC%95%E3%81%8D%E5%89%B2%E3%82%8A.html", 0)
	])
	app.logger.info("DB -- Database is seeded")	

def clear_db(app):
	app.logger.info("DB -- Clear the Database")
	repository = UrlInfoRepository(db.session).delete_all()
	app.logger.info("DB -- Database is Cleared")

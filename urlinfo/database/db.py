import click
import os

from flask import current_app
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from uhashring import HashRing
from ..model import db, UrlInfo, UrlInfoRepository

def initialize(app):
	instance_db_path = os.path.join(app.instance_path, app.config['DATABASE'])

	# Windows: sqlite:/// vs non-Windows: sqlite:////
	db_connection_template =  '{0}:///{1}' if os.name == 'nt' else  '{0}:////{1}'
	app.config['SQLALCHEMY_DATABASE_URI'] = db_connection_template.format(app.config['DB_ENGINE'],instance_db_path)

	if app.config['SHARDS'] is not None:
		app.config['SQLALCHEMY_BINDS'] = {}
		nodes = {}
		for key, value in app.config['SHARDS'].iteritems():
			shard_db = db_connection_template.format(app.config['DB_ENGINE'] ,instance_db_path + '.' + value )
			app.config['SQLALCHEMY_BINDS'][key] = shard_db
			nodes[key] = {'instance': key}
		app.config['HASHRING'] = HashRing(nodes)

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
	''' Initialize the databases via CLI: wrapper of init_db '''
	init_db(current_app)
	register_command(current_app)

@click.command('seed-db')
@with_appcontext
def seed_db_command():
	''' Seed the databases via CLI: wrapper of seed_db '''
	seed_db(current_app)

@click.command('clear-db')
@with_appcontext
def clear_db_command():
	''' Clear the databases via CLI: wrapper of clear_db '''
	clear_db(current_app)

def with_db(db, app):
	''' Generator to wrap multitenant DBs '''
	binds = app.config['SQLALCHEMY_BINDS']

	if binds is not None:
		for key, value in binds.iteritems():
			db.choose_tenant(key)
			yield db
			db.session.close()
			db.session.remove()	

def init_db(app):
	app.logger.info("DB -- Initializing Database")
	db = initialize(app)
	
	from ..model import UrlInfo
	dbs = with_db(db, app)
	for item in dbs:
		item.create_all()
		item.session.commit()

	app.logger.info("DB -- Database is created")

def seed_db(app):
	app.logger.info("DB -- Seeding Database")

	hr = app.config['HASHRING']

	url_infos = get_malware_urls(app)
	for url_info in url_infos:
		#app.logger.info("Using " + hr[url])
		db.choose_tenant(hr[url_info.url])
		repository = UrlInfoRepository(db.session)
		repository.add(url_info)
		db.session.close()
		db.session.remove()

	app.logger.info("DB -- Database is seeded")	

def get_malware_urls(app):
	seed_file = os.path.join(app.root_path, "resources", "list.txt")
	file = open(seed_file, "r")
	url_infos = []
	for line in file:
		url = line.replace('\n', '')
		url_infos.append(UrlInfo(url, 1))
	return url_infos

def clear_db(app):
	app.logger.info("DB -- Clear the Database")

	dbs = with_db(db, app)
	for item in dbs:
		repository = UrlInfoRepository(item.session)
		repository.delete_all()

	app.logger.info("DB -- Database is Cleared")

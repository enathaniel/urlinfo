import click
import os

from flask import current_app
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from ..model import db
from ..model.urlinfo import UrlInfo

def initialize(app):
	instance_db_path = os.path.join(app.instance_path, app.config['DATABASE'])

	# Windows: sqlite:/// vs non-Windows: sqlite:////
	db_connection_template =  '{0}:///{1}' if os.name == 'nt' else  '{0}:////{1}'
	app.config['SQLALCHEMY_DATABASE_URI'] = db_connection_template.format(app.config['DB_ENGINE'],instance_db_path)
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
	db = initialize(current_app)
	current_app.logger.info("DB -- Initializing Database")
	from ..model.urlinfo import UrlInfo
	db.create_all()
	db.session.commit()
	current_app.logger.info("DB -- Database is created")

@click.command('seed-db')
@with_appcontext
def seed_db_command():
	current_app.logger.info("DB -- Seeding Database")
	db.session.add_all([
		UrlInfo("www.google.com:8080/index.html", 0),
		UrlInfo("www.google.com:8080/index.html%3Fname%3Dedwin", 1),
		UrlInfo("example.com/%E5%BC%95%E3%81%8D%E5%89%B2%E3%82%8A.html", 0)
	])
	db.session.commit()
	current_app.logger.info("DB -- Database is seeded")

@click.command('clear-db')
@with_appcontext
def clear_db_command():
	current_app.logger.info("DB -- Deleting Database")
	UrlInfo.query.delete()
	db.session.commit()
	current_app.logger.info("DB -- Database is deleted")
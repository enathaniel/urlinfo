#!/usr/bin/env bash

export FLASK_APP=urlinfo
export FLASK_DEBUG=1


display_usage() { 
	echo "Usage: ./run.sh [option]"
	echo "Available options are: "
	echo "	run 	 - run urlinfo web service"
	echo "	init-db  - initialize the database"
	echo "	seed-db  - populate database with sample data"
	echo "	clear-db - clean up the url info database"

} 

if [  $# -ne 1 ] 
then 
	display_usage
	exit 1
fi 

python -m flask $1

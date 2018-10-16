URLInfo
=======

URLInfo is a web-service to check whether a URL contains malware or not.

# Requirements

The requirements to run URLInfo web-service are:
* Ubuntu 16.04 / 18.04
* Python 2.7
	* pip
* SQLite
* Git

0. Refresh your repository
```
sudo apt update
sudo apt upgrade
```

1. Install Python (most likely already installed in Ubuntu)
```
sudo apt install python2.7 
```

2. Install pip

```
sudo apt install python-pip
```

3. Install SQLite3

```
sudo apt install sqlite3 libsqlite3-dev
```

4. Install Git
```
sudo apt install git-core
```

# Development Environment

Once all required software are installed, we have to check out the code and prepare the environment.

1. Clone the git repo

```
git clone https://github.com/enathaniel/urlinfo.git
```

2. Install Python libraries

go to urlinfo folder
```
cd urlinfo
pip install -r requirements.txt
```

# Running the app

There is a shell script prepared to help play around with the web-service

```
$./run.sh
Usage: ./run.sh [option]
Available options are: 
	run 	 - run urlinfo web service
	init-db  - initialize the database
	seed-db  - populate database with sample data
	clear-db - clean up the url info database
```

We have to run the webservice at least once to install the database commands (this is done via Python "click" library)

```
chmod a+x run.sh
./run.sh run
# don't forge to kill the server via Ctrl+C
```

1. Prepare and seed the database

```
./run.sh init-db
./run.sh seed-db
```

2. Run the webservice

```
./run.sh run
```

3. [Optional] Clear the table
```
./run.sh clear-db
```

*Notes*
* init-db can be run many times
* seed-db can only be run if the database is empty 
	(otherwise unique constraint will be violated since it's the same seed data)
* clear-db helps to clear the database

# Accessing the service

Go to http://127.0.0.1:5000/urlinfo/1/{host_and_port}/{original_path_and_query_string}

For example:
Testing unicode: http://127.0.0.1:5000/urlinfo/1/example.com/&#24341;&#12365;&#21106;&#12426;.html
Testing query-string: www.google.com:8080/index.html?name=edwin


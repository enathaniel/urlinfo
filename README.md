URLInfo
=======

URLInfo is a web-service to check whether a URL contains malware or not.

# Requirements

The requirements to run URLInfo web-service are:
* Ubuntu 16.04 / 18.04
* Python 2.7
	* pip
	* pytest
* SQLite3
* Git
* Curl (for testing via command-line)

0. Refresh your repository
```
# on Ubuntu 18.04 server, follow https://askubuntu.com/a/1061488 before updating your repo
sudo apt update
sudo apt upgrade -y
```

1. Install required software
_NOTE_: If somehow Ubuntu failed to locate python-pip (e.g. Ubuntu Server 2018), follow the steps suggested here: https://askubuntu.com/a/1061488
```
sudo apt install python2.7 python-pip python-pytest sqlite3 libsqlite3-dev git-core curl -y
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

# Running URLInfo Web Service

There is a shell script, located at the root folder, prepared to help play around with the web-service

```
$./run.sh
Usage: ./run.sh [option]
Available options are: 
	run 	 - run urlinfo web service
	init-db  - initialize the database
	seed-db  - populate database with sample data
	clear-db - clean up the url info database
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

4. Running the test
```
# done inside urlinfo folder
pytest
```

*Notes*
* init-db can be run many times
* seed-db can only be run if the database is empty 
	(otherwise unique constraint will be violated since it's the same seed data)
* clear-db helps to clear the database

# Accessing the service

Go to http://127.0.0.1:5000/urlinfo/1/{host_and_port}/{original_path_and_query_string}

You can use seed data located at:
* {root_folder}/urlinfo/resources/goodlist.txt => list of good URLs
* {root_folder}/urlinfo/resources/badlist.txt => list of bad URLS (contain malware)

Good URLs should return 
```
{
	malware: 0
}. 
```

Bad URLs should return 
```
{
	malware:1
}
```

For example:
* good: http://127.0.0.1:5000/urlinfo/1/www.sap.com
* good: http://127.0.0.1:5000/urlinfo/1/google.com/search?ei=pxnIW7CWJZzB0PEPnKyTuAo&q=whitelist+url&oq=whitelist+url&gs_l=psy-ab.3..0l10.1628.1843.0.1977.3.2.0.1.1.0.126.126.0j1.1.0....0...1c.1.64.psy-ab..1.2.127....0.kwayDVX1rY0
* bad: http://127.0.0.1:5000/urlinfo/1/vensart.net/b1patch.exe
* bad: http://127.0.0.1:5000/urlinfo/1/xxvtrrmbuqshu.biz/news/?s=1681

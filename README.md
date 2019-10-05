# Sample chat with aiohttp
  
A minor project showcasing how WebSockets work using aiohttp. It has two main applications, for authentication and websockets' implementation.
  
## Getting started ##

The project was mainly built using aiohttp as an asynchronous server, motor as an asynchronous driver for MongoDB, and Jinja2 for working with templates

### Prerequisites ###

What software you need to install and how to install them

Redis
```bash
sudo apt-get update
sudo apt-get install -y redis-server
```
MongoDB
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
sudo apt-get update
sudo apt-get install -y mongodb-org
```
Python3.7
```bash
sudo apt-get install python3.7 python3.7-venv
```

Check if MongoDB and Redis are active
```bash
sudo service redis status
sudo service mongod status
```

### How to run the project ###

Make sure, you have python 3.7, python3.7-venv, git, and MongoBD being installed, then do the following:

1.  ```git clone https://github.com/Silver3310/Aiohttp-sample-chat```
2.  ```cd Aiohttp-sample-chat```
3.  ```python3.7 -m venv venv```
4.  ```source venv/bin/activate```
5.  ```pip install -r requirements.txt```
6.  ```echo "REDIS_HOST='<YOUR_REDIS_HOST>'\nREDIS_PORT='<YOUR_REDIS_PORT>'\nMONGO_HOST='<YOUR_MONGO_HOST_AND_PORT>'\nMONGO_DB_NAME='<YOUR_MONGO_DB_NAME>'" > .env```
7.  ```python main.py```
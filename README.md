# Start2Impact Final project: Auction platform powered by Ethereum blockchain
Auction platform that records the results of each auction on the Ethereum blockchain (Testnet Ropsten).

When an auction is created if the price and opening date are set properly, the system will automatically open the auction
and make it available to all users in the "Live auctions" section on the set date.\
Each auction remains open for a random time between 22 and 24 hours if it does not receive any bids.
Once the time has expired, the auction will be closed permanently.\
When an auction receives a bid[^1], the system waits 10 minutes before closing the auction (The previous random time is canceled) and decree the winner.
If within this time another user makes a new bid then the system restart waiting 10 minutes from that moment.\
When an auction is closed, a report summarizing all the information relating to the auction and the possible winning is generated.
Finally, the hash (SHA256) of the report is calculated and the result is written to the Ethereum blockchain.
Through the report provided by the web-app and the hash registered on the blockchain, it is possible 
to check and verify the genuineness of the winning and the reported data.

[^1]: Redis is required for Django Channels and Celery dependencies, as well as for the web-app's bidding system.\
For reasons of optimization and scalability, the system registers the bids exclusively on Redis.
The data relating to the winning bid are stored on the SQLite3 database only at the close of the auction.

**Live demo: [ChainBid](http://13.37.247.221/)**

***

# Index
1. [Features](#Features)
	1. [User interface](#User-interface)
	2. [API endpoints](####API-endpoints)
3. [Components and technologies](#Components-and-technologies)
4. []()

***

# Features

#### User interface
* User registration and authentication.
* Schedule new auctions.
* Display live auctions and participate via a bidding system.
* Display closed auctions and check the results.
* User profile.

#### API endpoints
* ```/api/rest-auth/registration/```: User registration via token.
* ```/api/rest-auth/login/```: Authentication via token.
* ```/api/user/```: Retrieve current user information.
* ```/api/profile/<user slug>/```: Retrieve the user profile.
* ```/api/schedule-auctions/```: List scheduled auctions or create a new one.
* ```/api/schedule-auctions/<auction slug>/```: Retrieve, update, delete a scheduled auction.
* ```/api/schedule-auctions/<auction slug>/upload-image/```: Update scheduled auction's image.
* ```/api/auctions/```: List live auctions.
* ```/api/auctions/<auction slug>/```: Retrieve a live auction.
* ```/api/closed-auctions/```: List closed auctions.
* ```/api/closed-auctions/<auction slug>/```: Retrieve a closed auction.
* ```/api/<user slug>/auctions/```: List auctions won by the user.

***

# Components and technologies

**Back-end**
* [Django 3.2](https://docs.djangoproject.com/en/3.2/) - Core
* [Django REST Framework 3.12](https://www.django-rest-framework.org/) - APIs
* [Django Channels 3.0](https://channels.readthedocs.io/en/stable/index.html) - WebSockets
* [Web3 5.23](https://web3py.readthedocs.io/en/stable/#) - Interface for Ethereum blockchain
* [Celery 5.1](https://docs.celeryproject.org/en/v5.1.2/) - Scheduled tasks

**Front-end**
* [Vue.js 2.6](https://vuejs.org/v2/guide/) - Core
* [Bootstrap 5.1](https://getbootstrap.com/docs/5.1/getting-started/introduction/) - CSS
* [ReconnectingWebSocket 1.0](https://github.com/joewalnes/reconnecting-websocket) - WebSockets
* [Vue Router 3.5](https://router.vuejs.org/guide/) - Page routing
* [Vue Toasted 1.1](https://github.com/shakee93/vue-toasted#readme) - Notifications
* [V Clipboard 2.2](https://github.com/euvl/v-clipboard#readme) - Copy to clipboard functionality
* [Moment.js 2.29](https://momentjs.com/docs/) - Date and time display

**Databases**
* [SQLite](https://sqlite.org/docs.html) - Storage and web-app structure
* [Redis](https://redis.io/documentation) - Bidding system

***

# Setup for production

### First step
Clone the repository and install the required packages:
```
$ sudo apt-get update upgrade
$ sudo apt-get install net-tools python3.9 python3.9-dev python3-virtualenv gcc nginx redis-server
$ git clone -b production https://github.com/pogginicolo98/start2impact_final-project.git
```

### Virtual environment
Create a virtual Python environment and install the project dependencies:
```
start2impact_final-project$ virtualenv venv -p python3.9
start2impact_final-project$ source venv/bin/activate
(venv) start2impact_final-project$ pip install -r setup/requirements.txt
```

### Redis
Open the file `/etc/redis/redis.conf` and replace the command `supervised no` with `supervised systemd`\
Then restart the service:
```
$ sudo systemctl restart redis
$ sudo systemctl enable redis
```
Verify that the service is running correctly:
```
$ sudo systemctl status redis
```

### Django project
Open `start2impact_final-project/setup/password_empty.py` and replace placeholders with your secret keys.\
Than initialize the database, create a super user, execute the automated tests and collect static files as follows:
```
(venv) start2impact_final-project$ cp setup/password_empty.py chainBid/password.py
(venv) start2impact_final-project/chainBid$ python manage.py makemigrations
(venv) start2impact_final-project/chainBid$ python manage.py migrate
(venv) start2impact_final-project/chainBid$ python manage.py createsuperuser
(venv) start2impact_final-project/chainBid$ python manage.py test
(venv) start2impact_final-project/chainBid$ python manage.py collectstatic
```

### Gunicorn
Host WSGI application with Gunicorn:
```
start2impact_final-project$ sudo cp setup/gunicorn.socket /etc/systemd/system/
start2impact_final-project$ sudo cp setup/gunicorn.service /etc/systemd/system/
$ sudo systemctl start gunicorn.socket
$ sudo systemctl enable gunicorn.socket
```
Verify that the service is running correctly:
```
$ sudo systemctl status gunicorn.socket
```

### Daphne
Host ASGI application with Daphne:
```
start2impact_final-project$ sudo cp setup/daphne.service /etc/systemd/system/
$ sudo systemctl start daphne.service
$ sudo systemctl enable daphne.service
```
Verify that the service is running correctly:
```
$ sudo systemctl status daphne.service
```

### Celery
Manage scheduled tasks with Celery:
```
start2impact_final-project$ sudo cp setup/celery.service /etc/systemd/system/
$ sudo systemctl start celery.service
$ sudo systemctl enable celery.service
```
Verify that the service is running correctly:
```
$ sudo systemctl status celery.service
```

### Nginx
Configure Nginx to Proxy Pass to Gunicorn. It helps to protect the website from attackers.\
Update `/etc/nginx/nginx.conf` Nginx config file in order to upload large files (images in that case)
```
http{
	...
	client_max_body_size 100M; 
}
```
Then add the website configuration and update the firewall:
```
start2impact_final-project$ sudo cp setup/chainbid /etc/nginx/sites-available/
$ sudo ln -s /etc/nginx/sites-available/chainbid /etc/nginx/sites-enabled/
$ sudo nginx -t
$ sudo ufw allow 'Nginx Full'
$ sudo systemctl restart nginx
$ sudo systemctl enable nginx
```
Verify that the service is running correctly:
```
$ sudo systemctl status nginx
```

### Debugging
List of commands useful for debugging possible errors:\
`$ sudo journalctl -u <service>`: Service logs\
`$ sudo systemctl status <service>`: Service status

**Services**
* gunicorn.socket
* daphne.service
* celery.service
* nginx
* redis

### Reboot
If everythings is running correctly reboot the system and then the web-app should be available at the address of the server: `$ sudo reboot`

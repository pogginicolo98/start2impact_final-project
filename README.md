# Start2Impact Final project: Auction platform powered by Ethereum blockchain
Auction platform that records the results of each auction on the Ethereum blockchain (Testnet Ropsten).

When an auction is created if the price and opening date are set properly, the system will automatically open the auction
and make it available to all users in the "Live auctions" section on the set date.\
Each auction remains open for a random time between 20 and 24 hours if no one places a bid.\
When a user places a bid, the system waits 10 minutes before closing the auction (the previous random time is canceled) and decree the winner.
If within this time another user places a new bid then the system restart waiting 10 minutes from that moment.\
When an auction is closed, a report summarizing all the information about it is generated.\
Lastly the hash (SHA256) of the report is calculated and the result is written on chain.
Thanks to the downloadable report and the transaction id (and the hash inside the transaction message), it is possible to check the authenticity of the winning and the reported data.

**Docs: [Project presentation slides](https://github.com/pogginicolo98/start2impact_final-project/blob/f6252fbec2a5c0d103f4663f683b39d397eb60f8/docs/Project%20presentation.pdf)**\
**Live demo: [ChainBid](http://13.37.247.221/)**

***

# Index
1. [Features](#Features)
	1. [User interface](#User-interface)
	2. [API endpoints](#API-endpoints)
2. [Components and technologies](#Components-and-technologies)
	1. [Back-end](#Back-end)
	2. [Front-end](#Front-end)
	3. [Databases](#Databases)
3. [Deploy in production](#Deploy-in-production)
	1. [Setup](#Setup)
	2. [Virtual environment](#Virtual-environment)
	3. [Redis](#Redis)
	4. [Django project](#Django-project)
	5. [Gunicorn](#Gunicorn)
	6. [Daphne](#Daphne)
	7. [Celery](#Celery)
	8. [Nginx](#Nginx)
	9. [Reboot](#Reboot)
	10. [Debugging](#Debugging)

***

# Features

### User interface
* User registration and authentication.
* Schedule new auctions.
* View live auctions and participate via a bidding system.
* View closed auctions and check the results.
* View th user profile.

### API endpoints
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

### Back-end
* [Django 3.2](https://docs.djangoproject.com/en/3.2/) - Core
* [Django REST Framework 3.12](https://www.django-rest-framework.org/) - APIs
* [Django Channels 3.0](https://channels.readthedocs.io/en/stable/index.html) - WebSockets
* [Web3 5.23](https://web3py.readthedocs.io/en/stable/#) - Interface for Ethereum blockchain
* [Celery 5.1](https://docs.celeryproject.org/en/v5.1.2/) - Scheduled tasks

### Front-end
* [Vue.js 2.6](https://vuejs.org/v2/guide/) - Core
* [Bootstrap 5.1](https://getbootstrap.com/docs/5.1/getting-started/introduction/) - CSS
* [ReconnectingWebSocket 1.0](https://github.com/joewalnes/reconnecting-websocket) - WebSockets
* [Vue Router 3.5](https://router.vuejs.org/guide/) - Page routing
* [Vue Toasted 1.1](https://github.com/shakee93/vue-toasted#readme) - Notifications
* [V Clipboard 2.2](https://github.com/euvl/v-clipboard#readme) - Copy to clipboard functionality
* [Moment.js 2.29](https://momentjs.com/docs/) - Date and time display

### Databases
* [SQLite](https://sqlite.org/docs.html) - Storage and web-app structure
* [Redis](https://redis.io/documentation) - Bidding system [^1]

[^1]: Redis is required for Django Channels and Celery dependencies, as well as for the web-app's bidding system.\
For reasons of optimization and scalability, the system registers the bids exclusively on Redis.
The data relating to the winning bid are stored on the SQLite3 database only at the close of the auction.

***

# Deploy in production

### Setup
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
Check that the service is running correctly:
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
Open `start2impact_final-project/setup/gunicorn.socket` and replace placeholders with production data.\
Host WSGI application with Gunicorn:
```
start2impact_final-project$ sudo cp setup/gunicorn.socket /etc/systemd/system/
start2impact_final-project$ sudo cp setup/gunicorn.service /etc/systemd/system/
$ sudo systemctl start gunicorn.socket
$ sudo systemctl enable gunicorn.socket
```
Check that the service is running correctly:
```
$ sudo systemctl status gunicorn.socket
```

### Daphne
Open `start2impact_final-project/setup/daphne.service` and replace placeholders with production data.\
Host ASGI application with Daphne:
```
start2impact_final-project$ sudo cp setup/daphne.service /etc/systemd/system/
$ sudo systemctl start daphne.service
$ sudo systemctl enable daphne.service
```
Check that the service is running correctly:
```
$ sudo systemctl status daphne.service
```

### Celery
Open `start2impact_final-project/setup/celery.service` and replace placeholders with production data.\
Manage scheduled tasks with Celery:
```
start2impact_final-project$ sudo cp setup/celery.service /etc/systemd/system/
$ sudo systemctl start celery.service
$ sudo systemctl enable celery.service
```
Check that the service is running correctly:
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
Open `start2impact_final-project/setup/PROJECT_NAME` and replace placeholders with production data.\
Then add the website configuration and update the firewall:
```
start2impact_final-project$ sudo cp setup/PROJECT_NAME /etc/nginx/sites-available/chainbid
$ sudo ln -s /etc/nginx/sites-available/chainbid /etc/nginx/sites-enabled/
$ sudo nginx -t
$ sudo ufw allow 'Nginx Full'
$ sudo systemctl restart nginx
$ sudo systemctl enable nginx
```
Check that the service is running correctly:
```
$ sudo systemctl status nginx
```

### Reboot
If everythings is running correctly reboot the system and then the web-app should be available at the address of the server: `$ sudo reboot`

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

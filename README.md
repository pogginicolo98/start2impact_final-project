# Start2Impact Final project: Auction platform powered by Ethereum blockchain
Auction platform that records the results of each auction on the Ethereum blockchain (Testnet Ropsten).

When an auction is created if the price and opening date are set properly, the system will automatically open the auction
and make it available to all users in the "Live auctions" section on the set date.
Each auction remains open for a random time between 22 and 24 hours if it does not receive any bids.
Once the time has expired, the auction will be closed permanently.
When an auction receives a bid, the system waits 10 minutes before closing it and deciding the winner.
If within this time another user makes a new bid then the time resets and another 10 minutes must pass before the auction closes.
When an auction is closed, a report summarizing all the information relating to the auction and the possible winning is generated.
Finally, the hash (SHA256) of the report is calculated and the result is written to the Ethereum blockchain.
Through the report provided by the web-app and the hash registered on the blockchain, it is possible 
to check and verify the genuineness of the winning and the reported data.

#### Live demo: [ChainBid](http://13.37.247.221/)

[test](#Components-and-technologies)

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
* ```/api/profile/<user.slug>/```: Retrieve the user profile.
* ```/api/schedule-auctions/```: List scheduled auctions or create a new one.
* ```/api/schedule-auctions/<auction.slug>/```: Retrieve, update, delete a scheduled auction.
* ```/api/schedule-auctions/<auction.slug>/upload-image/```: Update scheduled auction's image.
* ```/api/auctions/```: List live auctions.
* ```/api/auctions/<auction.slug>/```: Retrieve a live auction.
* ```/api/closed-auctions/```: List closed auctions.
* ```/api/closed-auctions/<auction.slug>/```: Retrieve a closed auction.
* ```/api/<user.slug>/auctions/```: List auctions won by the user.


# Components and technologies
#### Back-end
* [Django 3.2](https://docs.djangoproject.com/en/3.2/) - Core
* [Django REST Framework 3.12](https://www.django-rest-framework.org/) - APIs
* [Django Channels 3.0](https://channels.readthedocs.io/en/stable/index.html) - WebSockets
* [Web3 5.23](https://web3py.readthedocs.io/en/stable/#) - Interface for Ethereum blockchain
* [Celery 5.1](https://docs.celeryproject.org/en/v5.1.2/) - Scheduled tasks

#### Front-end
* [Vue.js 2.6](https://vuejs.org/v2/guide/) - Core
* [Bootstrap 5.1](https://getbootstrap.com/docs/5.1/getting-started/introduction/) - CSS
* [ReconnectingWebSocket 1.0](https://github.com/joewalnes/reconnecting-websocket) - WebSockets
* [Vue Router 3.5](https://router.vuejs.org/guide/) - Page routing
* [Vue Toasted 1.1](https://github.com/shakee93/vue-toasted#readme) - Notifications
* [V Clipboard 2.2](https://github.com/euvl/v-clipboard#readme) - Copy to clipboard functionality
* [Moment.js 2.29](https://momentjs.com/docs/) - Date and time display

#### Databases
* [SQLite](https://sqlite.org/docs.html) - Storage and web-app structure
* [Redis](https://redis.io/documentation) - Bidding system


## Setup for production
#### Clone the repository and install some required packages:
```
$ git clone https://github.com/pogginicolo98/start2impact_social-dex
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get update
$ sudo apt-get install python3.9
$ sudo apt-get install gcc
$ sudo apt-get install python3-virtualenv
```

#### Configure the virtual environment:
```
start2impact_social-dex$ virtualenv venv -p python3.9
start2impact_social-dex$ source venv/bin/activate
(venv) start2impact_social-dex$ pip install -r requirements.txt
```

#### Install Redis:
```
start2impact_social-dex$ wget https://download.redis.io/releases/redis-6.2.5.tar.gz
start2impact_social-dex$ tar xzf redis-6.2.5.tar.gz
start2impact_social-dex$ cd redis-6.2.5
start2impact_social-dex/redis-6.2.5$ sudo make
start2impact_social-dex/redis-6.2.5$ sudo make test
```

Run Redis in then background using ```$ screen``` then press ```ENTER```, then ```start2impact_social-dex/redis-6.2.5$ src/redis-server```, then press ```CTRL+A``` and finally press ```D```. (These commands must be executed every time the server is restarted)

#### Setup and test django project:
First of all populate ```start2impact_social-dex/setup/password_empty.py``` with your keys.
```
start2impact_social-dex$ mv setup/password_empty.py social_dex/password.py
(venv) start2impact_social-dex/social_dex$ python manage.py runserver
(venv) start2impact_social-dex/social_dex$ python manage.py makemigrations
(venv) start2impact_social-dex/social_dex$ python manage.py migrate
(venv) start2impact_social-dex/social_dex$ python manage.py test
```

#### Install and configure Gunicorn:
```
(venv) start2impact_social-dex$ pip install gunicorn
start2impact_social-dex$ mv setup/gunicorn_start.bash .
start2impact_social-dex$ sudo chmod u+x gunicorn_start.bash
```

#### Install and configure Supervisor:
```
$ sudo apt-get install supervisor
start2impact_social-dex$ sudo mv setup/social_dex_supervisor.conf /etc/supervisor/conf.d/social_dex.conf
start2impact_social-dex$ mkdir logs
start2impact_social-dex$ mv setup/gunicorn_supervisor.log logs/
$ sudo systemcl restart supervisor
$ sudo systemcl enable supervisor
```
Check if Supervisor is working properly: ```$ sudo supervisorctl status social_dex```

#### Install and configure Nginx:
```
$ sudo apt-get install nginx
start2impact_social-dex$ mkdir static-serve
$ sudo rm /etc/nginx/sites-available/default
$ sudo rm /etc/nginx/sites-enabled/default
start2impact_social-dex$ sudo mv /setup/social_dex_nginx.conf /etc/nginx/sites-available/social_dex.conf
$ sudo ln -s /etc/nginx/sites-available/social_dex.conf /etc/nginx/sites-enabled/social_dex.conf
(venv) start2impact_social-dex/social_dex$ python manage.py collectstatic
$ sudo service nginx start
```
Check if Nginx is working properly by accessing to the server via browser. You should see a message like this:
![Nginx web page](.images/nginx.png)

If Nginx is working properly restart it with: ```$ sudo service nginx restart```. Now you should see the homepage and the web-app should working properly.

#### Enable scheduled tasks:
```$ screen``` then press ```ENTER```, then ```(venv) start2impact_social-dex/social_dex$ celery -A social_dex worker -B -l INFO```, then press ```CTRL+A``` and finally press ```D```. (These commands must be executed every time the server is restarted)

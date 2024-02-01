#!/usr/bin/env bash
# working on my web server configuration
sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'


if [ ! -e /data/ ]
then
	mkdir /data/
fi

if [ ! -e /data/web_static/ ]
then
        mkdir /data/web_static/
fi

if [ ! -e /data/web_static/releases/ ]
then
        mkdir /data/web_static/releases/
fi

if [ ! -e /data/web_static/shared/ ]
then
        mkdir /data/web_static/shared/
fi

if [ ! -e /data/web_static/releases/test/ ]
then
        mkdir /data/web_static/releases/test/
fi

sudo touch /data/web_static/releases/test/index.html
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

sudo service nginx restart

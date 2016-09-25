FROM ubuntu:16.04

# Update
RUN apt-get update

# Install app dependencies
RUN apt-get -y install python
RUN apt-get -y install python-pip
RUN pip install --upgrade pip
RUN pip install Flask
RUN pip install pyyaml
RUN apt-get -y install apache2
RUN apt-get -y install libapache2-mod-wsgi
RUN apt-get -y install python-dev

# enable wsgi mod
RUN a2enmod wsgi

# clean temps
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Bundle app source
RUN mkdir -p /var/www/jinjabread/jinjabread

COPY favicon.ico /var/www/jinjabread/jinjabread/favicon.ico
COPY functions    /var/www/jinjabread/jinjabread/functions
COPY static      /var/www/jinjabread/jinjabread/static
COPY templates   /var/www/jinjabread/jinjabread/templates
COPY __init__.py   /var/www/jinjabread/jinjabread/__init__.py

COPY jinjabread.conf /etc/apache2/sites-available/jinjabread.conf

COPY jinjabread.wsgi /var/www/jinjabread/jinjabread.wsgi

# Enable site in apache
RUN a2dissite 000-default
RUN a2ensite jinjabread

RUN service apache2 restart

EXPOSE 80
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]

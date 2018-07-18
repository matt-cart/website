#!/bin/bash

# Update OS and install Python
sudo apt-get update
sudo apt install python-minimal
sudo apt-get install python-pip
sudo apt install virtualenv

# Install Node and Yarn, then install CSS/JS resources using Yarn
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install -y nodejs
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get update && sudo apt-get install yarn
cd website/static
yarn install

# Install Apache
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi
sudo /etc/init.d/apache2 start

# Create symnbolic link for Apache to find
sudo ln -sT ~/website /var/www/html/website
sudo /etc/init.d/apache2 restart

# Move up to website home folder
cd ../..

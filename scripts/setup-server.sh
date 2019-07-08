#!/bin/bash
USER=ubuntu

apt-get update
apt-get install -y git vim build-essential python3.5-dev python3-venv \
  libncurses5-dev fabric postgresql-9.5 postgresql-server-dev-9.5 \
  libjpeg62-dev zlib1g-dev libfreetype6-dev

sudo -u postgres psql -c "CREATE DATABASE postgres ENCODING='UTF8' TEMPLATE=template0;"
sudo -u postgres psql -c "CREATE USER ubuntu;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE postgres TO ubuntu;"
sudo -u postgres psql -c "ALTER USER ubuntu CREATEDB;"

chmod +x /vagrant/scripts/setup-server-user.sh
sudo -H -u $USER /vagrant/scripts/setup-server-user.sh

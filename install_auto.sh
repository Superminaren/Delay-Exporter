#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run installer as root"
  exit
fi

SERVICE_DIR="/etc/systemd/system"
INSTALL_DIR="/usr/local/bin"
SCRIPT_DIR="/opt"
CONFIG_DIR="/etc"
PROJECT_NAME="prometheus-sl-exporter"
PROJECT_DIR=$PWD
PROJECT_USERNAME="prometheus"


adduser --disabled-password --gecos "" $PROJECT_USERNAME
#Install requirements for python
pip install -r requirements.txt

echo "COPY $PROJECT_NAME.sh"


# Making binary executable
chmod +x $INSTALL_DIR/$PROJECT_NAME #

# Making directory for python scripts
echo 'MAKE DIRECTORY'
mkdir $SCRIPT_DIR/$PROJECT_NAME


# Copying python scripts to Script folder
echo 'COPY SCRIPTS'
cp $PWD/*.py $SCRIPT_DIR/$PROJECT_NAME/


# Copying service to systemd
echo 'COPY SERVICE'
cp $PWD/config/$PROJECT_NAME-user.service $SERVICE_DIR/$PROJECT_NAME.service

# Copying config to etc -n to not overwrite if file exists.
echo 'COPY CONFIG'
cp -n $PWD/config/config.ini $CONFIG_DIR/$PROJECT_NAME.conf

echo "RELOAD SYSTEMD"
systemctl daemon-reload
systemctl enable $PROJECT_NAME

#Installer has finished
echo "----------------"
echo "Install complete"
echo "Please edit /etc/$PROJECT_NAME.conf to add key."
echo "Also edit /etc/systemd/system/$PROJECT_NAME.service to update user."
echo "----------------"

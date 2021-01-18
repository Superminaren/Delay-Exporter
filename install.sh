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


#Install requirements for python
pip install -r requirements.txt

echo "COPY $PROJECT_NAME.sh"


cp $PWD/$PROJECT_NAME.sh $INSTALL_DIR/$PROJECT_NAME

# Making binary executable
chmod +x $INSTALL_DIR/$PROJECT_NAME #

# Making directory for python scripts
mkdir $SCRIPT_DIR/$PROJECT_NAME


# Copying python scripts to Script folder
cp $PWD/*.py $SCRIPT_DIR/$PROJECT_NAME/


# Copying service to systemd
cp $PWD/config/$PROJECT_NAME.service $SERVICE_DIR/

# Copying config to etc
cp $PWD/config/config.ini $CONFIG_DIR/$PROJECT_NAME.conf


systemctl daemon-reload
systemctl enable $PROJECT_NAME

#Installer has finished
echo "----------------"
echo "Install complete"
echo "Please edit /etc/$PROJECT_NAME.conf to add key."
echo "Also edit /etc/systemd/system/$PROJECT_NAME.service to update user."
echo "----------------"

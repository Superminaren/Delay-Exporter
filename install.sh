#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run installer as root"
  exit
fi

INSTALL_DIR="/usr/local/bin"
SCRIPT_DIR="/opt/"
PROJECT_NAME="prometheus-sl-exporter"
PROJECT_DIR=$PWD

#Install requirements for python
pip install -r requirements.txt

echo "COPY $PROJECT_NAME.sh"


cp $PWD/$PROJECT_NAME.sh $INSTALL_DIR/$PROJECT_NAME
chmod +x $INSTALL_DIR/$PROJECT_NAME
mkdir $SCRIPT_DIR/$PROJECT_NAME

#TODO install

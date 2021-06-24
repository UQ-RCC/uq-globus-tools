#!/bin/sh

BASEDIR=/opt/uq-globus-tools
PYTHON=/opt/globus/bin/python3

#BASEDIR="$HOME/Documents/Coding/globus-uidmap"
#PYTHON=python

export GLOBUS_IDMAP_CONFIG_PATH="$BASEDIR/etc/config.json"
export PYTHONPATH="$BASEDIR/vendor:$PYTHONPATH"
exec $PYTHON "$BASEDIR/bin/idmap.py" $@

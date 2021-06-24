#!/bin/sh
export GLOBUS_IDMAP_CONFIG_PATH=/opt/uq-globus-tools/etc/idmap.json
exec /opt/globus/bin/python3 /opt/uq-globus-tools/bin/idmap.py

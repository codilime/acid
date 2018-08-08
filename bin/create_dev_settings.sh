#!/usr/bin/env bash

DEV_SETTINGS_NAME=settings_dev.yml

# copy only when settings.yml is newer
cp -u settings.yml $DEV_SETTINGS_NAME

# set full path to ~/.vagrant.d
sed -i "s/~\/.vagrant.d/\/home\/`whoami`\/.vagrant.d/" $DEV_SETTINGS_NAME
# set path to tmp file for host's fingerprints
sed -i 's/zuul_host_key.pub/\/tmp\/acid_dev_host_pub.key/' $DEV_SETTINGS_NAME

# clear ssh fingerprint for zuul dev server (on every start)
echo -n "" > /tmp/acid_dev_host_pub.key

#!/usr/bin/env bash

# npm
sudo npm i npm@11.2.0 -g
npm install -g pnpm


# nginx
sudo apt update
sudo apt install -y nginx apache2-utils

if [[ -f /etc/nginx/sites-enabled/default ]] ; then sudo unlink /etc/nginx/sites-enabled/default ;fi
sudo mkdir -p /etc/nginx/locations


# https://stackoverflow.com/questions/59895/how-do-i-get-the-directory-where-a-bash-script-is-l>
SOURCE=${BASH_SOURCE[0]}
while [ -L "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )
  SOURCE=$(readlink "$SOURCE")
  [[ $SOURCE != /* ]] && SOURCE=$DIR/$SOURCE # if $SOURCE was a relative symlink, we need to re>
done
DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )


pnpm install -C $DIR  && pnpm  -C $DIR start --host 0.0.0.0 --port 8005

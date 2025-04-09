#!/usr/bin/env bash

# install npm
# npm
# sudo apt install -y npm
# sudo npm i npm@11.2.0 -g
# npm install -g pnpm

# nginx

if ! which nginx &>/dev/null; then
  sudo apt update && sudo apt install nginx apache2-utils
fi

if [[ -f /etc/nginx/sites-enabled/default ]]; then sudo unlink /etc/nginx/sites-enabled/default; fi
sudo mkdir -p /etc/nginx/locations

# https://stackoverflow.com/questions/59895/how-do-i-get-the-directory-where-a-bash-script-is-l>
SOURCE=${BASH_SOURCE[0]}
while [ -L "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR=$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)
  SOURCE=$(readlink "$SOURCE")
  [[ $SOURCE != /* ]] && SOURCE=$DIR/$SOURCE # if $SOURCE was a relative symlink, we need to re>
done
DIR=$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)

if tty -s; then
  echo "I am on a TTY"
  IS_TTY=true
else
  echo "I am NOT on a TTY"
  IS_TTY=false

fi

DOCKER_TTY=""
if $IS_TTY; then
  DOCKER_TTY="-it"
fi

# env
PROJECT=mdeditor

PORT=8000
CONTENT=$DIR/content

NGINX_DOMAIN=$PROJECT
NGINX_USER=$PROJECT
NGINX_PSW=$PROJECT
if [[ ! -z "$MDE_PORT" ]]; then PORT=$MDE_PORT; fi
if [[ ! -z "$MDE_CONTENT" ]]; then CONTENT=$MDE_CONTENT; fi
if [[ ! -z "$MDE_DOMAIN" ]]; then NGINX_DOMAIN=$MDE_DOMAIN; fi

if [[ ! -z "$MDE_USER" ]]; then NGINX_USER=$MDE_USER; fi
if [[ ! -z "$MDE_PSW" ]]; then NGINX_PSW=$MDE_PSW; fi

CONATINER_NAME=$PROJECT-$NGINX_DOMAIN

echo PORT $PORT
echo CONTENT $CONTENT
echo NGINX_DOMAIN $NGINX_DOMAIN

echo NGINX_USER $NGINX_USER
echo NGINX_PSW $NGINX_PSW
echo CONATINER_NAME $CONATINER_NAME

if [ ! -z "$CMD" ]; then
  echo run $CMD
  docker run --name $CONATINER_NAME -e NGINX_DOMAIN="$NGINX_DOMAIN" -v $CONTENT:$CONTENT -v $DIR:$DIR -w $DIR --rm $DOCKER_TTY node:22 bash -c "npm install -g npm@11.2.0 && npm install -g pnpm && $CMD "

  exit 0

fi

if [ ! -f /etc/nginx/.htpasswd ]; then sudo htpasswd -bcB -C 10 /etc/nginx/.htpasswd $NGINX_USER $NGINX_PSW; else sudo htpasswd -bB -C 10 /etc/nginx/.htpasswd $NGINX_USER $NGINX_PSW; fi

if [ "$NGINX_OVERWRITE_CONF" == "true" ]; then
  sudo cp $DIR/default.conf /etc/nginx/conf.d/default.conf

else

  if [ ! -f "/etc/nginx/conf.d/default.conf" ]; then
    sudo cp $DIR/default.conf /etc/nginx/conf.d/default.conf
  fi
fi

sed "/proxy_pass/s/127.0.0.1:[0-9]\+/127.0.0.1:$PORT/" $DIR/location-$PROJECT.conf | sudo tee /etc/nginx/locations/location-$PROJECT-$NGINX_DOMAIN.conf
sudo sed -i "/$PROJECT/s/$PROJECT/$NGINX_DOMAIN/" /etc/nginx/locations/location-$PROJECT-$NGINX_DOMAIN.conf

sudo service nginx restart
sudo nginx -t && sudo systemctl reload nginx

# pnpm install -C $DIR  && pnpm  -C $DIR start --host 0.0.0.0 --port 8005
#docker run --name $CONATINER_NAME -v $CONTENT:$CONTENT -v $DIR:$DIR -w $DIR -p $PORT:$PORT --rm $DOCKER_TTY node:22 bash -c "npm install -g npm@11.2.0 && npm install -g pnpm && pnpm install && pnpm start --host 0.0.0.0 --port $PORT --base /$NGINX_DOMAIN"

docker run --name $CONATINER_NAME -e NGINX_DOMAIN="$NGINX_DOMAIN" -v $CONTENT:$CONTENT -v $DIR:$DIR -w $DIR --rm $DOCKER_TTY node:22 bash -c "npm install -g npm@11.2.0 && npm install -g pnpm && pnpm install && npm run build"

#pnpm install -C $DIR
#npm run build --prefic $DIR
if [ ! -d $DIR/mdeditor/dist ]; then ln -s $DIR/dist $DIR/mdeditor/; fi

python3 -m venv $DIR/.venv
source $DIR.venv/bin/activate
pip install -r $DIR/requirements.txt

#flask --debug --app main run --port $PORT --host 0.0.0.0
echo PORT $PORT
echo NGINX_DOMAIN $NGINX_DOMAIN
cd $DIR && gunicorn -w 1 --bind 0.0.0.0:$PORT main:app --reload --env FLASK_BASE_URL="$NGINX_DOMAIN"

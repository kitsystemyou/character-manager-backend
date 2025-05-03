# character-manager
Character Manager was made for managing TRPG character sheets.
There are vairious TRPG game systems and characters in each systems. We'd like to create the web application for them.
Now, there are some web app for managing character sheets (e.g. ) but they manage only one game system, or has legayc infra system.
So We try to create character manage web app which manage all game system characters and has modern infra system.

## Over view
This repository has a backend code of Character Manager.([Frontend is here](https://github.com/kitsystemyou/character-manager-frontend))

## API Documentation
https://kitsystemyou.github.io/character-manager-backend/dist/#/

## NEED
Pipenv

## getting start
DB(*)

```
docker run \
--restart=always \
--name charamane \
-e MYSQL_ROOT_PASSWORD=pass \
-e MYSQL_USER=user \
-e MYSQL_PASSWORD=pass \
-e TZ=Asia/Tokyo \
-p 3308:3306 \
-d mysql:8.0

mysql -h 127.0.0.1 --port 3308 -u root -ppass < ./migrate/initialize.sql
```


API

```
export FLASK_APP=flaskr
export FLASK_ENV=development

flask run
```

## if you use docker-compose
please start your mysql db with upper procedure (*)

```
docker network create charamanetwork
docker network connect charamanetwork charamane
docker compose up
# or docker compose up -d
```

exit

```
docker compose down
```

test

```
curl localhost:5001/hello
curl localhost:5001/
# return 404 html
```

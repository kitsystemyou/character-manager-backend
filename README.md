# character-manager

## API Documentation
https://kitsystemyou.github.io/character-manager-backend/dist/#/

## NEED
Pipenv

## getting start
DB

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
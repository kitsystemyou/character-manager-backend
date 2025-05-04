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
cd ./app
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

create character sample

```
curl "https://5000-kitsystemyo-characterma-ewvu0d1ycf7.ws-us118.gitpod.io/character_all_info" \
  -H "accept: application/json, text/plain, */*" \
  -H "accept-language: ja,en-US;q=0.9,en;q=0.8" \
  -H "cache-control: no-cache" \
  -H "content-type: application/json" \
  -H "origin: http://localhost:3000" \
  -H "referer: http://localhost:3000/" \
  -H "sec-ch-ua: \"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"" \
  -H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36" \
  --data-raw "{\"character\":{\"user_id\":\"11561c1d-bd82-4cd9-91c1-8b3119aeef5c\",\"game_system\":\"coc\",\"character_name\":\"character\",\"player_name\":\"player\",\"tags\":\"tags\",\"prof_img_path\":\"\",\"coc_meta_info\":{\"job\":\"job\",\"home_place\":\"america\",\"sex\":\"male\",\"age\":\"100\",\"edu_background\":\"\",\"mental_disorder\":\"ptsd\",\"height\":\"170\",\"weight\":\"60\",\"hair_color\":\"red\",\"eye_color\":\"red\",\"skin_color\":\"dark\",\"memo\":\"memo\",\"edu_backgroud\":\"school\"},\"coc_status_parameters\":{\"str\":10,\"con\":10,\"pow\":10,\"dex\":10,\"app\":10,\"size\":10,\"int\":10,\"edu\":10,\"hp\":20,\"mp\":10,\"init_san\":50,\"current_san\":50,\"idea\":50,\"knowledge\":50,\"damage_bonus\":\"0\",\"luck\":50,\"max_job_point\":\"\",\"max_concern_point\":\"\"},\"coc_skills\":[{\"id\":1,\"step\":\"あ\",\"skill_name\":\"言いくるめ\",\"init_point\":5,\"job_point\":1,\"concern_point\":0,\"grow\":0,\"other\":0,\"summary\":6,\"init_flag\":false,\"skill_type\":1}]}}"
```

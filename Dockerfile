FROM python:3.9.17-bookworm

WORKDIR /usr/src/app
# ENV FLASK_APP=flaskr
# ENV FLASK_ENV=development
# ENV DB_USER=root
# ENV DB_PASS=pass
# ENV DB_HOST=charamane_test
# ENV DB_PORT=3306
# ENV DB_NAME=charamane

COPY /app/requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
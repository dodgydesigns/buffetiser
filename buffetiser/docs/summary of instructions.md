Buffetiser is a web application for organising and visualisisng a shares portfolio. Each investment is shown in its own tab with the variations in price in the tab header. Click on the header to reveal a graph of the share's price history as well as further summary details.
The bottom panel shows a graph and summary details for the portfolio as a whole.
Buffetiser is written using Python, Django, Django Rest Framework and React+JS for the front end.

![image](https://github.com/user-attachments/assets/c747eb11-02e9-44ca-91fa-0dcdfa8b2320)


docker cp postgres_backup/backup.sql buffetiser_db:/backup.sql
sudo docker exec -it buffetiser_db bash
chmod 644 /backup.sql
su - postgres
psql -U buffetiser -d BUFFETISER_DB -f /backup.sql

run docker-compose with just postgres then exec into it:

CREATE DATABASE buffetiser_db;
psql -U buffetiser -d buffetiser_db - should work

# pg_restore -U buffetiser -d buffetiser_db /backup/your-backup-file.sql

Comment out postgres and run backend part of docker-compose. comment out depends_on. Should build all the migrations.
Exec into django and create superuser: python manage.py createsuperuser


On NAS
su - postgres
psql -c "create database buffetiser_db"
psql -c "CREATE USER buffetiser WITH PASSWORD 'password';"


python manage.py dumpdata buffetiser --indent 2 > buffetiser_fixtures.json

apt-get update && apt-get -y install openssh-client

installed pg on be
apt update && apt install -y postgresql-client
installed vim
apt install vim


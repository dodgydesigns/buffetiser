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


*************************DATABASE BACKUP AND RESTORE******************************
1. sudo exec -it buffetiser_db bash
2. mkdir db_backups, chmod +777 db_backups
3. su - postgres
4. cd db_backups
5. pg_dump -U buffetiser -d BUFFETISER_DB > backup.sql
6. sudo docker cp buffetiser_db:/db_backups/backup.sql volume1/dev/Buffetiser\ DBs/
7. ON LOCAL: dropdb 'buffetiser_db'
8. ON LOCAL: sudo su postgres
9. ON LOCAL: (might not need) createuser buffetiser **
10. ON LOCAL: createdb buffetiser_db                **
11. ** Might have to do in pgadmin
12. ON LOCAL: psql -U buffetiser -d buffetiser_db
13. ON LOCAL: alter user buffetiser with password 'password';
14. ON LOCAL: grant all privileges on database buffetiser_db to user buffetiser;
15. ON LOCAL: exit back to host
16. ON LOCAL: psql -X buffetiser_db < backup.sql
17. ON LOCAL: Django: createsuperuser, migrate
18. 

*************************UPDATE BACKEND AND FRONTEND******************************
1. Change Django setting to use db instead of lo
2. Copy buffetiser to mullsysmedia/dev
3. ssh mullsy@192.168.1.2 -p 2323
4. cd volume1/dev/buffetiser - get to docker-compose file
5. Comment out all in docker-compose except backend
6. Comment out depends on db
7. sudo docker-compose build
8. sudo docker-compose up
9. -------------------------------------------------------------------------------
10. Comment out all in docker-compose except frontend
11. Comment out depends on backend
12. Delete the frontend container, node image
13. npm install react-scripts --save
14.  sudo docker-compose up --build
15.  sudo docker-compose up

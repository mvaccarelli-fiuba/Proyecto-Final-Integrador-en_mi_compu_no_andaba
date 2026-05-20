sudo systemctl start mariadb
sudo mariadb < backend/db/user.sql
sudo mariadb krusty_krab < backend/db/schema.sql 

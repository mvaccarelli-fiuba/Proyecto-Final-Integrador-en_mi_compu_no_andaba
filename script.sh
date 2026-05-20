sudo systemctl start mariadb
sudo mariadb < Backend/db/setup.sql
sudo mariadb krusty_krab < Backend/db/schema.sql 

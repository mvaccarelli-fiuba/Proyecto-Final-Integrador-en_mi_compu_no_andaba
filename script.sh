sudo systemctl start mariadb
sudo mariadb < backend/db/user.sql
sudo mariadb < backend/db/schema.sql

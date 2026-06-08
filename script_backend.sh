sudo systemctl start mariadb
sudo mariadb < backend/db/user.sql
sudo mariadb < backend/db/schema.sql
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install --upgrade pip setuptools wheel
pip install -r backend/requirements.txt
python backend/app.py


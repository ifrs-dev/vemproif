### Deploy
[Source](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04#checking-for-the-gunicorn-socket-file)



Requisitos do sistema
```bash
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl htop git vim
```


Banco de dados
```bash
sudo -u postgres psql
CREATE DATABASE vemproif;
CREATE USER vemproif WITH PASSWORD 'vemproif';
ALTER ROLE vemproif SET client_encoding TO 'utf8';
ALTER ROLE vemproif SET default_transaction_isolation TO 'read committed';
ALTER ROLE vemproif SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE vemproif TO vemproif;
\q
```


Acesso SSH
```bash
ssh-keygen
cat ~/.ssh/id_rsa.pub
```
Adicionar chave em: https://github.com/ifrs-dev/vemproif/settings/keys


Repositório
```bash
sudo mkdir /webapps/
sudo chown ifrs /webapps/
cd /webapps/
git clone git@github.com:ifrs-dev/vemproif.git
cd /webapps/vemproif/
git fetch
git checkout prod
```


Virtualenv
```bash
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
cd /webapps/
virtualenv envvemproif
source /webapps/envvemproif/bin/activate
pip install -r /webapps/vemproif/project/requeriments_prod.txt
```


Database
```bash
cd /webapps/vemproif/
python manage.py makemigrations
python manage.py migrate
```


Test app
```bash
cd /webapps/vemproif/
sudo ufw allow 8000
python manage.py runserver 0.0.0.0:8000
python manage.py createsuperuser
gunicorn --bind 0.0.0.0:8000 project.wsgi
sudo ufw delete allow 8000
deactivate
```



Gunicorn Service File
_sudo vim /etc/systemd/system/vemproif-gunicorn.socket_
```bash
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/vemproif-gunicorn.sock

[Install]
WantedBy=sockets.target
```



Gunicorn Service File
_sudo vim /etc/systemd/system/vemproif-gunicorn.service_
```bash
[Unit]
Description=gunicorn daemon
Requires=vemproif-gunicorn.socket
After=network.target

[Service]
User=ifrs
Group=www-data
WorkingDirectory=/webapps/vemproif/
ExecStart=/webapps/envvemproif/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/vemproif-gunicorn.sock \
          project.wsgi:application

[Install]
WantedBy=multi-user.target
```


Gunicorn Service
```
sudo systemctl start vemproif-gunicorn.socket
sudo systemctl enable vemproif-gunicorn.socket
sudo systemctl status vemproif-gunicorn.socket
file /run/vemproif-gunicorn.sock
sudo journalctl -u vemproif-gunicorn.socket
sudo systemctl status vemproif-gunicorn
curl --unix-socket /run/vemproif-gunicorn.sock localhost
sudo systemctl status gunicorn
sudo journalctl -u gunicorn
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```


NGINX File
_sudo vim /etc/nginx/sites-available/vemproif_
```bash
server {
    listen 80;
    server_name vemproif.ibiruba.ifrs.edu.br;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /webapps/vemproif/project/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```


NGINX Service
```
sudo ln -s /etc/nginx/sites-available/vemproif /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
```


Deploys
```
cd /webapps/
source envvemproif/bin/activate
cd vemproif
git pull
pip install -r vemproif/project/requeriments_prod.txt
./manage migrate
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

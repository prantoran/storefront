# MySQL
## Install deps
### For `mysql.connector.django` engine in settings.py
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
pip install mysql-connector-python
# pip install mysqlclient # Does not work, manage.py runserver crashes
```
## Option 1: Docker

https://medium.com/@m22kats/configuring-docker-mysql-and-datagrip-connection-da0b6b71082f

```bash
docker stop mysqlts; \
docker remove mysqlts; \
docker run --name mysqlts \
    -p 3306:3306/tcp -p 33060:33060/tcp \
    -v ~/ltsmysql-data:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=my-secret-pw \
    mysql:lts
```
### MySQL console
```bash
docker exec -it mysqlts mysql -u root -p
```
### Create a user
```sql
CREATE USER 'pinku'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'pinku'@'%';
```
### Create db
```
CREATE DATABASE storefront;
```

https://medium.com/tech-learn-share/docker-mysql-access-denied-for-user-172-17-0-1-using-password-yes-c5eadad582d3



## Option 2: Install directly 
- Easy to mess up with old installations

https://dev.mysql.com/downloads/mysql/

```bash
sudo service mysql status
```

### Remove
https://www.digitalocean.com/community/questions/completely-uninstall-mysql-server
https://stackoverflow.com/questions/43446218/dpkg-error-processing-package-mysql-server-dependency-problems

### Install
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-22-04


# DB IDE
## DataGrip


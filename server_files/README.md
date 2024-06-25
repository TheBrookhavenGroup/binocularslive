This whole server_files dir structure does not do anything.
It is just reference material for setting up the server.

***

# Setting up an Ubuntu Server for Django

Great Reference: [How to Setup Django](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)

Nearly all of this should work for any Ubuntu server.

We'll use Nginx, Gunicorn, and Django.

Notes: 
1. Angle brackets indicate where you need to use an appropriate value.  i.e. `<ip address>`, or `<domain name>` should be replaced with your ip address or domain name.
2. As an example I'll use our binocularslive project so you may see 
   binoculars.live or binocularslive for a database name in this doc.  Replace 
   that with your domain or project.
3. **DO NOT USE** binocularslive anywhere on your server. 


## Get an Ubuntu Server
An obvious first step.

- Allocate a Basic 1G/25G Ubuntu Server.
   
- Set the DNS A record for your domain or subdomain for that server. 

  I use http://namecheap.com for domain registaration and DNS services.  
  Other popular choices are http://godaddy.com or http://aws.com.
  
  ```
  A @ <your droplet ip address>
  ```

  Obviously replace <ip address> with the ip address for your droplet.  
  Note, this is a DNS record change and could take hours or even days before it works.

  You may want other servers as subdomains.  
  I like to have a second staging server/droplet, so I added this A record as well:

  ```
  A staging <your staging droplet ip address>
  ```

  This second staging DNS record use the ip address for my Digital Ocean staging droplet.


- login as root
  ```
  # ssh root@staging.commonologygame.com
  # apt update
  # apt upgrade
  ```
- You may want to add your development platform public ssh key to the droplets root account 
  `.ssh/authorized_keys` file so you don't need a password to login.
- Install your favorite editor.
  ```
  # apt install emacs
  ```
- [set hostname](https://www.digitalocean.com/community/questions/how-do-i-change-hostname)

  ```
  # hostnamectl set-hostname staging.commonologygame.com
  ```
  
  Edit `/etc/hosts` and add your domain name to the right of localhost:

  ```
  127.0.0.1 localhost staging.commonologygame.com
  ```
  
  Change `preserve_hostname` in `/etc/cloud/cloud.cfg` is set to true.

  Now execute hostnamectl to finish up:

     ```
     # hostnamectl
     # reboot
     ```

  Log back in with:
  `# ssh root@staging.commonologygame.com`
  
  You should have a nice prompt stating domain name of your server as the prompt.  It may just state the subdomain.
  You can always, safely, use `$ hostname` to see the fully qualified domain name (FQDN).


## ufw (Uncomplicated Firewall)

```
# ufw default deny incoming
# ufw default allow outgoing
# ufw allow ssh
# ufw allow OpenSSH
# ufw enable
```

## Install Software

At this point you can copy the contents of `packages.txt` and add them to a new file in your root directory. You will need to copy them from your local directory, as the git repo is not yet available on the server.

From your local terminal:
```
  $ scp packages.txt root@staging.commonologygame.com:~/
```
 
```
  # apt update -y
  # xargs -a /root/packages.txt sudo apt-get install
  # cd /usr/bin
  # ln -s pip3 pip
  # ufw allow "Nginx Full"
  # ufw status
  ```
The output of that status should look like this:

```
$ sudo ufw status
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere                  
OpenSSH                    ALLOW       Anywhere                  
Nginx Full                 ALLOW       Anywhere                  
22/tcp (v6)                ALLOW       Anywhere (v6)             
OpenSSH (v6)               ALLOW       Anywhere (v6)             
Nginx Full (v6)            ALLOW       Anywhere (v6)             

q@staging:~$ 
```

You can visit the server with your browser now to see that it is running Nginx. 
Just put http://staging.commonologygame.com in our browser.  You should see a "Welcome to nginx!" page.
Don't worry yet that it isn't secure.  We'll get an ssl certificate soon to secure it.

## Create user django.

  ```
  $ adduser django
  ```

  Enable django to as sudo user, allow django to run commands as superuser using sudo.

  Add this line to the end of `/etc/sudoers`. You'll have to temporarily change the permissions with 
  `chmod +w /etc/sudoers` and then after editing change it back with `chmod -w /etc/sudoers`.

  `django ALL=(ALL) NOPASSWD:ALL`

  You may want to put your public ssh key in `/home/django/.ssh/authorized_keys` so you can login without a password.

  Now you can logout as root and login again:

  `ssh django@staging.commonologygame.com`

  This way you can organize your project in the q user account and use git commands etc.  
  But if you need to do some superuser operations you have permission.

## Set up pyenv

Reference: [pyenv-installer](https://github.com/pyenv/pyenv-installer)

```
  $ curl https://pyenv.run | bash
```

That command will give you a few lines to add to `/home/django/.bashrc` do that.
See the end of the `staging.bashrc` file in this repo.
Then logout and log back in again.  It could take a long time, 5-10 minutes, for the `pyenv install` line.

```
  $ pyenv install 3.9.4
  $ pyenv shell 3.9.4
  $ pyenv virtualenv project
```


## Make ssh keys

  You'll need a set of ssh keys for github and maybe other things described later.

  ```
  $ ssh-keygen
  ```

  The public key file is `/home/django/.ssh/id_rsa.pub`.
  Copy the contents of your public key for this server to the quizitiveprod github acccount.

That should create `/home/django/.ssh/id_rsa_.pub`, a public key. 


## git clone

Clone your git project in the django account on the server.

```
$ cd
$ git clone git@github.com:quizitive/commonology.git
$ pyenv shell project
$ cd commonology
$ pip install -r requirements
$ python manage.py collectstatic --noinput
```

Note: you will need to make sure your project settings.py file has the appropriate files for ALLOWED_HOSTS.


## Environment Variables

Environment Variables are in `/etc/profile.d/django_project.sh`.
That file may contain secrets and so it is not in the repo.

That file would define the `DJANGO_SECRET` value used in your Django settings.py file.

Add this to the end of `/home/django/.bashrc`.

```shell
export PATH="/home/django/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

set -a
source /etc/profile.d/django_project.sh
set +a
```

## Postgres

 
### Create a database:

  ```
  $ sudo -u postgres psql
  
  postgres=# CREATE DATABASE commonology;
  postgres=# CREATE USER postgres with password 'postgres';
  postgres=# ALTER ROLE postgres SET client_encoding TO 'utf8';
  postgres=# ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
  postgres=# ALTER ROLE postgres SET timezone TO 'UTC';
  postgres=# GRANT ALL PRIVILEGES ON DATABASE commonology TO postgres;
  postgres=# alter user postgres PASSWORD 'postgres';
  postgres=# alter user postgres createdb;
  postgres=# 
  postgres=# \q
  ```

### Copy production database to staging server (optional).
  You may want to do this if you are building a staging server.

  Add your public ssh key, `/home/django/.ssh/id_rsa_.pub`, to your production server `/home/django/.ssh/authorized_keys` file.

  Now you can use `rsync -avz -e ssh django@commonologygame.com:~/pg_dumps ~/` to copy over postgres dump files.

  You can load the dump into postgres like this:
  ```
  $ cd
  $ sudo -u postgres pg_restore --verbose --clean --no-acl -d commonology -h 127.0.0.1 ~/pg_dumps/commonology_Mon.tar 
  ```

## Redis

This was installed earlier when Ubuntu packages were installed.  There 
shouldn't  be anything else to do.  You may have to add user ubuntu to the 
redis group in /etc/group.

## Celery
systemd files for celery

```
$ sudo su -
# cp /home/django/commonology/server_files/etc/systemd/system/celery.service /etc/systemd/system/
# cp /home/django/commonology/server_files/etc/systemd/system/celeryserial.service /etc/systemd/system/
# mkdir /etc/conf.d
# cp /home/django/commonology/server_files/etc/conf.d/celery /etc/conf.d/
# cp /home/django/commonology/server_files/etc/tmpfiles.d/celery.conf /etc/tmpfiles.d/ 
# systemctl enable celery
# systemctl enable celeryserial
# sudo systemctl daemon-reload
# mkdir /var/log/celery
# chown ubuntu:ubuntu /var/log/celery
# mkdir /var/run/celery
# chown ubuntu:ubuntu /var/run/celery
# sudo systemctl restart celery
# sudo systemctl restart celeryserial
```

Note: you can use wildcards with systemctl like this `sudo systemctl restart 'celery*'`.

## GUnicorn

```shell
$ sudo su -
# cd /etc/systemd/system/
# cp /home/ubuntu/binocularslive/server_files/etc/systemd/system/gunicorn.
service ./
# sudo systemctl daemon-reload
# systemctl start gunicorn
# systemctl enable gunicorn
# exit
$ cd
$ cd binocularslive
$ ls
```

At this point you should see the `binocularslive.sock` file in the ls listing.

## Get https certificates

We'll use [letsencrypt](http://letsencrypt.org)
because it is free and works well.

Reference: [certbot install directions](https://certbot.eff.org/lets-encrypt/ubuntufocal-nginx)

Before we start we need to make sure the server is answering for our domain.
Make sure to start nginx with default values.  Later we'll change them for Django.

```shell
$ sudo su 
# ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/
# systemctl restart nginx
```


Install and run letsencrypt certbot:

```shell
$ sudo snap install core
$ sudo snap refresh core
$ sudo apt update
$ sudo snap install --classic certbot
$ sudo certbot certonly --nginx
```

For some reason this command sometimes adds the appropriate references to
the end of each config file in `/etc/nginx/sites-available/`.  I copied the records
from the ones in our repo.  We should not have to do this.

## Nginx

Copy site config files from repo.

```shell
$ sudo su
# cp /home/ubuntu/binocularslive/server_files/etc/nginx/sites-available
/binocularslive.nginx /etc/nginx/sites-available/
# ln -s /etc/nginx/sites-available/binocularslive.nginx /etc/nginx/sites-enabled/
# rm /etc/nginx/sites-enabled/default
```

```shell
# systemctl restart nginx
# systemctl restart gunicorn.service 
```

### Nginx-ulitimate-bad-bot-blocker

Ref: `https://github.com/mitchellkrogza/nginx-ultimate-bad-bot-blocker`

This uses databases that are frequently updated to block traffic from known bad actors.

```commandline
$ sudo su -
# wget https://raw.githubusercontent.com/mitchellkrogza/nginx-ultimate-bad-bot-blocker/master/install-ngxblocker -O /usr/local/sbin/install-ngxblocker
# cd /usr/local/sbin
# chmod +x install-ngxblocker
# ./install-ngxblocker
# ./install-ngxblocker -x
# chmod +x setup-ngxblocker
# chmod +x update-ngxblocker
# ./setup-ngxblocker -x -e nginx
# nginx -t
# nginx -s reload
# service nginx reload
# service nginx restart
```

Note: used `-e nginx` arg with `setup-ngxblocker` because that is the extension we use on our nginx config files.

Add this line to the crontab:

`13 22 * * * root /usr/local/sbin/update-ngxblocker -e ms@quizitive.com`

Try tests suggested at the end of hte github home page.


## Add a few houskeeping items to /etc/crontab

### Crontab

These three lines should be added to /etc/crontab.  That file is in the repo.

```shell
0 21 * * * django /home/ubuntu/binocularslive/scripts/pg_backup.bash
55 15 * * * root /usr/bin/certbot renew --renew-hook 'service nginx reload'
```

Sometimes certbot is installed in `/snap/bin` so you may need to do this:
```shell
$ sudo su -
# cd /usr/bin
# ln -s /snap/bin/certbot
```

It is not necessary to have `pg_backup.bash` run on a staging server.

### pg_dumps

Need a pg_dumps dir for the cron'd `pg_backup.bash` script.

```shell
$ mkdir /home/ubuntu/pg_dumps/
```

### redis_dumps

Redis seems to dump automatically and frequently.  So, backing
it up just means copying the dump file.

```shell
scp ubuntu@binoculars.live:/var/lib/redis/dump.rdb ~/Documents/dev/commonology/redis_dumps
```

# Try it!


## Upgrade Notes
[Upgrade Notes](server_files/upgrade.md)
# Rivnet
Rivnet is a multiple gateway proxy system to use in parrallel with https://github.com/gnikwo/Rivnet_client

##Installation

```bash
git clone https://github.com/gnikwo/Rivnet
cd Rivnet
virtualenv --python=python3 env
source env/bin/activate
pip install django
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
```

You have to edit core/settings.py and Changing "Server" by your server name.
It must match the name you will gave to the server instance you will then create on the manager.


##Run

```bash
source env/bin/activate
./manage.py runserver 0.0.0.0:8000
```

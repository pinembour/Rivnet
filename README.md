# Rivnet
Rivnet is a multiple gateway proxy system to use in parrallel with https://github.com/pinembour/Rivnet_client

## Installation

```bash
git clone https://github.com/pinembour/Rivnet
cd Rivnet
virtualenv --python=python3 env
source env/bin/activate
pip install django
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
```

## Configuration

First edit ```core/settings.py``` and input your server name.
It must match the name of the server instance you will create on the manager.

```python
#Input your server name here, it has to match the name of the server instance you will create on the manager
server_name=""
```

Then edit ```rivnet/settings.py```

+ Input your own secret key
+ Set debug to false
+ Add all the allowed hosts you need, for example ```127.0.0.0.1``` or ```domain.local```


## Run

```bash
source env/bin/activate
./manage.py runserver 0.0.0.0:8000
```

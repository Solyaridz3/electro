# Electro
E-commerce Website written in Django.
[You can check it here](https://electro-webstore.herokuapp.com/) (May take a few seconds to load because the server has been inactive)

#### Setup

1. install python-3.10.2
2. setup env variables 

#### Run that in terminal

```bash
pip install -r /path/to/requirements.txt
```

```bash
python manage.py runserver
```

#### Authentication

- CustomUserManager that inherits from BaseUserManager with that realized authentication with email.
- In other authentication is defoult for django.

#### DB
- During development used sqlite3
- For publishing on Heroku used PostgreSQL

#### Uploading files
- Used Cloudinary storage for uploading files on server



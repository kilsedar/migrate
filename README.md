# MIGRATE - MIGRation pATterns in Europe

MIGRATE - MIGRation pATterns in Europe is a Web mapping application aimed at educating and raising awareness about the phenomenon of migration in Europe. This goal is achieved using a gamification approach, i.e. users interact with the application by playing a map-based game, where questions are asked, and answers are provided and explained, about a number of topics related to migration. According to their answers, users are awarded with points and badges, and are ranked into a publicly available ranking which allows to keep them motivated in further using the application. Users' answers will help to understand the current knowledge and perception of migration-related issues.

The game can be found at http://geomobile.como.polimi.it/migrate.


## Requirements

For replicating the game on your own server you will need:

1. Python 2.7
2. Django 1.9
3. PostgreSQL 9.3

Clone this repository:
```
#!python

git clone https://bitbucket.org/kilsedar/migrate
```

Install psycopg2, using linux:
```
#!python

sudo apt-get install python-psycopg2
```

Using pip:
```
#!python

pip install psycopg2
pip install pycrypto
```

Change the file migrate/settings.py to your server's details and from the root directory of the application run:
```
#!python

python manage.py migrate
```

This will create the necessary tables for the game, then to populate them:
```
#!python

python manage.py loaddata fixtures/questionnaire6.json
python manage.py loaddata fixtures/country.json
```

To start your server in test mode:
```
#!python

python manage.py runserver
```

You should then be able to access and use the application at http://localhost:8000/

To create a superuser run:
```
#!python

python manage.py createsuperuser
```

With this you'll be able to login to:
```
#!python

http://localhost:8080/admin/
```

From this panel you can consult and modify all the records of the application and give/remove permissions.

To set up a production server follow the instructions at https://docs.djangoproject.com/en/1.10/howto/deployment/


## Credits

This application was developed under the MYGEOSS Third Call For Innovative Apps in the environmental and social domains project. The team can be found at http://geomobile.como.polimi.it/migrate/team.


## License

The data used to create the questions for the trivia game was collected from open sources listed in the section [data](Link http://geomobile.como.polimi.it/migrate/data/) of the application.
The tools used during the development were Free and Open Source Software (FOSS) complying to the directions of the GEOSS Data-CORE.
If you wish to modify the project or clone the app, you need to provide proper credits to this repository and keep the modified project open as well. This code is under the EU Public License (EUPL).
This will allow further development of the applications in the future, even for commercial purposes, as long as the original source code remains open.

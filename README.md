# docker-mjerapp

django python docker postgresql

How to startup docker mjer-app
* Docker start up
    * docker-mjerapp_devcontainer
        * docker-mjerapp_devcontainer_web_1
        * docker-mjerapp_devcontainer_pgadmin4_1
        * docker-mjerapp_devcontainer_db_1
* Django start up
    * cd project/mjerapp
    * cd socoringsheets
    * export DJANGO_SETTINGS_MODULE=scoringsheets.settings.dev
    * python manage.py runserver
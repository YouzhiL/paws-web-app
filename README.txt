Paws.com Version 1.00

## Authors
Youzhi Liang, Tong Lin, Xinran Song, Eva Gao


## Installation

1. Download CODE.zip.

2. Create a new database named ‘pawsApp’ on pgAdmin.

3. Find settings.py file in ‘paws_ltd’ folder and change ‘USER’ and ‘PASSWORD’ to your own. The default database tool is postgresql. You are free to change it to any database tool, but please remember to follow the instructions on https://docs.djangoproject.com/en/4.0/topics/db/multi-db/. 

4. If you decide to use postgresql, you can directly navigate to the directory ‘paws_ltd’, run ‘python manage.py makemigrations’ and ‘python manage.py migrate’ to transfer any changes to the database created in postgresql. 

5. Find import_data.py file in the ‘scripts’ folder and change each directory to where the ‘data’ folder exists. Then navigate to the ‘paws-web-app’ folder. Run ‘python manage.py runscript import_data’ to load the data into django models. 

6. Note if you run into 'AssertionError: database connection isn't set to UTC' error, it's lastest psycopg2 causing this. You can either run 'pip install psycopg2==2.8.6' or 'pip install psycopg2-binary==2.8.6'.

6. Import the data into the database created in postgresqL by running ‘python manage.py makemigrations’ and ‘python manage.py migrate’.

7. Remain in the ‘paws-web-app’ directory, and run ‘python manage.py runserver’ in the terminal to run the server for the website (currently at local port). Add URL suffix (such as accounts/signup/)  to the URL and open it in the browser. The showing interface will be the signup page.


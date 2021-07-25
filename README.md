# FaBackend Assignment | FamPaympay


### TechStack Used
1. Python (Programming Language)
2. Django (Web Framework)
3. SQLite (Database)


### How to setup and run locally
  1. Clone the Repository.
  2. Redirect to project base directory.
  3. Run the following command for installing dependencies.

    $ pip install -r requirements.txt

  4. Now before running the server, we have to setup database, so run.
 
    $ python3 manage.py migrate

  5. Now execute the following commands in separate terminal/ command line
  
    $ python manage.py process_tasks
    $ python manage.py runserver


Notes:
- Please wait for the background task to fetch the data and store that data in db.
- After running the server url to get all vides will be : http://localhost:8000/api/videos/
- After running the server url to get searched videos will be : http://localhost:8000/api/search/?search_term=goals

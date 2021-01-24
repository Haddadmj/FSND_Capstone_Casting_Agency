# FSND_Capstone_Casting_Agency
Fullstack Nanodegree Final Project - Casting Agency

# Casting Agency
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

No frontend developed yet, only server side.

Application hosted on Heroku 

https://vast-stream-21858.herokuapp.com/

## Working with the application locally
Make sure you have [python 3](https://www.python.org/downloads/) or later installed

1. **Clone The Repo**
    ```bash
    git clone https://github.com/Haddadmj/FSND_Capstone_Casting_Agency
    ```
2. **Set up a virtual environment**:
    ```bash
    virtualenv env
    source env/Scripts/activate # for Windows
    source env/bin/activate # for MacOs/Linux
    ```
3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt # for Windows/Linux
    pip3 install -r requirements.txt # for MacOs
    ```
4. **Export Environment Variables**

    Refer to the `setup.sh` file and export the environment variables for the project.

5. **Create Local Database**:

    Create a local database and export the database URI as an environment variable with the key `DATABASE_URL`.

6. **Run Database Migrations**:
    ```bash
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    ```

7. **Run the Flask Application locally**:
    ```bash
    export FLASK_APP=app
    export FLASK_ENV=development
    flask run
    ```

## Testing
To run the tests, run
```bash
dropdb capstone
createdb capstone
python test_app.py # if running locally
```

## API Reference

### Getting Started

* Base URL: Currently this application is only hosted locally. The backend is hosted at `https://vast-stream-21858.herokuapp.com/`
* Authentication: This application use Auth0 service

* Use this link to get new token [Get Token](https://fsnd-udacity.eu.auth0.com/authorize?audience=CastingAgency&response_type=token&client_id=WMvUqnD1GAJg2OH06i4Musq0vllhysMh&redirect_uri=https://localhost:8080/login-results)

Users in this application are:

* Assistant : Can view actors and movies
    * Email: AssistantTest@gmail.com
    * Password: Test1234
* Director : Assistant Access + CURD on actors + Modify movies
    * Email: DirectorTest@gmail.com
    * Password: Test1234
* Executive: Full Access
    * Email: ExecutiveTest@gmail.com
    * Password: Test1234

### Error Handling

Errors are returned as JSON in the following format:<br>

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

The API will return three types of errors:

* 404 – resource not found
* 422 – unprocessable
* 401 - Unauthorized

### Endpoints

#### GET /actors

* General: Return list of actors in Database
* Sample: `curl -L -X GET 'vast-stream-21858.herokuapp.com/actors' \
-H 'Authorization: Bearer Assisant_Token'`<br>

        {
            "actors": [
                {
                    "age": 25,
                    "gender": "male",
                    "id": 3,
                    "name": "mohammad"
                }
            ],
            "success": true
        }

#### GET /movies

* General: Return list of movies in Database
* Sample: `curl -L -X GET 'vast-stream-21858.herokuapp.com/movies' \
-H 'Authorization: Bearer Assisant_Token'`<br>

        {
            "movies": [],
            "success": true
        }

#### POST /actors

* General:
    * Create actor using JSON Request Body
    * Return ID of created actor
* Sample: `curl -X POST 'vast-stream-21858.herokuapp.com/actors' \
-H 'Authorization: Bearer Director_Token' \
-H 'Content-Type: application/json' \
--data-raw '{
    "name":"mohammad",
    "age":15,
    "gender":"male"
}'`

        {
            "created_id": 4,
            "success": true
        }

#### POST /movies

* General:
    * Create movie using JSON Request Body
    * Return ID of created movie
* Sample: `curl -X POST 'vast-stream-21858.herokuapp.com/movies' \
-H 'Authorization: Bearer Executive_Token' \
-H 'Content-Type: application/json' \
--data-raw '{
    "title":"The Mud",
    "release_date" : "10-10-2016"
}'`

        {
            "created_id": 2,
            "success": true
        }

#### PATCH /actors/<actor_id>

* General:
    * Modify actor given id in URL provided the information to update
* Sample: `curl -X PATCH 'vast-stream-21858.herokuapp.com/actors/3' \
-H 'Authorization: Bearer Director_Token' \
-H 'Content-Type: application/json' \
--data-raw '{
    "name" : "mohammad",
    "age" : 25
}'`

        {
            "actor": {
                "age": 25,
                "gender": "male",
                "id": 3,
                "name": "mohammad"
            },
            "success": true
        }
#### PATCH /movies/<movie_id>

* General:
    * Modify movie given id in URL provided the information to update
* Sample: `curl -X PATCH 'vast-stream-21858.herokuapp.com/movies/2' \
-H 'Authorization: Bearer Director_Token' \
-H 'Content-Type: application/json' \
--data-raw '{
    "title":"Terminator",
    "release_date":"10/19/2019"
}'`

#### DELETE /actors/<actor_id>

* General: Delete an actor given id in URL
* Sample: `curl -X DELETE 'vast-stream-21858.herokuapp.com/actors/3' \
-H 'Authorization: Bearer Executive_Token'`

        {
            "deleted_id": 3,
            "success": true
        }

#### DELETE /movies/<movie_id>

* General: Delete movie given id in URL
* Sample: `curl -X DELETE 'vast-stream-21858.herokuapp.com/actors/2' \
-H 'Authorization: Bearer Executive_Token'`

        {
            "deleted_id": 2,
            "success": true
        }

#### Postman user
in this repo there is collection file exported with latest postman version

you can use it to test all API Provided in here

PS: Update Tokens For Folders in the collection
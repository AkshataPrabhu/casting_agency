# Casting Agency
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. 

## Models implemented:

- Movies 
  - Title 
  - Release date
- Actors 
  - Name
  - Age
  - Gender
## Endpoints:
- `GET` /actors and /movies
- `DELETE` /actors/ and /movies/
- `POST` /actors and /movies 
- `PATCH` /actors/ and /movies/
## Roles :

### Casting Assistant 
- Can view actors and movies

### Casting Director
- All permissions a Casting Assistant has and 
- Add or delete an actor from the database
- Modify actors or movies

### Executive Producer
- All permissions a Casting Director has and 
- Add or delete a movie from the database

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies


```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. 

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb casting_agency
```

## Running the server

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```


## API Reference

### Getting Started 
- Base URL: `https://akshata-casting-agency.onrender.com`
- 
### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /movies
- General:
   -  Fetches a dictionary of movies
   - Request Arguments: None
   - Returns: list of movies
- Sample: `curl https://akshata-casting-agency.onrender.com/movies`

``` {
  {
      "movies": {
            {
              "id":1,
              "title":"Movie Name",
              "release_date": "2020-10-10"
            }
       }, 
      "success": true
  }
```
#### GET /actors
- General:
   -  Fetches a dictionary of actors
   - Request Arguments: None
- Sample: `curl https://akshata-casting-agency.onrender.com/actors`

``` {
  {
      "actors": {
            {
              "id":1,
              "name":"John",
              "age": 32,
              "gender": "male"
            }
       }, 
      "success": true
  }

```


#### DELETE /actor/{id}

- General 
  - Deletes a specified actor using the id of the actor
  - Request Arguments: id - integer
  - Returns: returns the deleted actor id along with status code.
- Sample: `curl -X DELETE https://akshata-casting-agency.onrender.com/questions/16`
- Response Sample
```
{
  "deleted": 40, 
  "success": "True"
}

```
#### DELETE /movie/{id}

- General 
  - Deletes a specified movie using the id of the movie
  - Request Arguments: id - integer
  - Returns: returns the deleted movie id along with status code.
- Sample: `curl -X DELETE https://akshata-casting-agency.onrender.com/movie/16`
- Response Sample
```
{
  "deleted": 41, 
  "success": "True"
}
```

#### POST /actor
- General
  - Sends a post request to create a new actor
  - Returns: id of the newly created actor
- Sample `curl https://akshata-casting-agency.onrender.com/actor -X POST -H "Content-Type: application/json" -d '{"name":"John","age":32, "gender":"male"}'`
- Response sample
```
{
  "created": 10
  "success": true
}

```
#### POST /movie
- General
  - Sends a post request to create a new movie
  - Returns: id of the newly created actor
- Sample `curl https://akshata-casting-agency.onrender.com/actor -X POST -H "Content-Type: application/json" -d '{"title": "Titanic",release_date":"2020-1-1"}'`
- Response sample
```
{
  "created": 10
  "success": true
}

```

#### PATCH /actor/{id}
- General
  - Sends a patch request to update an actor
  - Returns: id of the updated  actor
- Sample `curl https://akshata-casting-agency.onrender.com/actor{id} -X PATCH -H "Content-Type: application/json" -d '{"name":"John","age":32, "gender":"male"}'`
- Response sample
```
{
  "updated": 10
  "success": true
}

```
#### PATCH /movie/{id}
- General
  - Sends a post request to update movie 
  - Returns: id of the updated movie
- Sample `curl https://akshata-casting-agency.onrender.com/actor/{id} -X PATCH -H "Content-Type: application/json" -d ''{"title": "Titanic",release_date":"2020-1-1"}'`
- Response sample
```
{
  "created": 10
  "success": true
}

```

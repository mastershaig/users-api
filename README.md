# Coding Test Django Python #
The challenge consists of creating two services: 
- user_birthday
- letter_digit

Conditions:
- Make use of docker and docker-compose
- Make use of unit tests

######1. User Birthday Service
a. Create an API endpoint which accepts a list of JSON objects as POST-payload.
- Store the data in a Postgres Database
- The email address should be unique
- All fields are required

Payload Example:

 ![payload example](https://i.ibb.co/b7VxTXK/Screen-Shot-2021-02-01-at-14-52-56.png)

b. Create an API endpoint which returns a list of objects, filtered by the following parameters (birthday)
- from (example: from=%d%m)
- to (example: to=%d%m)

c. Create an API endpoint which returns the average age of all records in the database. Think about caching.

######2. Letter Digit
Create an API-Endpoint taking a string with letters and digits and returning a list of all possible upper & lowercase variations.
Example: (a2B => [a2b, a2B, A2b, A2B])

###  Run the project   ###

Build and run the Docker images and map the 8050 to host.

```sh
$ docker-compose up --build -d
$ docker-cleanup
```
Now django app is running in production mode.
After postgres is up, run migrations

```sh
$ docker exec -it code_test sh -c "/venv/bin/python manage.py makemigrations --merge --noinput && /venv/bin/python manage.py migrate --noinput"
```

Verify the deployment by navigating to the server address in your preferred browser.

```sh
localhost:8050/api/v1/redoc/
localhost:8050/api/v1/users
```

### Questions? ###

Ask me any questions by writing to khaligli@hotmail.com
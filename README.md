# e_university_api


## Development

1. Create in the project root (or obtain from team member) an `.env` file with environment variables required by application.
   Refer `local/example.env` for example. You can copy it and edit during local development:

       cp local/example.env .env

2. Copy `local/docker-compose.example.yml` to the project root:

       cp local/docker-compose.example.yml ./docker-compose.yml

   Feel free to modify it for personal use (e. g. change ports, add more services).

### Local run in docker container using docker-compose

1. Ensure `.env` file has at least `POSTGRES_USER`, `POSTGRES_PASSWORD` and `POSTGRES_DB` variables
   set to any string values.

2. Run _postgres_ and _backend_ in docker containers:

       docker-compose up  # run all services defined in docker-compose file

   > :warning: If you see an error messages about failing to connect database, try running database *first*:
   >
   >     docker-compose up postgres  # wait several seconds until database is up
   >     docker-compose up backend  # in separate terminal

3. Open <http://localhost:8000> to access API (port is specified in docker-compose file).
   Open <http://localhost:8000/docs> to access docs.

### Local run on host system

During development it may be useful to run application outside of docker container (e. g. for debugging). To perform this:

1. Install Python 3.8 (refer `pyproject.toml` for python verion used on the project) and [Poetry](https://python-poetry.org/)

2. Create virtual environment and install project dependencies:

       poetry install

3. Run database in docker container using docker-compose:

       docker-compose up postgres

   Now database is accessible via localhost:5432.

4. Ensure that `.env` file has `POSTGRES_HOST=localhost` and `POSTGRES_PORT=5432`.

   Run application (one-liner):

       poetry run uvicorn apps.main:app --port 8778

   or

       poetry shell  # activate virtual environment; spawns a subshell
       uvicorn apps.main:app --port 8778

   Now API must be accessible at <http:/localhost:8778> and docs at <http:/localhost:8778/docs>

<br>

<h4>Working with dependency(library) groups</h4>
If you need to work with specific dependency group - change in `poetry.toml` group 'optional' status from `True` to `False`.

**EXAMPLE**<br> You're working with testing, and connect dependency group to project, so you need to change here `optional = true` to `optional = false`:<br>
```
[tool.poetry.group.test]
optional = false
```


### Setup database

For work with application, you need to setup your database in docker container. To perform this:

1. While postgres docker container is running, enter it (use separate terminal):

       docker exec -it e_university_api-postgres bash

2. Enter inside psql terminal (inside your container):

       psql -U postgres

3. Create database for use it in our application and use it (inside psql terminal):

       CREATE DATABASE e_university;
       \c e_university;

4. Copy content of 1) migrations/main.sql and 2) migrations/data.sql one after another and paste it in previously opened psql terminal.
   Check that migrations applied successfully.

5. Change in .env file in root directory value of POSTGRES_DB on e_university

6. Rebuild docker and up it, use commands:

       docker-compose build --no-cache
       docker-compose up

### Sending mail configurations

1. For sending messages use email_manager.

2. Due to possibility of using different smtp services it can be chosen any of that available.

3. As an example it can be mailtrap.io. Create an account and in 'Email Testing' section
   choose "Add project" and "Add inbox" buttons. After creating 'Inbox' click it and in
   'Integrations' field choose Python/Django env settings, fill with that values corresponding
   places in .env file. These values are (with examples):

      
      MAIL_USERNAME = 8f2d4fcedddb
      MAIL_PASSWORD = 6bab9ee9d83c
      MAIL_FROM = noreply@gmail.com
      MAIL_PORT = 2525
      MAIL_SERVER = smtp.mailtrap.io
      MAIL_FROM_NAME = admin

5. Calling send_email_async with appropriate arguments will send test message to the mailtrap 
   service in testing mode, without forwarding it due to the specified email in message.

6. Final configuration can be done later before project deploying.


## Project layout

- main.py: FastAPI app definition
- local/: files that may be useful for local development; not used by app

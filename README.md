# e_university_api

## Local run using docker-compose

1. Create (or obtain) an .env file with environment variables required by application.
   Refer `local/example.env` for example. At least `POSTGRES_USER`, `POSTGRES_PASSWORD`
   and `POSTGRES_DB` are required to successfully run app + database.

2. Copy `local/docker-compose.example.yml` to the project root. Feel free to modify it for personal use.

       cp local/docker-compose.example.yml ./docker-compose.yml

3. Run backend in docker container:

       docker-compose up backend  # also automatically run database service as dependency

   or (shorter)

       docker-compose up  # run all services defined in docker-compose file

4. Open <http://localhost:8000> to access API (port is specified in docker-compose file).
   Open <http://localhost:8000/docs> to access docs.

## Local run on host system

During development it may be useful to run application outside of docker container (e. g. for debugging). To perform this:

1. Create python virtual environment; install dependencies.
   TODO: complete this section

2. Run database in docker container

       docker-compose up database

3. Enable virtual environment and run uvicorn (or main.py?).
   TODO: complete this section

## Project layout

- main.py: FastAPI app definition
- local/: files that may be useful for local development; not used by app


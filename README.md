# e_university_api

### Local development

1. Get `.env` from team member & copy it to root of cloned project.
2. Start `docker-compose.yml` with this command:
    ```commandline
    docker-compose up --build
    ```
    OR (for newer versions of Docker & Docker compose)
    ```commandline
    docker compose up --build
    ```

3. Run migration `main.sql` script (source should be `db` service from docker-compose).
4. Check API docs started properly: [http://0.0.0.0:8889/docs/](http://0.0.0.0:8889/docs/)

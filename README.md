## Prequesitions

- I'm using Docker containers :)
- Run Docker containers for Postgres and Redis

```bash
docker run --name tdio-postgres -p 54321:5432 -e POSTGRES_USER=taxi -e POSTGRES_DB=taxi -e POSTGRES_PASSWORD=taxi -d postgres
docker run --name tdio-redis -p 6379:6379 -d redis
```

- PS. next time, it will be docker-compose instead of docker-run

## Create virtual env and install requirements

```
python3.9 -m venv env
source venv/bin/activated
pip install -r requirements.txt
```

## Debugging with VSCode

- Please see the config file in /.vscode/launch.task
- You can run debugger django with `Python: Django` config
- Also, you can debug the unit tests with `Django Test` config

![image](https://user-images.githubusercontent.com/40058076/174108506-a9b4a6b5-5443-48ef-b840-126f75e08b3e.png)

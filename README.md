## Prequesitions

- docker-compose

## Build and spin up the containers

```bash
docker-compose up -d --build
```

## Run Cypress with docker run

```
docker run -it -v $PWD:/e2e -w /e2e cypress/included:3.2.0
```

## Debugging with VSCode

- Please see the config file in /.vscode/launch.task
- You can run debugger django with `Python: Django` config
- Also, you can debug the unit tests with `Django Test` config

![image](https://user-images.githubusercontent.com/40058076/174108506-a9b4a6b5-5443-48ef-b840-126f75e08b3e.png)

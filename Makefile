DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
STORAGES_FILE = docker_compose/storages.yaml
APP_CONTAINER = smit-main-app

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: all 
all: 
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: all-down
all-down:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} down

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest

.PHONY: postgres
postgres:
	psql -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U ${POSTGRES_USER} -d ${POSTGRES_DB}

.PHONY: alembic-upgrade
alembic-upgrade:
	${EXEC} ${APP_CONTAINER} alembic upgrade head

# make alembic-revision m="Your migration message here"
.PHONY: alembic-revision
alembic-revision:
	${EXEC} ${APP_CONTAINER} alembic revision --autogenerate -m "$(m)"

.PHONY: alembic-downgrade
alembic-downgrade:	
	${EXEC} ${APP_CONTAINER} alembic downgrade -1

.PHONY: all-restart
all-restart: all-down all
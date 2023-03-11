export USER_HANDLER_IMAGE_NAME := user-handler-image:latest
export USER_HANDLER_CONTAINER_NAME := user-handler-app
export POSTGRES_IMAGE_NAME := postgres-image:latest
export POSTGRES_CONTAINER_NAME := postgres-db

build: user_handler postgres
	@echo "Building images..."


run:
	@echo "Starting platform..."
	@user_handler=${USER_HANDLER_IMAGE_NAME} postgresql=${POSTGRES_IMAGE_NAME} docker-compose -p "RSWW" up


clean:
	@docker image rm ${USER_HANDLER_IMAGE_NAME} ${POSTGRES_IMAGE_NAME} --force

user_handler:
	@echo "Building image for ${USER_HANDLER_CONTAINER_NAME}..."
	@docker build -f ../src/user_handler/Dockerfile -t ${USER_HANDLER_IMAGE_NAME} ../src/user_handler


postgres:
	@echo "Building image for ${POSTGRES_CONTAINER_NAME}..."
	@docker build -f postgresql/Dockerfile -t ${POSTGRES_IMAGE_NAME} postgresql
export USER_HANDLER_IMAGE_NAME := user-handler-image:latest
export USER_HANDLER_CONTAINER_NAME := user-handler-app
export POSTGRES_IMAGE_NAME := postgres-image:latest
export POSTGRES_CONTAINER_NAME := postgres-db
export MONGO_IMAGE_NAME := mongodb-image:latest
export MONGO_CONTAINER_NAME := mongo-db
export RABBIT_IMAGE_NAME := rabbitmq-image:latest
export RABBIT_CONTAINER_NAME := rabbitmq


build: user_handler postgres mongo rabbit
	@echo "Building images..."


run:
	@echo "Starting platform..."
	@USER_HANDLER_IMAGE=${USER_HANDLER_IMAGE_NAME} \
	POSTGRES_IMAGE=${POSTGRES_IMAGE_NAME} \
	MONGO_IMAGE=${MONGO_IMAGE_NAME} \
	RABBIT_IMAGE=${RABBIT_IMAGE_NAME} \
	docker-compose -p "victor-travels" up


clean:
	@docker image rm ${USER_HANDLER_IMAGE_NAME} ${POSTGRES_IMAGE_NAME} ${MONGO_IMAGE_NAME} ${RABBIT_IMAGE_NAME} --force


user_handler:
	@echo "Building image for ${USER_HANDLER_CONTAINER_NAME}..."
	@docker build -f ../src/user_handler/Dockerfile -t ${USER_HANDLER_IMAGE_NAME} ../src/user_handler


postgres:
	@echo "Building image for ${POSTGRES_CONTAINER_NAME}..."
	@docker build -f postgresql/Dockerfile -t ${POSTGRES_IMAGE_NAME} postgresql


mongo:
	@echo "Building image for ${MONGO_CONTAINER_NAME}..."
	@docker build -f mongodb/Dockerfile -t ${MONGO_IMAGE_NAME} mongodb


rabbit:
	@echo "Building image for ${RABBIT_CONTAINER_NAME}..."
	@docker build -f ../src/rabbitmq/Dockerfile -t ${RABBIT_IMAGE_NAME} ../src/rabbitmq

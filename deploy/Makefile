GATEWAY_IMAGE_NAME := gateway-image:latest
GATEWAY_CONTAINER_NAME := gateway-app
POSTGRES_IMAGE_NAME := postgres-image:latest
POSTGRES_CONTAINER_NAME := postgres-db
MONGO_IMAGE_NAME := mongodb-image:latest
MONGO_CONTAINER_NAME := mongo-db
RABBIT_IMAGE_NAME := rabbitmq-image:latest
RABBIT_CONTAINER_NAME := rabbitmq


build: gateway postgres mongo rabbit
	@echo "Building images..."


run:
	@echo "Starting platform..."
	@GATEWAY_IMAGE=${GATEWAY_IMAGE_NAME} \
	POSTGRES_IMAGE=${POSTGRES_IMAGE_NAME} \
	MONGO_IMAGE=${MONGO_IMAGE_NAME} \
	RABBIT_IMAGE=${RABBIT_IMAGE_NAME} \
	docker-compose -p "victor-travels" up


clean:
	@docker image rm ${USER_HANDLER_IMAGE_NAME} ${POSTGRES_IMAGE_NAME} ${MONGO_IMAGE_NAME} ${RABBIT_IMAGE_NAME} --force


gateway:
	@echo "Building image for ${GATEWAY_CONTAINER_NAME}..."
	@docker build -f ../src/gateway/Dockerfile -t ${GATEWAY_IMAGE_NAME} ../src/gateway


postgres:
	@echo "Building image for ${POSTGRES_CONTAINER_NAME}..."
	@docker build -f postgresql/Dockerfile -t ${POSTGRES_IMAGE_NAME} postgresql


mongo:
	@echo "Building image for ${MONGO_CONTAINER_NAME}..."
	@docker build -f mongodb/Dockerfile -t ${MONGO_IMAGE_NAME} mongodb


rabbit:
	@echo "Building image for ${RABBIT_CONTAINER_NAME}..."
	@docker build -f ../src/rabbitmq/Dockerfile -t ${RABBIT_IMAGE_NAME} ../src/rabbitmq

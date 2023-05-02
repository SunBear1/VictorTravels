GATEWAY_IMAGE_NAME := gateway-image:development
GATEWAY_CONTAINER_NAME := gateway-app
POSTGRES_IMAGE_NAME := postgres-image:development
POSTGRES_CONTAINER_NAME := postgres-db
MONGO_IMAGE_NAME := mongodb-image:development
MONGO_CONTAINER_NAME := mongo-db
RABBIT_IMAGE_NAME := rabbitmq-image:development
RABBIT_CONTAINER_NAME := rabbitmq
RESERVATIONS_IMAGE_NAME := reservations-image:development
RESERVATIONS_CONTAINER_NAME := reservations-ms
PURCHASE_IMAGE_NAME := purchase-image:development
PURCHASE_CONTAINER_NAME := purchase-ms
PAYMENT_IMAGE_NAME := payment-image:development
PAYMENT_CONTAINER_NAME := payment-ms
TRIPS_IMAGE_NAME := trips-image:development
TRIPS_CONTAINER_NAME := trips-ms
DATA_INIT_CONTAINER_NAME := data-init
DATA_INIT_IMAGE_NAME := data-init-image:development
HOTEL_IMAGE_NAME :=  hotel-image:development
HOTEL_CONTAINER_NAME := hotel-ms
TRANSPORT_IMAGE_NAME :=  transport-image:development
TRANSPORT_CONTAINER_NAME := transport-ms


build-and-run: build run


build: gateway rabbit reservations purchases payments data-init trips hotels transports clean


run:
	@echo "Starting platform..."
	@GATEWAY_IMAGE=${GATEWAY_IMAGE_NAME} \
	RABBIT_IMAGE=${RABBIT_IMAGE_NAME} \
	RESERVATIONS_IMAGE=${RESERVATIONS_IMAGE_NAME} \
	PURCHASE_IMAGE=${PURCHASE_IMAGE_NAME} \
	PAYMENT_IMAGE=${PAYMENT_IMAGE_NAME} \
	TRIPS_IMAGE=${TRIPS_IMAGE_NAME} \
	DATA_INIT_IMAGE=${DATA_INIT_IMAGE_NAME} \
	HOTEL_IMAGE=${HOTEL_IMAGE_NAME} \
	TRANSPORT_IMAGE=${TRANSPORT_IMAGE_NAME} \
	docker-compose -p "victor-travels" up


clean:
	@docker image rm ${GATEWAY_IMAGE_NAME} ${RABBIT_IMAGE_NAME} ${RESERVATIONS_IMAGE_NAME} ${PURCHASE_IMAGE_NAME} ${PAYMENT_IMAGE_NAME} ${TRIPS_IMAGE_NAME} ${DATA_INIT_IMAGE_NAME} --force
	@echo "Removing stopped containers..."
	@docker container prune -f
	@echo "Removing old images..."
	@if [ -n "$$(docker images -f 'dangling=true' -q)" ]; then \
		docker rmi $$(docker images -f 'dangling=true' -q); \
	fi


delete:
	@docker image rm ${GATEWAY_IMAGE_NAME} ${RABBIT_IMAGE_NAME} ${RESERVATIONS_IMAGE_NAME} ${PURCHASE_IMAGE_NAME} ${PAYMENT_IMAGE_NAME} ${DATA_INIT_IMAGE_NAME} ${HOTEL_IMAGE_NAME} ${TRANSPORT_IMAGE_NAME} --force


gateway:
	@echo "Building image for ${GATEWAY_CONTAINER_NAME}..."
	@docker build -f ../src/gateway/Dockerfile -t ${GATEWAY_IMAGE_NAME} ../src/gateway


rabbit:
	@echo "Building image for ${RABBIT_CONTAINER_NAME}..."
	@docker build -f ../src/rabbitmq/Dockerfile -t ${RABBIT_IMAGE_NAME} ../src/rabbitmq

reservations:
	@echo "Building image for ${RESERVATIONS_CONTAINER_NAME}..."
	@docker build -f ../src/reservations_ms/Dockerfile -t ${RESERVATIONS_IMAGE_NAME} ../src/reservations_ms

purchases:
	@echo "Building image for ${PURCHASE_CONTAINER_NAME}..."
	@docker build -f ../src/purchase_ms/Dockerfile -t ${PURCHASE_IMAGE_NAME} ../src/purchase_ms

payments:
	@echo "Building image for ${PAYMENT_CONTAINER_NAME}..."
	@docker build -f ../src/payment_ms/Dockerfile -t ${PAYMENT_IMAGE_NAME} ../src/payment_ms

trips:
	@echo "Building image for ${TRIPS_CONTAINER_NAME}..."
	@docker build -f ../src/trips_ms/Dockerfile -t ${TRIPS_IMAGE_NAME} ../src/trips_ms

data-init:
	@echo "Building image for ${DATA_INIT_CONTAINER_NAME}..."
	@docker build -f ../src/data_initializer/Dockerfile -t ${DATA_INIT_IMAGE_NAME} ../src/data_initializer

hotels:
	@echo "Building image for ${HOTEL_CONTAINER_NAME}..."
	@docker build -f ../src/hotel_ms/Dockerfile -t ${HOTEL_IMAGE_NAME} ../src/hotel_ms

transports:
	@echo "Building image for ${TRANSPORT_CONTAINER_NAME}..."
	@docker build -f ../src/transport_ms/Dockerfile -t ${TRANSPORT_IMAGE_NAME} ../src/transport_ms

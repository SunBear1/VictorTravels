BASE_PYTHON_IMAGE_NAME := base-python:dev
GATEWAY_IMAGE_NAME := malajski/victor-travels:gateway
GATEWAY_CONTAINER_NAME := gateway-app
POSTGRES_IMAGE_NAME := postgres-image:development
POSTGRES_CONTAINER_NAME := postgres-db
MONGO_IMAGE_NAME := mongodb-image:development
MONGO_CONTAINER_NAME := mongo-db
RABBIT_IMAGE_NAME := malajski/victor-travels:rabbitmq
RABBIT_CONTAINER_NAME := rabbitmq
RESERVATIONS_IMAGE_NAME := malajski/victor-travels:reservations
RESERVATIONS_CONTAINER_NAME := reservations-ms
PURCHASE_IMAGE_NAME := malajski/victor-travels:purchases
PURCHASE_CONTAINER_NAME := purchase-ms
PAYMENT_IMAGE_NAME := malajski/victor-travels:payments
PAYMENT_CONTAINER_NAME := payment-ms
TRIPS_IMAGE_NAME := malajski/victor-travels:trips
TRIPS_CONTAINER_NAME := trips-ms
DATA_INIT_CONTAINER_NAME := data-init
DATA_INIT_IMAGE_NAME := malajski/victor-travels:data-init
HOTEL_IMAGE_NAME := malajski/victor-travels:hotels
HOTEL_CONTAINER_NAME := hotel-ms
TRANSPORT_IMAGE_NAME := malajski/victor-travels:transports
TRANSPORT_CONTAINER_NAME := transport-ms
EVENTHUB_IMAGE_NAME := malajski/victor-travels:eventhub
EVENTHUB_CONTAINER_NAME := event-hub-ms
EVENTHUB_IMAGE_V2_NAME :=  event-hub-v2-image:development
EVENTHUB_CONTAINER_V2_NAME := event-hub-ms-v2
GUI_IMAGE_NAME := malajski/victor-travels:gui
GUI_CONTAINER_NAME := web-gui
EVENT_GENERATOR_IMAGE_NAME := malajski/victor-travels:event-generator
EVENT_GENERATOR_CONTAINER_NAME := event-generator


build-and-run: build run


build: base gui gateway rabbit reservations purchases payments hotels transports event-hub-v2 trips data-init data-generator clean


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
	EVENTHUB_V2_IMAGE=${EVENTHUB_IMAGE_V2_NAME} \
	GUI_IMAGE=${GUI_IMAGE_NAME} \
	EVENT_GENERATOR_IMAGE=${EVENT_GENERATOR_IMAGE_NAME} \
	docker-compose -p "victor-travels" up


clean:
	@echo "Removing stopped containers..."
	@docker container prune -f
	@echo "Removing old images..."
	@if [ -n "$$(docker images -f 'dangling=true' -q)" ]; then \
		docker rmi $$(docker images -f 'dangling=true' -q); \
	fi


delete:
	@docker image rm ${GATEWAY_IMAGE_NAME} ${RABBIT_IMAGE_NAME} ${RESERVATIONS_IMAGE_NAME} ${PURCHASE_IMAGE_NAME} ${PAYMENT_IMAGE_NAME} ${DATA_INIT_IMAGE_NAME} ${HOTEL_IMAGE_NAME} ${TRANSPORT_IMAGE_NAME} ${EVENTHUB_IMAGE_NAME} ${EVENTHUB_IMAGE_V2_NAME} ${GUI_IMAGE_NAME} --force


base:
	@echo "Building base images..."
	@docker build -f ../src/base_images/base-python.dockerfile -t ${BASE_PYTHON_IMAGE_NAME} ../src/base_images

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

event-hub:
	@echo "Building image for ${EVENTHUB_CONTAINER_NAME}..."
	@docker build -f ../src/event_hub_ms/Dockerfile -t ${EVENTHUB_IMAGE_NAME} ../src/event_hub_ms

event-hub-v2:
	@echo "Building image for ${EVENTHUB_CONTAINER_V2_NAME}..."
	@docker build -f ../src/event_hub_ms_v2/Dockerfile -t ${EVENTHUB_IMAGE_V2_NAME} ../src/event_hub_ms_v2

gui:
	@echo "Building image for ${GUI_CONTAINER_NAME}..."
	@docker build -f ../src/gui/Dockerfile -t ${GUI_IMAGE_NAME} ../src/gui

data-generator:
	@echo "Building image for ${EVENT_GENERATOR_CONTAINER_NAME}..."
	@docker build -f ../src/event_generator/Dockerfile -t ${EVENT_GENERATOR_IMAGE_NAME} ../src/event_generator

test:
	@pip3 install pytest pytest-md pytest-emoji starlette fastapi
	@echo "Running component tests..."
	@pytest -v --emoji --md ../tests/api/api-test-report.md ../tests/api/component

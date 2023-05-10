FROM rabbitmq:3.12-rc as build-stage

WORKDIR /rabbitmq_data

RUN apt-get update

RUN apt-get install -y curl

RUN rabbitmq-plugins enable rabbitmq_management

ADD rabbitmq.config /etc/rabbitmq/

ADD definitions.json /etc/rabbitmq/

RUN chown rabbitmq:rabbitmq /etc/rabbitmq/rabbitmq.config /etc/rabbitmq/definitions.json

CMD ["rabbitmq-server"]

EXPOSE 5672 15672

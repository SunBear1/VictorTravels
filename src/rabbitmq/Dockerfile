FROM rabbitmq:3.12-rc as build-stage

WORKDIR /rabbitmq_data

RUN apt-get update

RUN apt-get install -y curl

RUN rabbitmq-plugins enable rabbitmq_management

RUN rabbitmq-plugins enable rabbitmq_federation

RUN rabbitmq-plugins enable rabbitmq_federation_management

RUN rabbitmq-plugins enable rabbitmq_tracing

ADD rabbitmq.config /etc/rabbitmq/

ADD definitions.json /etc/rabbitmq/

RUN chown rabbitmq:rabbitmq /etc/rabbitmq/rabbitmq.config /etc/rabbitmq/definitions.json

CMD ["rabbitmq-server"]

EXPOSE 4369 5671 5672 25672 15671 15672

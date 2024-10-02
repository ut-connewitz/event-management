FROM rabbitmq:3.13-management-alpine

RUN mkdir -p /etc/rabbitmq/conf.d
RUN chown -R rabbitmq:rabbitmq /etc/rabbitmq/conf.d
COPY 20-logging.conf /etc/rabbitmq/conf.d

COPY ./init.sh /init.sh
RUN chmod +x /init.sh
EXPOSE 4369 5671 5672 15671 15672 25672 35672-35682

# Define default command
CMD ["sh", "./init.sh"]

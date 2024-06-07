FROM rabbitmq:3.13-management-alpine

#COPY rabbitmq.config /etc/rabbitmq/
#RUN chmod 777 /etc/rabbitmq/rabbitmq.config
#WORKDIR /var/lib/rabbitmq/
#RUN rabbitmq-plugins enable rabbitmq_management
#RUN rabbitmq-plugins list


# Define environment variables.
ENV RABBITMQ_ADMIN admin
ENV RABBITMQ_ADMIN_PASS admin
ENV RABBITMQ_WORKER worker
ENV RABBITMQ_WORKER_PASS worker
ENV RABBITMQ_PID_FILE /var/lib/rabbitmq/mnesia/rabbitmq

ADD init.sh /init.sh
RUN chmod +x /init.sh
EXPOSE 15672

# Define default command
CMD ["/init.sh"]

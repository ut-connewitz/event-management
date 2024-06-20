#!/bin/sh

# Create Rabbitmq user
( rabbitmqctl wait --timeout 60 $RABBITMQ_PID_FILE ; \
rabbitmqctl add_user $RABBITMQ_ADMIN $RABBITMQ_ADMIN_PASS 2>/dev/null ; \
rabbitmqctl set_user_tags $RABBITMQ_ADMIN administrator ; \
rabbitmqctl set_permissions -p / $RABBITMQ_ADMIN  ".*" ".*" ".*" ; \
echo "*** User '$RABBITMQ_ADMIN' completed. ***" ; \
rabbitmqctl add_user $RABBITMQ_WORKER $RABBITMQ_WORKER_PASS 2>/dev/null ; \
rabbitmqctl set_permissions -p / $RABBITMQ_WORKER  ".*" ".*" ".*" ; \
echo "*** User '$RABBITMQ_WORKER' completed. ***" ; \
echo "*** Log in the WebUI at port 15672 (example: http:/localhost:15672) ***") &

# $@ is used to pass arguments to the rabbitmq-server command.
# For example if you use it like this: docker run -d rabbitmq arg1 arg2,
# it will be as you run in the container rabbitmq-server arg1 arg2
rabbitmq-server $@

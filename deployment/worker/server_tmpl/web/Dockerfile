FROM node:5.0
ARG SERVER_PATH=.
RUN mkdir -p /home/Server
WORKDIR /home/Server
ADD ${SERVER_PATH} /home/Server/
# replace ip:port
ADD replace_addr_in_container.sh /home/Server/replace_addr_in_container.sh

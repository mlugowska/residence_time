FROM nginx

ARG NGINX_CONFIG=nginx.conf

WORKDIR /nginx

RUN rm /etc/nginx/conf.d/*
COPY $NGINX_CONFIG /etc/nginx/conf.d/nginx.conf

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

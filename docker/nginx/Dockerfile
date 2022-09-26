FROM nginx:1.22.0-alpine

COPY ./conf/* /etc/nginx/
COPY ./run.sh /run.sh

ENV APP_HOST=app
ENV APP_PORT=8000

USER root

RUN apk add --no-cache openssl bash
RUN chmod +x /run.sh

VOLUME /static
VOLUME /www

CMD ["/run.sh"]
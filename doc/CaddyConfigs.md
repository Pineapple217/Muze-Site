# Caddy configs

## Caddyfile

```yml
beta.jhdemuze.be {
        reverse_proxy django-gunicorn:8000

        handle_path /static* {
                root * /static
                file_server
        }
}
```

## Compose

Is allemaal vrij standaard. gunicorn moet ook in het proxy-netwerk zitten maar dat is normaal het geval.
Wat specifiek voor de site hier aan is is het volume static.

```yml
networks:
        web:
                external: true
        proxy-network:
                external: true
                name: proxy-network

services:
        caddy:
                image: caddy:2-alpine
                container_name: caddy
                restart: unless-stopped
                environment:
                        - CADDY_INGRESS_NETWORKS=proxy-network
                ports:
                        - "80:80"
                        - "443:443"
                volumes:
                        - ./Caddyfile:/etc/caddy/Caddyfile
                        - ./data:/data
                        - ./config:/config
                        - static:/static
                networks:
                        - web
                        - proxy-network
volumes:
  static:
    external: true
```
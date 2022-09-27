server {
    listen 80;
    server_name ${DOMAIN};

    location /.well-known/acme-challenge/ {
        root /www/;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

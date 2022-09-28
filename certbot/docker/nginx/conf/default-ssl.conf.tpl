upstream django {
    server django_gunicorn:8000;
}

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


server {
    listen 443 ssl;
    server_name ${DOMAIN};

    ssl_certificate     /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;

    include     /etc/nginx/options-ssl-nginx.conf;
    ssl_dhparam /proxy/ssl-dhparams.pem;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    client_max_body_size 2M;
    location / {
        proxy_pass http://django;
        client_max_body_size 2M;
    }

    location /static/ {
        alias /static/;
    }
}
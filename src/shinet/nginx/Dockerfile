FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

COPY cert.pem /etc/nginx/certs/certificate.crt
COPY key.pem /etc/nginx/certs/private.key
COPY secret_word /etc/nginx/certs/secret_word


FROM georgjung/nginx-brotli:latest
COPY dist /usr/share/nginx/html
# COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

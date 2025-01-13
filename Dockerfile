FROM georgjung/nginx-brotli:latest
COPY dist /usr/share/nginx/html
COPY nginx/site.conf /etc/nginx/nginx.conf

FROM georgjung/nginx-brotli:latest
COPY dist /usr/share/nginx/html
RUN mkdir -p /var/run/nginx-cache/jscache
RUN echo "D /var/run/nginx-cache 0755 root root -" > /usr/lib/tmpfiles.d/nginx-cache.conf
COPY nginx/site.conf /etc/nginx/nginx.conf

FROM caddy

COPY dashboard /srv/
COPY dashboard/Caddyfile /etc/caddy/Caddyfile
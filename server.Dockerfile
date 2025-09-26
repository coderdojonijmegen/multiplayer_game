FROM caddy

COPY server /srv/
COPY server/Caddyfile /etc/caddy/Caddyfile
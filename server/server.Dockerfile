FROM python:3.13-slim AS app
ENV TZ=Europe/Amsterdam

COPY src/ /app
COPY requirements.txt /
RUN pip3 install --no-cache-dir -r /requirements.txt

WORKDIR /app

ENTRYPOINT ["/app/server.py"]

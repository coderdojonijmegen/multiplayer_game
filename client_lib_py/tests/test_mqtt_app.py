import logging
from time import sleep

import pytest

from mqtt_app import MqttConfig, MqttApp

loop_cnt = 0

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-30s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M')
logger = logging.getLogger(__file__)

MQTT_BROKER_CONFIG_FILE = "mqtt_broker_conf.yaml"
MQTT_BROKER_CONFIG_WS_FILE = "mqtt_broker_conf_ws.yaml"


@pytest.mark.skip("does real calls, so don't run as unit-test")
def test_mqtt_app_func():
    def on_message(topic: str, msg: str) -> None:
        logger.info(f"{topic} -> {msg}")

    def func(app: MqttApp):
        while True:
            global loop_cnt
            app.publish("hot_topic", f"message #{loop_cnt}")
            loop_cnt += 1
            if loop_cnt == 10:
                raise Exception("fail!")
            sleep(2)

    app = MqttApp(MqttConfig.load(MQTT_BROKER_CONFIG_FILE), "mqttApp")
    app.on_message = (on_message, "hot_topic")
    app.func = func
    app.start()


@pytest.mark.skip("does real calls, so don't run as unit-test")
def test_mqtt_app_loop_func():
    def on_message(topic: str, msg: str) -> None:
        logger.info(f"{topic} -> {msg}")

    def loop_func(app: MqttApp):
        global loop_cnt
        app.publish("hot_topic", f"message #{loop_cnt}")
        loop_cnt += 1
        if loop_cnt == 10:
            raise Exception("fail!")

    def on_connected():
        logger.info("connected")

    app = MqttApp(MqttConfig.load(MQTT_BROKER_CONFIG_FILE), "mqttApp")
    app.on_message = (on_message, "hot_topic")
    app.on_connected = on_connected
    app.loop_func = (loop_func, 2)
    app.start()


@pytest.mark.skip("does real calls, so don't run as unit-test")
def test_mqtt_app_websockets():
    def on_message(topic: str, msg: str) -> None:
        logger.info(f"{topic} -> {msg}")

    def loop_func(app: MqttApp):
        global loop_cnt
        app.publish("hot_topic", f"message #{loop_cnt}")
        loop_cnt += 1
        if loop_cnt == 10:
            raise Exception("fail!")

    def on_connected():
        logger.info("connected")

    app = MqttApp(MqttConfig.load(MQTT_BROKER_CONFIG_WS_FILE), "mqttApp")
    app.on_message = (on_message, "hot_topic")
    app.on_connected = on_connected
    app.loop_func = (loop_func, 2)
    app.start()

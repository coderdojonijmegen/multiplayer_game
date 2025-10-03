import logging
from datetime import datetime
from threading import Thread
from time import sleep
from collections.abc import Callable

from paho.mqtt.client import Client
from paho.mqtt.enums import MQTTErrorCode

from .mqtt_config import MqttConfig

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-6s %(filename)-15s %(funcName)s L%(lineno)d :: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__file__)

CallbackOnMessage = Callable[[str, str], None]
CallbackFunc = Callable[[Client], None]
CallbackLoopFunc = Callable[[Client], None]
CallbackOnConnected = Callable


class MqttApp:

    def __init__(self, config: MqttConfig, client_id: str):
        self._topic = None
        self._on_message_ = None
        self._on_connected_func = None
        self._func = None
        self._loop_func = None
        self._loop_func_interval_s = None
        self._loop_func_thread = None
        self._caught_exception = None
        self.config = config
        self.client_id = client_id
        if config.websocket_path:
            self.client = Client(client_id=client_id, transport='websockets')
            self.client.ws_set_options(path=config.websocket_path)
            self.client.tls_set()
        else:
            self.client = Client(client_id=client_id, transport='tcp')
        self.client.username_pw_set(username=config.username, password=config.password)
        self.client.will_set(f"clients/{client_id}", "disconnected", retain=True)

    @property
    def on_message(self) -> CallbackOnMessage:
        return self._on_message_

    @on_message.setter
    def on_message(self, args: tuple) -> None:
        """
        Register a function to execute once a message is received and pass the topic(s) to listen to:
        (on_message, topic) where topic is on of `topic` or `(topic, qos)` or `[(topic1, qos), (topic2, qos)]`
        :param args: tuple of function pointer and topic(s)
        :return: None
        """
        if not isinstance(args, tuple):
            raise Exception("on_message requires 2 arguments, a function and one or more topics")
        self._on_message_ = args[0]
        self._topic = args[1]

    @property
    def on_connected(self) -> CallbackOnConnected:
        return self._on_connected_func

    @on_connected.setter
    def on_connected(self, on_connected_func: CallbackOnConnected):
        self._on_connected_func = on_connected_func

    @property
    def func(self) -> CallbackFunc:
        return self._func

    @func.setter
    def func(self, func: CallbackFunc) -> None:
        if self._loop_func:
            raise Exception("a loop function was already declared!")
        self._func = func

    @property
    def loop_func(self) -> CallbackLoopFunc:
        return self._func

    @loop_func.setter
    def loop_func(self, args: tuple) -> None:
        """
        Specifies a function to loop over with a given interval in seconds.
        :param args: tuple of function pointer and interval in s: (do_loop, 3)
        :return:
        """
        if self._func:
            raise Exception("a function was already declared!")
        self._loop_func = args[0]
        self._loop_func_interval_s = args[1]

    def publish(self, topic: str, message: str) -> None:
        self.client.publish(topic, message, qos=2, retain=True)

    def _on_connect(self, client: Client, userdata, flags, rc) -> None:
        logger.info(f"connected, subscribing to {self._topic}")
        if self._topic:
            client.subscribe(self._topic)
        client.publish(f"clients/{self.client_id}", f"connected since {datetime.now()}", retain=True)
        if self._on_connected_func:
            self._on_connected_func()

    def _on_disconnect(self, client, userdata, flags, rc=0) -> None:
        logger.warning(f"got disconnected: {flags.name}")
        if flags != MQTTErrorCode.MQTT_ERR_SUCCESS:
            logger.warning(f"client_id = {self.client_id}; same client_id already connected to broker?\nreconnecting...")
            client.reconnect()

    def _on_message(self, client: Client, userdata, msg):
        if self._on_message_:
            self._on_message_(msg.topic, msg.payload.decode("utf-8"))

    def _loop_func_(self):
        try:
            is_first_call = True
            while True:
                self._loop_func(self.client)
                if is_first_call:
                    logger.info("successfully made first call to loop function")
                    is_first_call = False
                sleep(self._loop_func_interval_s)
        except Exception as e:
            self._caught_exception = e
            self.client.disconnect()
            logger.error(e)

    def _func_(self):
        try:
            self._func(self.client)
        except Exception as e:
            self._caught_exception = e
            self.client.disconnect()
            logger.error(e)

    def start(self) -> None:
        logger.info(f"starting app {self.client_id}")
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.client.connect(self.config.ip, port=self.config.port, keepalive=self.config.keep_alive_s)
        if self._loop_func:
            logger.info("starting loop function")
            self._loop_func_thread = Thread(target=self._loop_func_, daemon=True).start()
        if self._func:
            logger.info("starting function")
            self._loop_func_thread = Thread(target=self._func_, daemon=True).start()
        self.client.loop_forever()
        if self._caught_exception:
            raise self._caught_exception

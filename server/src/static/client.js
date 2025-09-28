const BROKER_ADDRESS = "drone-game.coderdojo-nijmegen.nl";
const mqtt = window.mqtt;


class GameClient {
    constructor(topics = [], brokerAddress = BROKER_ADDRESS, debug=false) {
        this.onStatusUpdate = (topic, message) => {
        };
        this.brokerAddress = brokerAddress;
        this.topics = topics;
        this.debug = debug;
        this.debugElem = null;
        this.clientId = null;
        this.mqtt_client = null;

        if (this.debug) {
            let divElement = document.createElement("div");
            document.getElementsByTagName("body")[0].appendChild(divElement);
            this.debugElem = divElement;
        }
        this.#registerClient()
            .then(clientId => {
                this.log("ClientId: " + clientId)
                this.clientId = clientId;
                this.topics.push(`drone-game/client/state/${clientId}`);
                this.#initMqttApp(clientId);
                this.#subscribeToTopics();
                this.#setupOnStatusUpdateHandler();
            });
    }

    #registerClient() {
        return fetch('/register', {method: 'POST'})
            .then(response => response.json())
            .then(data => data.client_id)
            .catch(error => console.log(error));
    }

    #initMqttApp(clientId) {
        let mqtt_client = mqtt.connect(
            `ws://${this.brokerAddress}:8083`,
            {
                clientId: clientId,
                username: "ninja",
                password: "welkom!",
                will: {
                    topic: `clients/drone-game/${clientId}`,
                    payload: 'disconnected',
                    qos: 2,
                    retain: true
                }
            }
        );

        mqtt_client.on("connect", () => {
            this.log("connected to MQTT broker");
            mqtt_client.publish(`clients/drone-game/${clientId}`, `connected since ${new Date()}`, {
                qos: 2,
                retain: true
            });
        });

        this.mqtt_client = mqtt_client;
    }

    #subscribeToTopics() {
        this.topics.forEach(topic => {
            this.mqtt_client.subscribe(topic, (err) => {
                this.log("subscribed to " + topic);
            });
        });
    }

    #setupOnStatusUpdateHandler() {
        this.mqtt_client.on("message", (topic, message) => {
            this.onStatusUpdate(topic, message);
        });
    }

    log(message) {
        if (this.debug) {
            this.debugElem.innerHTML += message + "<br>";
        }
        console.log(message);
    }
}

export {GameClient};

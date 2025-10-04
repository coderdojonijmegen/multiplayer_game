const BROKER_ADDRESS = "drone-game.coderdojo-nijmegen.nl";
const ROLE = "gamer"
const mqtt = window.mqtt;


class GameClient {
    constructor(topics = [], brokerAddress = BROKER_ADDRESS, role = ROLE, debug = false) {
        this.onStatusUpdate = (topic, message) => {
        };
        this.role = role;
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
    }

    async connect() {
        return new Promise((resolve, reject) => {
            this.#registerClient()
                .then(clientId => {
                    this.log("ClientId: " + clientId)
                    this.clientId = clientId;
                    this.topics.push(`drone-game/client/${clientId}`);
                    this.#initMqttApp(clientId, () => {
                        this.#subscribeToTopics();
                        this.#setupOnStatusUpdateHandler();
                        resolve(this);
                    });
                });
        });
    }

    #registerClient() {
        return fetch('/register', {
            method: 'POST',
            body: JSON.stringify({"role": this.role}),
            headers: {'Content-Type': 'application/json'}
        })
            .then(response => response.json())
            .then(data => data.client_id)
            .catch(error => console.log(error));
    }

    #initMqttApp(clientId, onConnected) {
        this.mqtt_client = mqtt.connect(
            `wss://${this.brokerAddress}/mqtt`,
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

        this.mqtt_client.on("connect", () => {
            this.log("connected to MQTT broker");
            this.mqtt_client.publish(`clients/drone-game/${clientId}`, `connected since ${new Date().toLocaleString("nl")}`, {
                qos: 2,
                retain: true
            });
            onConnected();
        });
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

    publish(topic, message) {
        this.mqtt_client.publish(topic, message);
    }

    log(message) {
        if (this.debug) {
            this.debugElem.innerHTML += message + "<br>";
        }
        console.log(message);
    }

}

class GameClientBuilder {
    constructor() {
        this.topics = [];
        this.brokerAddress = BROKER_ADDRESS;
        this.role = ROLE;
        this.debug = false;
    }

    withTopics(topics) {
        this.topics = topics;
        return this;
    }

    withBrokerAddress(brokerAddress) {
        this.brokerAddress = brokerAddress;
        return this;
    }

    withRole(role) {
        this.role = role;
        return this;
    }

    withDebug(debug) {
        this.debug = debug;
        return this;
    }

    build() {
        return new GameClient(this.topics, this.brokerAddress, this.role, this.debug);
    }
}

export {GameClient, GameClientBuilder};

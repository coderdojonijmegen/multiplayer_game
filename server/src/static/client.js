const BROKER_ADDRESS = "drone-game.coderdojo-nijmegen.nl";
const ROLE = "gamer"
const PLATFORM = "js"
const mqtt = window.mqtt;


class GameClient {
    constructor(topics, brokerAddress, role, showConnectionStatus) {
        this.onStatusUpdate = (topic, message) => {
        };
        this.role = role;
        this.brokerAddress = brokerAddress;
        this.topics = topics;
        this.showConnectionStatus = showConnectionStatus;
        this.connectionStatusElem = null;
        this.clientId = null;
        this.mqtt_client = null;

        if (this.showConnectionStatus) {
            this.connectionStatusElem = document.getElementById("clientConnectionLog");
            document.getElementById('toggleConnectionLog').addEventListener('click', () => {
                document.getElementById('connectionLogCard').classList.toggle('d-none');
            });
        }
    }

    async connect() {
        return new Promise((resolve, reject) => {
            this.#registerClient()
                .then(clientId => {
                    this.log(`ClientId: <i>${clientId}</i>`)
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
            body: JSON.stringify({
                "role": this.role,
                "platform": PLATFORM
            }),
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
            this.log(`verbonden met MQTT broker <i>${this.brokerAddress}</i>`);
            this.mqtt_client.publish(`clients/drone-game/${clientId}`, `verbonden sinds ${new Date().toLocaleString("nl")}`, {
                qos: 2,
                retain: true
            });
            onConnected();
        });
    }

    #subscribeToTopics() {
        this.topics.forEach(topic => {
            this.mqtt_client.subscribe(topic, (err) => {
                this.log(`geabonneerd op <i>${topic}</i>`);
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
        if (this.showConnectionStatus) {
            this.connectionStatusElem.innerHTML += message + "<br>";
        }
        console.log(message);
    }

}

class GameClientBuilder {
    constructor() {
        this.topics = [];
        this.brokerAddress = BROKER_ADDRESS;
        this.role = ROLE;
        this.showConnectionStatus = true;
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

    withShowConnectionStatus(showConnectionStatus) {
        this.showConnectionStatus = showConnectionStatus;
        return this;
    }

    build() {
        return new GameClient(this.topics, this.brokerAddress, this.role, this.showConnectionStatus);
    }
}

export {GameClient, GameClientBuilder};

class ClientList {

    constructor(client, elementId) {
        this.client = client;
        this.logElem = document.getElementById(elementId);
        this.clientList = {};
    }

    onStatusUpdate(topic, message) {
        if (topic.startsWith("clients/drone-game/")) {
            this.clientList[topic] = message;
            this.logElem.innerHTML = "";
            for (const [topic, message] of Object.entries(this.clientList)) {
                let isThisDashboard = topic.includes(this.client.clientId) ? " - dit dashboard" : "";
                this.logElem.innerHTML += `${topic} - ${message} ${isThisDashboard}<br>`;
            }
        }
    }

}

export {ClientList};
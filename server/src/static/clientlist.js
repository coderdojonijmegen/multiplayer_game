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
                const isThisDashboardId = topic.includes(this.client.clientId);
                let isThisDashboard = isThisDashboardId ? " - dit dashboard" : "";
                this.logElem.innerHTML += `${isThisDashboard? "<b>" : ""}${topic} - ${message} ${isThisDashboard}${isThisDashboard? "</b>" : ""}<br>`;
            }
        }
    }

}

export {ClientList};
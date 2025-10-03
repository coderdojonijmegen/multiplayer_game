import {ClientList} from "./clientlist.js";
import {PlayGround} from "./playground.js";


class Dashboard {

    constructor(client) {
        this.client = client;
        this.modules = [
            new ClientList(client, "clientConnectionLog"),
            new PlayGround(client, "gamePlayGround"),
        ]
        this.#onStatusUpdate();
    }

    #onStatusUpdate() {
        this.client.onStatusUpdate = (topic, message) => {
            for (const module of this.modules) {
                module.onStatusUpdate(topic, message);
            }
        }
    }
}

export {Dashboard};
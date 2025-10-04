import {PlayGround} from "/static/playground.js";

class GameEditor {

    constructor(client, codeElementId, buttonElementId, gameLogElemId) {
        this.onStatusUpdate = (status) => {
        };
        this.client = client;
        this.codeElem = document.getElementById(codeElementId);
        let code = localStorage.getItem("userCode");
        if (code) {
            this.codeElem.value = code;
        } else {
            this.codeElem.value = `let xDir = 1;
    this.onStatusUpdate = (status) => {
        if (status.drone.position.x < 0 || status.drone.position.x > 100) {
            xDir = -xDir;
            this.#log(\`xDir flipped to \${xDir}\`);
        }
        this.#sendAction({
            "position": {
                "x": status.drone.position.x + xDir,
                "y": status.drone.position.y
            }
        });
}
        `;
        }
        this.gameLogElem = document.getElementById(gameLogElemId);
        this.runButton = document.getElementById(buttonElementId);
        this.runButton.addEventListener("click", (event) => this.#onRun(event));
        this.playground = new PlayGround(client, "gamePlayGround");
        this.client.onStatusUpdate = (topic, message) => {
            if (!topic.startsWith("clients/drone-game/")) {
                this.onStatusUpdate(JSON.parse(message));
            }
            this.playground.onStatusUpdate(topic, message);
        };
    }

    #onRun(event) {
        let code = this.codeElem.value;
        localStorage.setItem("userCode", code);
        try {
            eval(code);
            this.#log("running code...")
        } catch (e) {
            this.#log(`Fout in script: ${e}`);
        }
    }

    #sendAction(action) {
        action.drone_id = this.client.clientId;
        this.client.publish(`drone-game/client/${this.client.clientId}/action`, JSON.stringify(action));
    }

    #log(message) {
        this.gameLogElem.value = `${new Date().toLocaleTimeString("nl")} - ${message} \n${this.gameLogElem.value}`;
    }

}

export {GameEditor}

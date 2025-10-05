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
    this.#log(\`x=\${status.drone.position.x}\`);
    if (status.drone.position.x <= 0) {
        xDir = 1;
    else if (status.drone.position.x >= 100) {
        xDir = -1;
    }
    this.#sendAction({
        "position": {
            "x": status.drone.position.x + xDir,
            "y": Math.sin(status.drone.position.x/2) * 5 + 30
        }
    });
}`;
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
        let loglines = this.gameLogElem.value.split('\\n');
        loglines.unshift(`${new Date().toLocaleTimeString("nl")} - ${message}`);
        this.gameLogElem.value = loglines.slice(0, 20).join('\\n');
    }

}

export {GameEditor}

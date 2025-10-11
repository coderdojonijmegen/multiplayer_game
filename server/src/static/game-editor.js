import {PlayGround} from "/static/playground.js";

const CODE_EXAMPLE = `let xDir = 1;
this.onStatusUpdate = (status) => {
    this.#log(\`x=\${status.drone.position.x} y=\${status.drone.position.y}\`);
    let hasBook = status.drone.hasBook;
    let bookShelfX = status.game.bookShelfX;
    let releasedBook = false;
    if (status.drone.position.x <= 0) {
        xDir = 1;
        hasBook = true;
    } else if (status.drone.position.x >= 65) {
        xDir = -1;
        hasBook = false;
    }
    let x = status.drone.position.x;
    let y = status.drone.position.y;
    if (hasBook && status.drone.position.x == bookShelfX) {
        releasedBook = true;
        hasBook = false;
    } else {
         x += xDir;
         y = Math.round(Math.sin(status.drone.position.x*2/3) * 3 + 10)
    }
    this.#sendAction({
        "position": {
            "x": x,
            "y": y
        },
        "hasBook": hasBook,
         "releasedBook": releasedBook
    });
}
`;

class GameEditor {

    constructor(client) {
        this.onStatusUpdate = (status) => {
        };
        this.client = client;
        this.codeElem = document.getElementById("game-editor");
        let code = localStorage.getItem("userCode");
        if (code) {
            this.codeElem.value = code;
        } else {
            this.codeElem.value = CODE_EXAMPLE;
        }
        this.gameLogElem = document.getElementById("game-log");
        this.runButton = document.getElementById("run-game");
        this.runButton.addEventListener("click", (event) => this.#onRun(event));
        this.resetButton = document.getElementById("reset-code");
        this.resetButton.addEventListener("click", (event) => {
            this.codeElem.value = CODE_EXAMPLE;
            localStorage.setItem("userCode", this.codeElem.value);
        });
        this.playground = new PlayGround(client, "gamePlayGround");
        this.client.onStatusUpdate = (topic, message) => {
            if (!topic.startsWith("clients/drone-game/")) {
                this.onStatusUpdate(JSON.parse(message));
            }
            this.playground.onStatusUpdate(topic, message);
        };
         document.getElementById('toggleEditor').addEventListener('click', () => {
             document.getElementById('editorOverlay').classList.toggle('hidden');
         });
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
        let loglines = this.gameLogElem.value.split('\n');
        loglines.unshift(`${new Date().toLocaleTimeString("nl")} - ${message}`);
        this.gameLogElem.value = loglines.slice(0, 20).join('\n');
    }

}

export {GameEditor}

class Drone {
    #W = 20;
    #H = 20;

    constructor(ctx) {
        this.ctx = ctx;
        this._position = null;
        this._color = null;
        this._book = false;
    }
    
    position(position) {
        this._position = position;
        return this;
    }

    color(color) {
        this._color = color;
        return this;
    }

    withBook() {
        this._book = true;
        return this;
    }

    draw() {
        this.ctx.fillStyle = this._color;
        // rotors
        this.ctx.fillRect(this._position.x * this.#W, this._position.y * this.#H, 7, 3);
        this.ctx.fillRect(this._position.x * this.#W + this.#W - 7, this._position.y * this.#H, 7, 3);

        // rotor pins
        this.ctx.fillRect(this._position.x * this.#W + 2, this._position.y * this.#H + 3, 3, 3);
        this.ctx.fillRect(this._position.x * this.#W + this.#W - 5, this._position.y * this.#H + 3, 3, 3);

        // drone body
        this.ctx.fillRect(this._position.x * this.#W + 3, this._position.y * this.#H + 6, 14, 3);

        // drone bookholder
        this.ctx.fillRect(this._position.x * this.#W + 8, this._position.y * this.#H + 9, 4, 2);

        if (this._book) {
            this.ctx.fillStyle = "gray";
            this.ctx.fillRect(this._position.x * this.#W + 2, this._position.y * this.#H + 11, 16, 4);
        }
    }
}

class PlayGround {

    #COLORS = [
        "red",
        "blue",
        "yellow",
        "green",
        "orange",
        "purple",
    ];

    constructor(client, elementId) {
        this.client = client;
        this.canvas = document.getElementById(elementId);
        this.ctx = this.canvas.getContext("2d");
    }

    onStatusUpdate(topic, message) {
        if (topic === `drone-game/client/${this.client.clientId}`) {
            this.ctx.fillStyle = "black";
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

            const game = JSON.parse(message).game;
            const drones = game.drone_positions;
            for (const [idx, drone] of drones.entries()) {
                let dr = new Drone(this.ctx)
                    .position(drone.position)
                    .color(this.#COLORS[idx % this.#COLORS.length]);
                if (drone.hasBook) {
                    dr.withBook();
                }
                dr.draw();
            }

            if (game.books) {
                const books = game.books;
                for (const book of books) {
                    this.ctx.fillStyle = "gray";
                    this.ctx.fillRect(book.position.x, book.position.y, 16, 4);
                }
            }
        }
    }
}

export {PlayGround}

class Drone {
    #W = 20;
    #H = 20;

    constructor(ctx) {
        this.ctx = ctx;
        this._position = null;
        this._color = null;
        this._name = null;
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

    withName(name) {
        this._name = name;
        return this;
    }

    draw() {
        const x = this._position.x * this.#W;
        const y = this._position.y * this.#H;

        this.ctx.fillStyle = this._color;
        // rotors
        this.ctx.fillRect(x, y, 8, 2);
        this.ctx.fillRect(x + this.#W - 8, y, 8, 2);

        // rotor pins
        this.ctx.fillRect(x + 3, y + 2, 2, 2);
        this.ctx.fillRect(x + this.#W - 5, y + 2, 2, 2);

        // drone body
        this.ctx.fillRect(x + 3, y + 4, 14, 3);

        // drone bookholder
        this.ctx.fillRect(x + 8, y + 7, 4, 2);

        // drone name
        this.ctx.font = "11px sans-serif";
        this.ctx.fillText(this._name, x - 10, y - 5);

        if (this._book) {
            this.ctx.fillStyle = "gray";
            this.ctx.fillRect(x + 2, y + 9, 16, 4);
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
                    .color(this.#COLORS[idx % this.#COLORS.length])
                    .withName(drone.name);
                if (drone.hasBook) {
                    dr.withBook();
                }
                dr.draw();
            }

            if (game.books) {
                const books = game.books;
                const booksAtBottom = game.books.filter(book => book.reachedBottom);
                for (const book of books) {
                    this.ctx.fillStyle = "gray";
                    this.ctx.fillRect(book.position.x, book.position.y, 16, 4);
                }

                // book count
                if (booksAtBottom.length > 0) {
                    this.ctx.font = "11px sans-serif";
                    this.ctx.fillText(`${booksAtBottom.length} books`, books[0].position.x + 25, 700 - 5);
                }
            }
        }
    }
}

export {PlayGround}

import {droneImage} from "/static/drone-image.js";

class Drone {
    #W = 20;
    #H = 20;

    constructor(ctx, droneId) {
        this.ctx = ctx;
        this.droneId = droneId;
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

    withBook(hasBook) {
        this._book = hasBook;
        return this;
    }

    withName(name) {
        this._name = name;
        return this;
    }

    withDroneImage(image) {
        this._drone = image;
        return this;
    }

    draw() {
        if (this.droneId === "127.0.0.1/gamer/py") {
            console.log(this._position);
        }
        const x = this._position.x * this.#W;
        const y = this._position.y * this.#H;

        if (this._drone === undefined) {
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
        } else {
            this.ctx.drawImage(this._drone, x, y, this.#W, this.#H);
        }
        // drone name
        this.ctx.font = "11px sans-serif";
        this.ctx.fillText(this._name === null? this.droneId: this._name, x - 10, y - 5);

        if (this._book) {
            this.ctx.fillStyle = "gray";
            this.ctx.fillRect(x + 2, y + 20, 16, 4);
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
        this.drones = [];
    }

    onStatusUpdate(topic, message) {
        if (topic === `drone-game/client/${this.client.clientId}`) {
            this.ctx.fillStyle = "black";
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

            const game = JSON.parse(message).game;
            const drones = game.drone_positions;
            for (const [idx, drone] of drones.entries()) {
                let dr = this.drones.find(d => d.droneId === drone.drone_id);
                if (dr === undefined) {
                    let img = new Image();
                    img.src = droneImage();
                    dr = new Drone(this.ctx, drone.drone_id)
                        .color(this.#COLORS[idx % this.#COLORS.length])
                        .withName(drone.name)
                        .withDroneImage(img);
                    this.drones.push(dr);
                }
                dr.withBook(drone.hasBook)
                    .position(drone.position)
                    .draw();
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

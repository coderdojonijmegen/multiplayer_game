class PlayGround {

    #W = 10;
    #H = 10;
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

            const drones = JSON.parse(message).game.drone_positions;
            console.log(drones);
            for (const [idx, drone] of drones.entries()) {
                this.ctx.fillStyle = this.#COLORS [idx % this.#COLORS.length];
                this.ctx.fillRect(drone.position.x * this.#W, drone.position.y * this.#H, this.#W, this.#H);
            }
        }
    }
}

export {PlayGround}

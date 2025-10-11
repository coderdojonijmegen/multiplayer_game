# Software requirements voor de Drone Multi-player Game

## Systeem

- we gebruiken een centrale server met een domeinnaam: drone-game.coderdojo-nijmegen.nl
    - doordat we een centrale server gebruiken, hoeven we geen discovery mechanismen te implementeren (één van de functionaliteiten van Network Zero)
- we gebruiken MQTT voor de communicatie
    - want beschikbaar in de browser (Javascript) en in Python
    - want bi-directioneel, waardoor de client event-driven kan zijn en geen polling mechanisme hoeft te implementeren
    - overweging MQTT:
        - handig subscriben op topics (bijvoorbeeld game state)
        - kan eenvoudig event-driven worden gebruikt voor ontvangen van informatie
        - extra container, naast gameserver container
        - adresseren clients via topicnaam of message body?

### Architectuur

```mermaid
architecture-beta
    group game(cloud)[Multiplayer Drone Game]
    group laptop(server)[Laptop]

    service browser(internet)[browser client] in laptop
    service client(server)[Python client] in laptop

    service broker(server)[MQTT broker] in game
    service server(server)[web server] in game
    service engine(server)[Game Engine] in game

    engine:R -- L:broker
    server:T -- L:broker

    browser:T -- L:broker
    client:T -- L:broker

```

De Ninja speelt het spel op haar/zijn laptop. Dat kan met een Python script in Thonny, maar ook in Visual Studio Code met Javascript wat in de browser wordt uitgevoegd.

- Python client: 
- Browser client: 
- MQTT broker: berichten schakelpunt waar verschillende blokken in het systeem 
- Game engine: ontvangt berichten van de clients via het schakelpunt en verwerkt de informatie in de game state
- web server: serveert een dashboard dat een overzicht toont van de bibliotheken, boekentorens en vliegende drones, biedt ook een paar endpoints om een nieuwe client aan te melden bij de game engine

## Clients

De clients hebben verschillende rollen en geven die ook mee aan de server voor het bepalen van het client ID. Dit maakt het mogelijk om zowel een dashboard als gamer rol
op één machine te laten werken. Het clientId voor het verbinden aan de MQTT broker moet uniek zijn, dus met enkel het IP adres als clientId gebruiken zou het dan niet mogelijk
zijn om zowel een dashboard als gamer vanaf één machine te draaien. De gamer kan vervolgens nog geïmplementeerd worden in Javascript en Python en van dezelfde machine worden
uitgevoerd, hoewel dat een uitzonderlijke situatie zal zijn.

Mogelijke rollen zijn:

- gamer/py
- gamer/js
- dashboard/js

De mogelijke clientId's worden dan:

- `<IP>/gamer/py`: gamer geïmplementeerd in Python
- `<IP>/gamer/js`: gamer geïmplementeerd in Javascript
- `<IP>/dashboard/js`: dashboard geïmplementeerd in Javascript, tevens enige implmentatie
- `engine`: game engine
- `bot`: bot die eventueel ingezet wordt om de drones te laten bewegen; handig bij het testen van de playground

### Javascript

#### Dashboard
```mermaid
sequenceDiagram
    Actor ninja
    participant dashboard as dashboard<br>in browser
    participant javascript_client
    participant webserver
    participant mqtt_broker
    participant engine

    ninja ->> dashboard: open dashboard in browser<br/>drone-game.coderdojo-nijmegen.nl
    dashboard ->> webserver: laadt client en dashboard javascript modules van server
    webserver -->> dashboard: client en dashboard javascript modules
    dashboard ->> javascript_client: start client
    javascript_client ->> webserver: haal clientId op bij de server<br>rol: dashboard, platform: js
    webserver ->> webserver: concat IP, rol en platform<br>tot uniek ID: <IP>/<rol>/<platform>
    webserver -->> javascript_client: clientId

    javascript_client ->> mqtt_broker: verbindt met broker en <br>publiceer huidige datum/tijd op<br>"clients/drone-game/<clientId>"
    mqtt_broker --) javascript_client: onClientsUpdate: "clients/drone-game/#35;"<br>werk overzicht van clients bij
    mqtt_broker --) javascript_client: onGamestateUpdate: "drone-game/client/<clientId>"<br>teken dashboard
    javascript_client -) dashboard: update dashboard
   
```

#### Drone besturen
```mermaid
sequenceDiagram
    Actor ninja
    participant dashboard as dashboard<br>in browser
    participant javascript_client
    participant webserver
    participant mqtt_broker
    participant engine

    ninja ->> dashboard: open dashboard in browser<br/>drone-game.coderdojo-nijmegen.nl
    dashboard ->> webserver: laadt client en dashboard javascript modules van server
    webserver -->> dashboard: client en dashboard javascript modules
    dashboard ->> javascript_client: start client
    javascript_client ->> webserver: haal clientId op bij de server<br>rol: dashboard, platform: js
    webserver ->> webserver: concat IP, rol en platform<br>tot uniek ID: <IP>/<rol>/<platform>
    webserver -->> javascript_client: clientId

    javascript_client ->> mqtt_broker: verbindt met broker en <br>publiceer huidige datum/tijd op<br>"clients/drone-game/<clientId>"

    loop voor elke game cycle
        mqtt_broker --) javascript_client: onGamestateUpdate: "drone-game/client/<clientId>"
        javascript_client ->> javascript_client: bereken volgende stap
        javascript_client -) mqtt_broker: "drone-game/client/<clientId>/action"<br>publiceer volgende stap
        mqtt_broker -) engine: onClientAction: "drone-game/client/<clientId>/action"<br>voeg client action toe aan game state
        engine ->> engine: onGameStateTrigger:<br>bereken nieuwe game state op<br>basis van input alle clients
        loop voor elke client
            engine -) mqtt_broker: publish: "drone-game/client/<clientId>"<br>publiceer game state en client state
        end
    end
```

# Topics

## `clients/drone-game/#`

* `clients/drone-game/<IP>/<rol>/<platform>`
* `clients/drone-game/bot`
* `clients/drone-game/engine`

Een client haalt 

## `drone-game/client/<IP>/<rol>`

## `drone-game/client/<IP>/gamer/action`
